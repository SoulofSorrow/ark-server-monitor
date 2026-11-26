# Architecture

## Files

| Path | Purpose |
| --- | --- |
| `server_monitor.py` | Whole application |
| `config/config.yaml` | Configuration (template with placeholders in the repository) |
| `config/previous_status.yaml` | Last status per server name, written by the script |
| `requirements.txt` | `PyYAML` |
| `dockerfile`, `docker-compose.yaml` | Container build and run, see `docs/deployment.md` |
| `Makefile` | Repository setup helpers only, no build/test targets |

## Functions (`server_monitor.py`)

| Function | Behaviour |
| --- | --- |
| `main()` | Endless loop over `check_all_servers()`; exits on `KeyboardInterrupt` |
| `check_all_servers()` | `load_config()`, `load_previous_status()`, `check_server_status()` per entry in `servers`, `save_previous_status()`, then `time.sleep(interval_seconds)` (default 60) |
| `load_config()` | `yaml.safe_load` of `config/config.yaml` (relative to CWD) |
| `load_previous_status()` / `save_previous_status()` | Read/write `config/previous_status.yaml` |
| `check_server_status(server_config, email_config, previous_status)` | TCP connect to `server_ip:port`; on success sends a byte message containing `rcon_password` and `listplayers`, reads up to 4096 bytes; returns `"offline"` or the raw response string |
| `send_email(server_config, server_response, email_config)` | Builds a German subject/body and sends via `smtplib.SMTP`, optional STARTTLS and login |

## Status and notification logic

1. Status per server is `"offline"` or the decoded response text.
2. Connection refused, or any exception: status `"offline"` (exceptions are
   caught in `check_server_status`, printed, and `"offline"` returned).
3. If the status differs from `previous_status[name]`:
   - new status `"offline"`: e-mail "offline";
   - previous status `"offline"`: e-mail "online" with the response text;
   - otherwise (response text changed while online): no e-mail.
4. The status map is persisted after every pass.

## Output

- Console only (`print` with `[YYYY-mm-dd HH:MM:SS]` prefix). No log file is
  written, although `config/config.yaml` contains `log_file` and
  `log_backup_count`.

## Invariants

- Server identity is the `name` field; renaming a server resets its status
  history.
- The message sent on the TCP connection is not the Source RCON packet format;
  see Follow-ups in `docs/changes/2026-11-25-ai-ready-docs.md`.
