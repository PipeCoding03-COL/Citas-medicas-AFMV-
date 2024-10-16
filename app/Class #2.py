#Clase AGENDA
class Agenda:
    def __init__(self):
        self.historico_citas = []
        self.citas_pendientes = []
        self.citas_realizadas = []

    def agregar_cita(self, cita):
        self.citas_pendientes.append(cita)
        print(
            f"Cita agregada para el {cita.fecha} con el Dr. {cita.medico.nombre}")

    def cancelar_y_mover_cita(self, cita):
        self.citas_pendientes.remove(cita)
        print(
            f"La cita del {cita.fecha} ha sido cancelada y movida a otro día.")

    def finalizar_cita(self, cita):
        self.citas_pendientes.remove(cita)
        self.citas_realizadas.append(cita)
        print(
            f"Cita con el Dr. {cita.medico.nombre} el {cita.fecha} ha sido completada")

#Clase APLICACIÓN
class Aplicacion:
    def enviar_notificacion(self):
        print("Enviando notificación en la aplicación.")

#clase CELULAR
class Celular:
    def verificar_celular(self, numero_celular):
        print(f"Enviando mensaje de verificación a {numero_celular}")

    def enviar_mensaje(self, numero_celular, mensaje):
        print(
            f"Enviando mensaje de texto para {numero_celular}, con contenido: {mensaje}")

    def realizar_llamada(self, numero_celular):
        print(f"Realizando llamada telefónica a {numero_celular}")

#Clase CITA
class Cita:
    def __init__(self, paciente, medico, fecha):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.motivo_cancelacion = None

    def recordatorio_cita(self):
        print(f"Enviando notificación al paciente {self.paciente.nombre}")

    def reprogramar_cita(self, nueva_fecha):
        if self.medico.verificar_disponibilidad(nueva_fecha):
            print(f"Cita reprogramada del {self.fecha} al {nueva_fecha}")
            self.fecha = nueva_fecha
        else:
            print(
                f"No hay disponibilidad para reprogramar la cita en la fecha {nueva_fecha}")

    def cancelar_cita(self, motivo):
        self.motivo_cancelacion = motivo
        print(
            f"La cita ha sido cancelada por {self.paciente.nombre}, debido a: {self.motivo_cancelacion}")

    def __repr__(self):
        # return f"Cita programada para el {self.fecha}" -> return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha}"
        return f"Cita del paciente {self.paciente.nombre} con el Dr. {self.medico.nombre} programada para el {self.fecha}"

#Clase CORREO
class Correo:
    def verificar_correo(self, correo):
        print(f"Enviando correo de verificación a {correo}")

    def enviar_correo(self, para, asunto):
        print(f"Enviando correo a {para} con asunto: {asunto}")

#Clase HOSPITAL
class Hospital:
    __instance = None

    def get_instance(self):
        if Hospital.__instance is None:
            Hospital()
        return Hospital.__instance

    def __init__(self):
        self.usuarios = []
        self.medicos = []

    def agregar_paciente(self, paciente):
        self.usuarios.append(paciente)
        print(f"Paciente {paciente.nombre} agregado al hospital.")

    def agregar_medico(self, medico):
        self.medicos.append(medico)
        print(f"Médico {medico.nombre} agregado al hospital.")

    def verificar_disponibilidad(self, paciente, especialidad):
        for medico in self.medicos:
            if medico.especialidad == especialidad:
                if medico.verificar_disponibilidad(paciente.agenda.fecha):
                    return medico
        print(
            f"No se encontró disponibilidad para la especialidad {especialidad}.")

#Clase PERSONA
class Persona:
    def __init__(self, identificacion, nombre, celular):
        self.identificacion = identificacion
        self.nombre = nombre
        self.celular = celular

#Clase MÉDICO
##from persona import Persona
##from agenda import Agenda

