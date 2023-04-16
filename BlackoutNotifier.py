import os
import time
import datetime
import requests

PUSHBULLET_API_KEY = "API-KEY"
PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"
PUSHBULLET_TITLE = "Apagón detectado"

def send_pushbullet_notification(PUSHBULLET_BODY):
    PUSHBULLET_HEADERS = {
        "Authorization": "Bearer " + PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "type": "note",
        "title": PUSHBULLET_TITLE,
        "body": PUSHBULLET_BODY
    }
    requests.post(PUSHBULLET_URL, headers=PUSHBULLET_HEADERS, json=data)

def get_system_boot_time():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    boot_time_seconds = time.time() - uptime_seconds
    return datetime.datetime.fromtimestamp(boot_time_seconds)

def get_last_boot_time():
    try:
        with open('/home/alex/boot-time.txt', 'r') as f:
            last_boot_time_str = f.read().strip()
            last_boot_time = datetime.datetime.strptime(last_boot_time_str, '%Y-%m-%d %H:%M:%S')
    except (FileNotFoundError, ValueError):
        last_boot_time = get_system_boot_time()
    return last_boot_time

def write_boot_time():
    with open('/home/alex/boot-time.txt', 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def wait_for_internet_connection():
    while True:
        try:
            requests.get("http://www.google.com", timeout=5)
            break
        except:
            time.sleep(5)

if __name__ == "__main__":
    counter = 0  # inicializa el contador
    while counter < 2:  # solo se ejecuta 2 veces
        wait_for_internet_connection()
        last_boot_time = get_last_boot_time()
        current_time = datetime.datetime.now()
        downtime_seconds = (current_time - last_boot_time).total_seconds()
        elapsed_seconds = downtime_seconds
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        PUSHBULLET_BODY = "El sistema estuvo apagado durante {} horas, {} minutos y {} segundos.".format(int(hours), int(minutes), int(seconds))
        if downtime_seconds > 0:
            send_pushbullet_notification(PUSHBULLET_BODY)
            counter += 1  # incrementa el contador
            time.sleep(60)
            send_pushbullet_notification(PUSHBULLET_BODY)
            counter += 1  # incrementa el contador
        time.sleep(60)

    while True:
        write_boot_time()
        time.sleep(60)
