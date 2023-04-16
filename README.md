# BlackoutNotifier
# Readme del código 

Este código se encarga de detectar cuánto tiempo ha estado apagado el sistema y envía una notificación a través de la aplicación Pushbullet. También escribe la hora de inicio del sistema en un archivo llamado `boot-time.txt` en el directorio `/home/alex`. 

## Dependencias
El código requiere de los siguientes módulos de Python:

- `os`
- `time`
- `datetime`
- `requests`

## Variables
- `PUSHBULLET_API_KEY`: Clave de API de Pushbullet. Esta clave es necesaria para enviar notificaciones a través de la API de Pushbullet.
- `PUSHBULLET_URL`: URL de la API de Pushbullet.
- `PUSHBULLET_TITLE`: Título de la notificación que se enviará a través de la API de Pushbullet.
- `PUSHBULLET_BODY`: Cuerpo del mensaje que se enviará a través de la API de Pushbullet.

## Funciones
- `send_pushbullet_notification(PUSHBULLET_BODY)`: Esta función toma el cuerpo del mensaje y lo envía a través de la API de Pushbullet. Utiliza la clave de API y la URL definidas en las variables para enviar la notificación.
- `get_system_boot_time()`: Esta función obtiene la hora de inicio del sistema utilizando el archivo `/proc/uptime`.
- `get_last_boot_time()`: Esta función obtiene la última hora de inicio del sistema almacenada en el archivo `/home/alex/boot-time.txt`. Si el archivo no existe o no puede ser leído, la función llama a `get_system_boot_time()` para obtener la hora de inicio del sistema actual.
- `write_boot_time()`: Esta función escribe la hora de inicio del sistema actual en el archivo `/home/alex/boot-time.txt`.
- `wait_for_internet_connection()`: Esta función comprueba la conexión a Internet esperando a que se pueda conectar con Google durante 5 segundos.

## Lógica de ejecución
El código se divide en dos bucles `while`.

El primer bucle se ejecuta dos veces y comprueba si ha habido un apagón del sistema. Si ha habido un apagón, envía una notificación a través de la API de Pushbullet con el tiempo que ha estado apagado el sistema. Después de enviar la notificación, el contador se incrementa en uno y se espera 60 segundos antes de enviar otra notificación. Esto se hace dos veces para enviar dos notificaciones.

El segundo bucle se ejecuta continuamente y escribe la hora de inicio del sistema actual en el archivo `/home/alex/boot-time.txt` cada 60 segundos.

Lo ideal es ponerlo en el cron y que solo se inicie una vez al bootea.
