import socket
import time
import datetime
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def load_config():
    # Lade die Konfigurationsdaten aus der YAML-Datei
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_previous_status():
    previous_status = None

    if os.path.isfile('config/previous_status.yaml'):
        with open('config/previous_status.yaml', 'r') as file:
            previous_status = yaml.safe_load(file)

    return previous_status

def save_previous_status(previous_status):
    with open('config/previous_status.yaml', 'w') as file:
        yaml.safe_dump(previous_status, file)

def check_server_status(server_config, email_config, previous_status):
    try:
        # Socket-Verbindung zum ARK-Server herstellen
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((server_config['server_ip'], server_config['port']))
            except ConnectionRefusedError:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"Verbindung zum Server abgelehnt: {server_config['name']} - IP: {server_config['server_ip']}"
                print(f"[{timestamp}] {message}")
                current_status = "offline"
            else:
                # RCON-Befehl senden, um den Serverstatus abzurufen
                rcon_message = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0x02]) + server_config['rcon_password'].encode() + b'\x00listplayers'
                sock.send(rcon_message)

                response = sock.recv(4096).decode('utf-8')

                # Zeit- und Datumsstempel generieren
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Serverantwort verarbeiten
                # Hier kannst du deine eigene Logik implementieren, um den Status zu überprüfen
                # Zum Beispiel kannst du nach bestimmten Spielern suchen oder prüfen, ob der Server voll ist, etc.

                message = f"Server: {server_config['name']} - IP: {server_config['server_ip']} - Online! PlayerList: {response}"
                print(f"[{timestamp}] {message}")

                current_status = response

            # Serverstatus prüfen
            if previous_status.get(server_config['name']) != current_status:
                # Serverstatus hat sich geändert
                if current_status == "offline":
                    # Server ist offline, sende eine E-Mail
                    send_email(server_config, current_status, email_config)
                elif previous_status.get(server_config['name']) == "offline":
                    # Server ist nicht mehr offline, sende eine Benachrichtigung
                    send_email(server_config, "online", email_config)

                previous_status[server_config['name']] = current_status

            return current_status

    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Fehler beim Verbinden mit Server: {server_config['name']} - IP: {server_config['server_ip']}. {e}"
        print(f"[{timestamp}] {message}")
        return "offline"

def send_email(server_config, server_response, email_config):
    if server_response == "offline":
        email_subject = f"ARK Server Status - {server_config['name']} (offline)"
        email_body = f"Der Server {server_config['name']} ({server_config['server_ip']}) ist offline."
    else:
        email_subject = f"ARK Server Status - {server_config['name']} (online)"
        email_body = f"Der Server {server_config['name']} ({server_config['server_ip']}) ist online! Playerlist: {server_response}"

    # E-Mail-Konfiguration laden
    smtp_host = email_config.get('host')
    smtp_port = email_config.get('port', 587)
    sender_email = email_config.get('username')
    sender_password = email_config.get('password')
    recipient_email = email_config.get('to')

    # E-Mail zusammenstellen
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_email)
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body, 'plain'))

    # Verbindung zum SMTP-Server herstellen und E-Mail senden
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if email_config.get('use_starttls', False):
            server.starttls()
        if email_config.get('use_auth', False):
            server.login(sender_email, sender_password)
        server.send_message(msg)

    print(f"E-Mail an {', '.join(recipient_email)} gesendet")

def check_all_servers():
    # Lade die Konfigurationsdaten
    config = load_config()

    # Lade die E-Mail-Konfiguration
    email_config = config.get('email', {})

    # Vorherigen Serverstatus laden
    previous_status = load_previous_status()
    if previous_status is None:
        previous_status = {}

    # Überprüfe jeden Server in der Konfiguration
    for server_config in config.get('servers', []):
        server_status = check_server_status(server_config, email_config, previous_status)
        previous_status[server_config['name']] = server_status

    # Aktualisierten Serverstatus speichern
    save_previous_status(previous_status)

    interval_seconds = config.get('interval_seconds', 60)  # Standard-Intervall: 60 Sekunden
    time.sleep(interval_seconds)

def main():
    try:
        while True:
            check_all_servers()
    except KeyboardInterrupt:
        print("\nDas Skript wurde manuell unterbrochen.")

if __name__ == "__main__":
    main()
