import csv
import json
from datetime import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class Notificacion:
    def enviar_notificacion(self, mensaje):
        pass


class Correo(Notificacion):
    def enviar_notificacion(self, mensaje, correo):
        print(f"Enviando correo a {correo} con mensaje: {mensaje}")


class Celular(Notificacion):
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando SMS a {numero} con mensaje: {mensaje}")


class Whatsapp(Notificacion):
    def enviar_notificacion(self, mensaje, numero):
        print(f"Enviando Whatsapp a {numero} con mensaje: {mensaje}")


class Persona:
    def __init__(self, identificacion, nombre, celular):
        self.identificacion = identificacion
        self.nombre = nombre
        self.celular = celular


class Medico(Persona):
    def __init__(self, identificacion, nombre, celular, especialidad):
        super().__init__(identificacion, nombre, celular)
        self.especialidad = especialidad
        self.calificaciones = []

    def calificacion_promedio(self):
        if not self.calificaciones:
            return 0
        return sum(self.calificaciones) / len(self.calificaciones)


class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular)
        self.correo = correo


class Cita:
    def __init__(self, paciente, medico, fecha_hora):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.motivo_cancelacion = None
        self.calificacion = None
        self.comentario = None

    def __repr__(self):
        return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

    def agregar_feedback(self, calificacion, comentario):
        self.calificacion = calificacion
        self.comentario = comentario
        self.medico.calificaciones.append(calificacion)


class CitaUrgente(Cita):
    def __init__(self, paciente, medico, fecha_hora):
        super().__init__(paciente, medico, fecha_hora)
        self.es_urgencia = True

    def __repr__(self):
        return f"Cita URGENTE del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"


class Agenda:
    def __init__(self):
        self.citas = []

    def agendar_cita(self, cita):
        # Verificar si hay conflicto de horarios
        for c in self.citas:
            if c.medico == cita.medico and c.fecha_hora == cita.fecha_hora:
                if isinstance(cita, CitaUrgente) and not isinstance(c, CitaUrgente):
                    # Mover la cita existente si la nueva es urgente
                    nueva_fecha = self.encontrar_siguiente_horario_disponible(
                        c.medico, c.fecha_hora
                    )
                    c.fecha_hora = nueva_fecha
                    console.print(
                        f"[yellow]La cita existente ha sido movida a {nueva_fecha} debido a una urgencia.[/yellow]"
                    )
                else:
                    raise ValueError(
                        "Ya existe una cita en ese horario para este médico."
                    )

        self.citas.append(cita)
        console.print(f"[green]Cita agendada: {cita}[/green]")

    def encontrar_siguiente_horario_disponible(self, medico, fecha_hora):
        # Lógica simple: buscar el siguiente horario disponible en intervalos de 1 hora
        nueva_fecha = fecha_hora
        while True:
            nueva_fecha = nueva_fecha.replace(hour=(nueva_fecha.hour + 1) % 24)
            if not any(
                c.medico == medico and c.fecha_hora == nueva_fecha for c in self.citas
            ):
                return nueva_fecha

    def cancelar_cita(self, cita, motivo):
        if cita in self.citas:
            self.citas.remove(cita)
            cita.motivo_cancelacion = motivo
            print(f"Cita cancelada: {cita}")
        else:
            print("La cita no existe en la agenda.")

    def mover_cita(self, cita, nueva_fecha_hora):
        if cita in self.citas:
            cita.fecha_hora = nueva_fecha_hora
            print(f"Cita movida: {cita}")
        else:
            print("La cita no existe en la agenda.")

    def buscar_citas_paciente(self, paciente):
        return [cita for cita in self.citas if cita.paciente == paciente]

    def buscar_citas_medico(self, medico):
        return [cita for cita in self.citas if cita.medico == medico]


