# Configuration

Single file `config/config.yaml`, read on every pass by `load_config()`.
The committed file is a template with placeholders; real values (SMTP
password, RCON passwords, IPs, e-mail addresses) must not be committed.

## Keys read by the code

| Key | Default in code | Used in |
| --- | --- | --- |
| `servers` | `[]` | List of servers to check |
| `servers[].name` | none (required) | Status key and e-mail text |
| `servers[].server_ip` | none (required) | TCP target |
| `servers[].port` | none (required) | TCP target port |
| `servers[].rcon_password` | none (required) | Sent in the status request |
| `interval_seconds` | `60` | Sleep between passes |
| `email.host` | none | SMTP host |
| `email.port` | `587` | SMTP port |
| `email.username` | none | SMTP login and `From` header |
| `email.password` | none | SMTP login |
| `email.to` | none | List of recipients (joined with `, `) |
| `email.use_starttls` | `false` | Call `starttls()` |
| `email.use_auth` | `false` | Call `login()` |

## Keys present in the template but not read by the code

`email.enabled`, `email.use_ssl`, `email.from`, `root_server_ip`, `log_file`,
`log_backup_count`.

## Template issue

In the committed `config/config.yaml` the recipient list item follows
`enabled: false` without a `to:` key, so YAML parses it as part of the
`enabled` value and `email.to` is missing. `send_email()` then fails on
`', '.join(None)`; the exception is caught in `check_server_status()`.
