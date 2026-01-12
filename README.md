# Server Monitor
[![de](https://img.shields.io/badge/lang-de-yello)](https://github.com/SoulofSorrow/ark-server-monitor/blob/main/README.de.md)

This script monitors the status of ARK servers and notifies via email when the status changes.

## Features

- Monitors the online status of ARK servers.
- Regularly checks the status at configurable intervals.
- Sends email notifications on status changes.
- Supports RCON for server status verification.
- Configuration through a `config.yaml` file.

## Requirements

- Python 3.x
- `pythonping` library for ping check.
- `pyyaml` library for processing the configuration file.
- `smtplib` library for sending emails.

## Usage

1. Install the required dependencies:

```shell
pip install pythonping pyyaml
```

2. Customize the config.yaml configuration file and specify the ARK servers to monitor.

3. Run the script:

```shell
python server_monitor.py
```

4. The script will now monitor the configured ARK servers and send email notifications on status changes.

## Configuration

Configuration is done through the config.yaml file. Here are some important configuration options:

- `servers`: A list of ARK servers to monitor. Each server is configured with a name, IP address, port, and RCON password.
- `email`: Email configuration for sending notifications. Configure the SMTP server, sender, recipient, and credentials.

## Autoren

- [SoulofSorrow](https://github.com/SoulofSorrow)