class Medico(Persona):
    def __init__(self, identificacion, nombre, celular, especialidad):
        super().__init__(identificacion, nombre, celular)
        self.especialidad = especialidad
        self.agenda = Agenda()

    def verificar_disponibilidad(self, fecha):
        # Verifica si tiene citas pendientes en la fecha dada
        return fecha not in self.agenda.citas_pendientes

#Clase NOTIFIACIÓN
##from aplicacion import Aplicacion
##from celular import Celular
##from correo import Correo


class Notificacion:
    def __init__(self):
        self.correo = Correo()
        self.celular = Celular()
        self.aplicacion = Aplicacion()

    def enviar_notificacion(self):
        return self.aplicacion.enviar_notificacion()

    def verificar_correo(self):
        print(f"Verificando correo {self.correo}")

#Clase PACIENTE
##from persona import Persona
##from agenda import Agenda
##from cita import Cita


class Paciente(Persona):
    def __init__(self, identificacion, nombre, celular, correo):
        super().__init__(identificacion, nombre, celular)
        self.correo = correo
        self.medico_preferencia = None
        self.agenda = Agenda()  # Agenda del paciente

    def pedir_cita(self, medico, fecha, motivo):
        # Verificar si el médico tiene disponibilidad
        if medico.verificar_disponibilidad(fecha):
            # Cita(medico, fecha, motivo) -> Cita(self, medico, fecha)
            nueva_cita = Cita(self, medico, fecha)
            medico.agenda.agregar_cita(nueva_cita)
            self.agenda.agregar_cita(nueva_cita)
            # print(f"Cita solicitada para el paciente {self.nombre} con el Dr. {medico.nombre}")
        else:
            print(
                f"No hay disponibilidad con el Dr. {medico.nombre} en la fecha {fecha}")

    def cancelar_cita(self, cita):
        # Cancelar la cita y notificar tanto al médico como al paciente
        cita.cancelar_cita()
        print(f"Cita cancelada por el paciente {self.nombre}")

    def asignar_medico_preferencia(self, medico):
        self.medico_preferencia = medico
        print(
            f"El médico {medico.nombre} ha sido asignado como preferencia para el paciente {self.nombre}")

#Clase PERSONA FACTORY
##from paciente import Paciente
##from medico import Medico


class PersonasFactory:
    @staticmethod
    def crear_persona(tipo, identificacion, nombre, celular, especialidad=None, correo=None):
        if tipo.lower() == 'medico':
            return Medico(identificacion, nombre, celular, especialidad)

        elif tipo.lower() == 'paciente':
            return Paciente(identificacion, nombre, celular, correo)

        else:
            raise ValueError(f"Tipo de persona desconocido: {tipo}")

#Clase REPORTE
class Reporte:
    def __init__(self, tipo_reporte, fecha_inicio, fecha_fin):
        self.tipo_reporte = tipo_reporte
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def generar_reporte(self):
        pass

    def exportar_Excel(self):
        print(f"Exportando reporte {self.tipo_reporte} a Excel")


class ReporteDemanda(Reporte):
    def __init__(self, tipo_reporte, fecha_inicio, fecha_fin, medico):
        super().__init__(tipo_reporte, fecha_inicio, fecha_fin)
        self.medico = medico

    def generar_reporte(self):
        print(f"Generando reporte de demanda para el Dr. {self.medico.nombre}")


class ReporteTendencias(Reporte):
    def __init__(self, tipo_reporte, fecha_inicio, fecha_fin, citas_agendadas):
        super().__init__(tipo_reporte, fecha_inicio, fecha_fin)
        self.citas_agendadas = citas_agendadas

    def generar_reporte(self):
        print("Generando reporte de tendencias...")


class ReporteCancelaciones(Reporte):
    def __init__(self, tipo_reporte, fecha_inicio, fecha_fin, motivo_cancelacion):
        super().__init__(tipo_reporte, fecha_inicio, fecha_fin)
        self.motivo_cancelacion = motivo_cancelacion

    def generar_reporte(self):
        print(
            f"Generando reporte de cancelaciones por motivo: {self.motivo_cancelacion}")


