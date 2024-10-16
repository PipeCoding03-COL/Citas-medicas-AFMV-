# MEJORAS

A continuación, una explicación detallada de cada una de las modificaciones (mejoras) solicitadas.

## Modificaciones solicitadas

1. Corregir las notificaciones:
   - Se añadió una clase base `Notificacion` con un método `enviar_notificacion`.
   - Se crearon las subclases `Correo`, `Celular`, y `Whatsapp`, todas heredando de `Notificacion`.
   - Se quitaron todos los atributos referentes a las notificaciones de la clase `Notificacion` y se pasaron a la clase `Persona`, ya que Los datos de correo, celular, etc. pertenecen a la persona no a la notificación
   - Cada subclase sobreescribe el método `enviar_notificacion`.

2. Se agregó WhatsApp como una forma de notificación:
   - Ha sido creada la clase `Whatsapp`, la cual hereda de `Notificacion`.
   - También se le implementó su método `enviar_notificacion` para mensajes de WhatsApp.

3. Ha sido corregida la relación Agenda - Cita:
   - Se movió la clase `Agenda` como un atributo de la clase `Hospital`.
   - La clase `Hospital` ahora tiene un atributo `agenda` que maneja todas las citas.

4. Han sido corregidos todos los usuarios, pues no hay usuarios sino que hay pacientes:
   - Todas las partes donde se hacía referencia a los pacientes como "usuarios" fueron reemplazadas por "pacientes".
   - La clase `Hospital` también fue modificada para tener una lista de `pacientes` en lugar de `usuarios`.

5. Se crearon los métodos `buscar_paciente()` y `buscar_medico()` en la clase `Hospital`:
   - El método `buscar_paciente(identificacion)` fue añadido a la clase `Hospital`.
   - El método `buscar_medico(identificacion)` fue añadido a la clase `Hospital`.
   - Los métodos mencionados previamente preguntan el número de cédula del paciente o médico y retornan toda su respectiva información.

6. Agendar y cancelar cita fueron corregidos, ya que no deben ir en el paciente sino donde tengan la agenda:
   - Se movieron los métodos `agendar_cita()` y `cancelar_cita()` de la clase `Paciente` a la clase `Agenda`.
   - La clase `main` fue modificada para que dichos métodos sean llamados a través del atributo `agenda` de la clase `Hospital`.

7. Búsqueda de la información de una cita:
   - Fueron añadidos los métodos `buscar_citas_paciente(paciente)` y `buscar_citas_medico(medico)` a la clase `Agenda`.
   - Estos métodos retornan toda la información de las citas correspondientes.

8. Solución para el método `mover_cita()`:
   - El método `mover_cita(cita, nueva_fecha_hora)` fue añadido a la clase `Agenda`.
   - Este método permite que los pacientes puedan reagendar cada una de sus citas.

9. Mejora significativa de la interfaz de texto usando la librería Rich:
   - Se importó y también se usó dicha librería con el fin de crear paneles y tablas a través de los cuales se busca mostrar la información de una manera más visual y organizada.
   - Ha sido creada una función `mostrar_menu()` para mostrar el menú con una tabla hecha con ayuda de la librería Rich.
   - También se empleó la librería para usar el método `console.print()`, el cual ayuda a imprimir por consola una variedad enorme de fuentes, estilos y colores.

10. Carga de los datos iniciales desde archivos CSV y JSON:
    - Se creó el método `cargar_datos_iniciales()`, la cual lee los datos iniciales desde los archivos 'pacientes.csv', 'medicos.json', and 'citas.csv', y luego los carga al sistema.
    - También fue ideado un sistema que detecta y muestra la razón de los errores que puedan causar estos archivos.

11. Se usaron las clases `date` y `time` para la programación de las citas:
    - La clase `Cita` fue modificada para ahora usar un objeto de tipo `datetime` para `fecha_hora`, en vez de ser solamente `DATE`.

12. Muestra de la lista de médicos por especialidad a la hora de agendar citas:
    - Fue añadido el método `buscar_medicos_por_especialidad(especialidad)` a la clase `Hospital`.
    - Ahora, cada que se va a agendar una nueva cita, primero se pregunta por la especialidad requerida y luego, muestra una lista de médicos disponibles de esa especialidad seleccionada.

13. Se añadieron las opciones para poder ver las listas de pacientes, médicos y citas:
    - Se crearon los métodos `mostrar_lista_pacientes()`, `mostrar_lista_medicos()`, y `mostrar_lista_citas()`.
    - Cada método usa Rich para mostrar las tablas de una manera más bonita.

Estos cambios dieron como resultado un sistema de citas médicas más robusto, fácil de usar y con todas las características. El código ahora está mejor organizado, con una clara separación de responsabilidades entre las diferentes clases y funcionalidades. El uso de la biblioteca Rich ha mejorado significativamente la interfaz de usuario, haciéndola más legible y atractiva visualmente.

## Mejoras propias (añadidas por mí)

1. Se añadió la opción de que los pacientes puedan pedir citas por URGENCIAS: La gestión de urgencias permite priorizar citas urgentes sobre las regulares, lo cual es crucial en un entorno médico.La gestión de urgencias permite priorizar citas urgentes sobre las regulares, lo cual es crucial en un entorno médico.
    - Fue creada la clase `CitaUrgente`, la cual hereda de `Cita`.
    - Se modificó el método `agendar_cita` de la clase `Agenda` para manejar las citas urgentes.
    - Se agregó una nueva opción en el menú principal para agendar citas urgentes.

2. Fue añadido un sistema de feedback y calificaciones, el cual proporciona una forma de evaluar la calidad del servicio y la satisfacción del paciente, lo que puede ser útil para mejorar la atención médica.
    - Se agregaron los atributos `calificacion` y `comentario` a la clase `Cita`.
    - Se implementó el método `agregar_feedback` en la clase `Cita`.
    - Se agregó el atributo `calificaciones` y el método `calificacion_promedio` a la clase `Medico`.
    - Se agregaron dos nuevas opciones en el menú principal: Una para agregar feedback a una cita y otra para ver las calificaciones de los médicos.

Estos cambios permiten al sistema manejar citas urgentes, dando prioridad sobre las citas regulares, y también permiten a los pacientes proporcionar feedback y calificaciones para sus citas, que luego se pueden ver como un promedio para cada médico.