class Hospital:
    def __init__(self):
        self.pacientes = []
        self.medicos = []
        self.agenda = Agenda()

    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)
        # print(f"Paciente {paciente.nombre} agregado al hospital.")

    def agregar_medico(self, medico):
        self.medicos.append(medico)
        # print(f"Médico {medico.nombre} agregado al hospital.")

    def buscar_paciente(self, identificacion):
        return next(
            (p for p in self.pacientes if p.identificacion == identificacion), None
        )

    def buscar_medico(self, identificacion):
        return next(
            (m for m in self.medicos if m.identificacion == identificacion), None
        )

    def buscar_medicos_por_especialidad(self, especialidad):
        return [m for m in self.medicos if m.especialidad == especialidad]

    def cargar_pacientes_desde_csv(self, archivo):
        try:
            with open(archivo, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    paciente = Paciente(
                        row["identificación"],
                        row["nombre_completo"],
                        row["celular"],
                        row["correo"],
                    )
                    self.agregar_paciente(paciente)
            console.print(
                "[green]Pacientes cargados exitosamente desde el archivo CSV.[/green]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo CSV.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar pacientes: {str(e)}[/red]")

    def cargar_medicos_desde_json(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as jsonfile:
                medicos_data = json.load(jsonfile)
                for medico_data in medicos_data:
                    # Asegurarse de que todos los campos necesarios estén presentes
                    if all(
                        key in medico_data
                        for key in ["id", "nombre", "celular", "especialidad"]
                    ):
                        medico = Medico(
                            medico_data["id"],
                            medico_data["nombre"],
                            medico_data["celular"],
                            medico_data["especialidad"],
                        )
                        self.agregar_medico(medico)
                    else:
                        console.print(
                            f"[yellow]Advertencia: Datos incompletos para el médico {medico_data.get('nombre', 'desconocido')}[/yellow]"
                        )
            console.print(
                "[green]Médicos cargados exitosamente desde el archivo JSON.[/green]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo JSON.[/red]")
        except json.JSONDecodeError:
            console.print("[red]Error: El archivo JSON está mal formateado.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar médicos: {str(e)}[/red]")

    def cargar_citas_desde_csv(self, archivo):
        try:
            with open(archivo, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    paciente = self.buscar_paciente(row["paciente"])
                    medico = self.buscar_medico(row["medicos"])
                    if paciente and medico:
                        fecha_hora = datetime.strptime(
                            row["fecha_hora"], "%Y-%m-%d %H:%M:%S"
                        )
                        cita = Cita(paciente, medico, fecha_hora)
                        self.agenda.agendar_cita(cita)
                    else:
                        if not paciente:
                            console.print(
                                f"[yellow]Advertencia: No se encontró el paciente con ID {row['paciente']}[/yellow]"
                            )
                        if not medico:
                            console.print(
                                f"[yellow]Advertencia: No se encontró el médico con ID {row['medicos']}[/yellow]"
                            )
            console.print(
                "[green]Citas cargadas exitosamente desde el archivo CSV.[/green]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo CSV de citas.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar citas: {str(e)}[/red]")

    def agendar_cita_urgente(self, paciente, medico, fecha_hora):
        cita_urgente = CitaUrgente(paciente, medico, fecha_hora)
        self.agenda.agendar_cita(cita_urgente)

    def agregar_feedback_cita(self, cita, calificacion, comentario):
        if cita in self.agenda.citas:
            cita.agregar_feedback(calificacion, comentario)
            console.print(
                f"[green]Feedback agregado a la cita de {cita.paciente.nombre}[/green]"
            )
        else:
            console.print("[red]La cita no existe en la agenda.[/red]")


def cargar_datos_iniciales():
    hospital = Hospital()

    # Cargar pacientes iniciales
    hospital.cargar_pacientes_desde_csv("pacientes.csv")

    # Cargar médicos iniciales
    hospital.cargar_medicos_desde_json("medicos.json")

    # Cargar citas iniciales
    hospital.cargar_citas_desde_csv("citas.csv")

    return hospital


def mostrar_lista_pacientes(hospital):
    table = Table(title="[bold white]LISTA DE PACIENTES[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("CELULAR", style="green")
    table.add_column("CORREO ELECTRÓNICO", style="yellow")

    for paciente in hospital.pacientes:
        table.add_row(
            paciente.identificacion, paciente.nombre, paciente.celular, paciente.correo
        )

    console.print(table)


def mostrar_lista_medicos(hospital):
    table = Table(title="[bold white]LISTA DE MÉDICOS[/bold white]")
    table.add_column("ID", style="cyan")
    table.add_column("NOMBRE COMPLETO", style="magenta")
    table.add_column("ESPECIALIDAD", style="green")
    table.add_column("CELULAR", style="yellow")

    for medico in hospital.medicos:
        table.add_row(
            medico.identificacion, medico.nombre, medico.especialidad, medico.celular
        )

    console.print(table)


def mostrar_lista_citas(hospital):
    table = Table(title="[bold white]LISTA DE CITAS[/bold white]")
    table.add_column("PACIENTE", style="cyan")
    table.add_column("MÉDICO", style="magenta")
    table.add_column("ESPECIALIDAD", style="green")
    table.add_column("FECHA Y HORA", style="yellow")
    table.add_column("URGENCIAS", style="white")

    for cita in hospital.agenda.citas:
        urgente = "NO" if str(type(cita).__name__) == "Cita" else "SÍ"

        table.add_row(
            cita.paciente.nombre,
            cita.medico.nombre,
            cita.medico.especialidad,
            cita.fecha_hora.strftime("%Y-%m-%d %H:%M"),
            urgente,
        )

    console.print(table)


def mostrar_menu():
    console.print(
        Panel.fit(
            "1. Agregar paciente.\n"
            "2. Agregar médico.\n"
            "3. Agendar cita.\n"
            "4. Cancelar cita.\n"
            "5. Mover cita.\n"
            "6. Ver citas de un paciente.\n"
            "7. Ver citas de un médico.\n"
            "8. Ver lista de citas.\n"
            "9. Buscar un paciente.\n"
            "10. Buscar un médico.\n"
            "11. Agendar cita urgente.\n"
            "12. Agregar feedback a una cita.\n"
            "13. Ver calificaciones de médicos.\n"
            "14. Salir",
            title="Sistema de Citas Médicas",
            border_style="bold green",
        )
    )


def main():
    hospital = cargar_datos_iniciales()

    while True:
        mostrar_menu()
        opcion = Prompt.ask(
            "Seleccione una opción",
            choices=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
            ],
        )

        if opcion == "1":
            identificacion = Prompt.ask("Ingrese la identificación del paciente")
            nombre = Prompt.ask("Ingrese el nombre del paciente")
            celular = Prompt.ask("Ingrese el celular del paciente")
            correo = Prompt.ask("Ingrese el correo del paciente")
            paciente = Paciente(identificacion, nombre, celular, correo)
            hospital.agregar_paciente(paciente)

        elif opcion == "2":
            identificacion = Prompt.ask("Ingrese la identificación del médico")
            nombre = Prompt.ask("Ingrese el nombre del médico")
            celular = Prompt.ask("Ingrese el celular del médico")
            especialidad = Prompt.ask("Ingrese la especialidad del médico")
            medico = Medico(identificacion, nombre, celular, especialidad)
            hospital.agregar_medico(medico)

        elif opcion == "3":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                especialidad = Prompt.ask("Ingrese la especialidad requerida")
                medicos_disponibles = hospital.buscar_medicos_por_especialidad(
                    especialidad
                )
                if medicos_disponibles:
                    print("Médicos disponibles:")
                    for i, medico in enumerate(medicos_disponibles, 1):
                        print(f"{i}. Dr. {medico.nombre}")
                    medico_index = (
                        int(Prompt.ask("Seleccione el número del médico")) - 1
                    )
                    medico = medicos_disponibles[medico_index]
                    fecha = Prompt.ask("Ingrese la fecha de la cita (YYYY-MM-DD)")
                    hora = Prompt.ask("Ingrese la hora de la cita (HH:MM)")
                    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                    cita = Cita(paciente, medico, fecha_hora)
                    hospital.agenda.agendar_cita(cita)
                else:
                    print(
                        f"No hay médicos disponibles para la especialidad {especialidad}"
                    )
            else:
                print("Paciente no encontrado")

        elif opcion == "4":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(Prompt.ask("Seleccione el número de la cita a cancelar"))
                        - 1
                    )
                    cita = citas_paciente[cita_index]
                    motivo = Prompt.ask("Ingrese el motivo de la cancelación")
                    hospital.agenda.cancelar_cita(cita, motivo)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado")

        elif opcion == "5":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(Prompt.ask("Seleccione el número de la cita a mover")) - 1
                    )
                    cita = citas_paciente[cita_index]
                    nueva_fecha = Prompt.ask(
                        "Ingrese la nueva fecha de la cita (YYYY-MM-DD)"
                    )
                    nueva_hora = Prompt.ask("Ingrese la nueva hora de la cita (HH:MM)")
                    nueva_fecha_hora = datetime.strptime(
                        f"{nueva_fecha} {nueva_hora}", "%Y-%m-%d %H:%M"
                    )
                    hospital.agenda.mover_cita(cita, nueva_fecha_hora)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado")

        elif opcion == "6":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for cita in citas_paciente:
                        print(cita)
                else:
                    print("El paciente no tiene citas programadas")
            else:
                print("Paciente no encontrado.")

        elif opcion == "7":
            medico_id = Prompt.ask("Ingrese la identificación del médico")
            medico = hospital.buscar_medico(medico_id)
            if medico:
                citas_medico = hospital.agenda.buscar_citas_medico(medico)
                if citas_medico:
                    print("Citas del médico:")
                    for cita in citas_medico:
                        print(cita)
                else:
                    print("El médico no tiene citas programadas")
            else:
                print("Médico no encontrado")

        elif opcion == "8":
            mostrar_lista_citas(hospital)

        elif opcion == "9":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                table = Table(
                    title="[bold white]PACIENTE ENCONTRADO EN EL HOSPITAL[/bold white]"
                )
                table.add_column("ID", style="cyan")
                table.add_column("NOMBRE COMPLETO", style="magenta")
                table.add_column("CELULAR", style="green")
                table.add_column("CORREO ELECTRÓNICO", style="yellow")

                table.add_row(
                    paciente.identificacion,
                    paciente.nombre,
                    paciente.celular,
                    paciente.correo,
                )

                console.print(table)
            else:
                print("Paciente no encontrado.")

        elif opcion == "10":
            medico_id = Prompt.ask("Ingrese la identificación del médico")
            medico = hospital.buscar_medico(medico_id)
            if medico:
                table = Table(
                    title="[bold white]MÉDICO ENCONTRADO EN EL HOSPITAL[/bold white]"
                )
                table.add_column("ID", style="cyan")
                table.add_column("NOMBRE COMPLETO", style="magenta")
                table.add_column("ESPECIALIDAD", style="green")
                table.add_column("CELULAR", style="yellow")

                table.add_row(
                    medico.identificacion,
                    medico.nombre,
                    medico.especialidad,
                    medico.celular,
                )

                console.print(table)
            else:
                print("Médico no encontrado.")

        elif opcion == "11":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                especialidad = Prompt.ask(
                    "Ingrese la especialidad requerida para la urgencia"
                )
                medicos_disponibles = hospital.buscar_medicos_por_especialidad(
                    especialidad
                )
                if medicos_disponibles:
                    print("Médicos disponibles:")
                    for i, medico in enumerate(medicos_disponibles, 1):
                        print(f"{i}. Dr. {medico.nombre}")
                    medico_index = (
                        int(Prompt.ask("Seleccione el número del médico")) - 1
                    )
                    medico = medicos_disponibles[medico_index]
                    fecha = Prompt.ask(
                        "Ingrese la fecha de la cita urgente (YYYY-MM-DD)"
                    )
                    hora = Prompt.ask("Ingrese la hora de la cita urgente (HH:MM)")
                    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
                    try:
                        hospital.agendar_cita_urgente(paciente, medico, fecha_hora)
                    except ValueError as e:
                        console.print(
                            f"[red]Error al agendar cita urgente: {str(e)}[/red]"
                        )
                else:
                    print(
                        f"No hay médicos disponibles para la especialidad {especialidad}"
                    )
            else:
                print("Paciente no encontrado")

        elif opcion == "12":
            paciente_id = Prompt.ask("Ingrese la identificación del paciente")
            paciente = hospital.buscar_paciente(paciente_id)
            if paciente:
                citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
                if citas_paciente:
                    print("Citas del paciente:")
                    for i, cita in enumerate(citas_paciente, 1):
                        print(f"{i}. {cita}")
                    cita_index = (
                        int(
                            Prompt.ask(
                                "Seleccione el número de la cita para agregar feedback"
                            )
                        )
                        - 1
                    )
                    cita = citas_paciente[cita_index]
                    calificacion = float(Prompt.ask("Ingrese la calificación (0-5)"))
                    comentario = Prompt.ask("Ingrese un comentario sobre la cita")
                    hospital.agregar_feedback_cita(cita, calificacion, comentario)
                else:
                    print("El paciente no tiene citas para calificar")
            else:
                print("Paciente no encontrado")

        elif opcion == "13":
            table = Table(
                title="[bold white]CALIFICACIÓN PROMEDIO POR MÉDICO[/bold white]"
            )
            table.add_column("Nombre del Médico", style="cyan")
            table.add_column("Especialidad", style="magenta")
            table.add_column("Calificación Promedio", style="yellow")

            for medico in hospital.medicos:
                calificacion_promedio = round(medico.calificacion_promedio(), 2)
                table.add_row(
                    medico.nombre, medico.especialidad, str(calificacion_promedio)
                )

            console.print(table)

        elif opcion == "14":
            print("Gracias por usar el Sistema de Citas Médicas. ¡Hasta luego!")
            break

        console.print("\nPresione Enter para continuar...")
        input()


if __name__ == "__main__":
    main()