class ReporteAusentismo(Reporte):
    def __init__(self, tipo_reporte, fecha_inicio, fecha_fin, citas_ausentes):
        super().__init__(tipo_reporte, fecha_inicio, fecha_fin)
        self.citas_ausentes = citas_ausentes

    def generar_reporte(self):
        print("Generando reporte de ausentismo...")

#CLASE MAIN
##from hospital import Hospital
##from persona_factory import PersonasFactory

hospital = Hospital()

while True:
    print("\n--- Menú ---")
    print("1. Agregar persona")
    print("2. Pedir cita")
    print("3. Cancelar cita")
    print("4. Asignar médico de preferencia")
    print("5. Ver citas pendientes")
    print("6. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        tipo_persona = input(
            "Ingrese el tipo de persona (médico o paciente): ")
        identificacion = input("Ingrese la identificación: ")
        nombre = input("Ingrese el nombre: ")
        celular = input("Ingrese el celular: ")

        if tipo_persona.lower() == "medico":
            especialidad = input("Ingrese la especialidad: ")
            persona = PersonasFactory.crear_persona(
                "medico", identificacion, nombre, celular, especialidad)
            hospital.agregar_medico(persona)
        elif tipo_persona.lower() == "paciente":
            correo = input("Ingrese el correo: ")
            persona = PersonasFactory.crear_persona(
                "paciente", identificacion, nombre, celular, correo=correo)
            hospital.agregar_paciente(persona)
        else:
            print("Tipo de persona inválido.")

    elif opcion == "2":
        id_paciente = input("Ingrese la identificación del paciente: ")
        id_medico = input("Ingrese la identificación del médico: ")
        fecha = input("Ingrese la fecha de la cita (YYYY-MM-DD): ")
        motivo = input("Ingrese el motivo de la cita: ")

        paciente = next(
            (p for p in hospital.usuarios if p.identificacion == id_paciente), None)
        medico = next(
            (m for m in hospital.medicos if m.identificacion == id_medico), None)

        if paciente and medico:
            paciente.pedir_cita(medico, fecha, motivo)
        else:
            print("Paciente o médico no encontrado.")

    elif opcion == "3":
        id_paciente = int(input("Ingrese la identificación del paciente: "))
        paciente = next(
            (p for p in hospital.usuarios if p.identificacion == id_paciente), None)

        if paciente:
            print("Citas pendientes:")
            for i, cita in enumerate(paciente.agenda.citas_pendientes):
                print(f"{i+1}. {cita}")

            opcion_cita = int(input("Seleccione la cita a cancelar: "))
            if 1 <= opcion_cita <= len(paciente.agenda.citas_pendientes):
                cita_a_cancelar = paciente.agenda.citas_pendientes[opcion_cita - 1]
                paciente.cancelar_cita(cita_a_cancelar)
            else:
                print("Opción inválida.")
        else:
            print("Paciente no encontrado.")

    elif opcion == "4":
        id_paciente = int(input("Ingrese la identificación del paciente: "))
        id_medico = int(input("Ingrese la identificación del médico: "))

        paciente = next(
            (p for p in hospital.usuarios if p.identificacion == id_paciente), None)
        medico = next(
            (m for m in hospital.medicos if m.identificacion == id_medico), None)

        if paciente and medico:
            paciente.asignar_medico_preferencia(medico)
        else:
            print("Paciente o médico no encontrado.")

    elif opcion == "5":
        id_paciente = int(input("Ingrese la identificación del paciente: "))
        paciente = next(
            (p for p in hospital.usuarios if p.identificacion == id_paciente), None)

        if paciente:
            print("Citas pendientes:")
            for cita in paciente.agenda.citas_pendientes:
                print(cita)
        else:
            print("Paciente no encontrado.")

    elif opcion == "6":
        print("Saliendo del programa...")
        break

    else:
        print("Opción inválida.")