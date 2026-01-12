# Server Monitor
[![en](https://img.shields.io/badge/lang-en-red)](https://github.com/SoulofSorrow/ark-server-monitor/blob/main/README.md)


Dieses Skript überwacht den Status von ARK-Servern und benachrichtigt per E-Mail, wenn der Status geändert wird.

## Funktionen

- Überwacht den Online-Status von ARK-Servern
- Prüft den Status regelmäßig in konfigurierbaren Intervallen
- Sendet E-Mail-Benachrichtigungen bei Statusänderungen
- Unterstützt RCON zur Überprüfung des Serverstatus
- Konfiguration über eine `config.yaml`-Datei

## Anforderungen

- Python 3.x
- `pythonping`-Bibliothek für den Ping-Check
- `pyyaml`-Bibliothek für die Verarbeitung der Konfigurationsdatei
- `smtplib`-Bibliothek für das Senden von E-Mails

## Verwendung

1. Installiere die erforderlichen Abhängigkeiten:

```shell
pip install pythonping pyyaml
```

2. Passe die Konfigurationsdatei `config.yaml` an und lege die ARK-Server fest, die überwacht werden sollen.

3. Führe das Skript aus:

```shell
python server_monitor.py
```

4. Das Skript überwacht nun die konfigurierten ARK-Server und sendet E-Mail-Benachrichtigungen bei Statusänderungen.

## Konfiguration

Die Konfiguration erfolgt über die `config.yaml`-Datei. Hier sind einige wichtige Konfigurationsoptionen:

- `servers`: Eine Liste von ARK-Servern, die überwacht werden sollen. Jeder Server wird mit Namen, IP-Adresse, Port und RCON-Passwort konfiguriert.
- `email`: E-Mail-Konfiguration für das Senden von Benachrichtigungen. Konfiguriere den SMTP-Server, Absender, Empfänger und Anmeldeinformationen.

## Autoren

- [SoulofSorrow](https://github.com/SoulofSorrow)
