# Deployment

## Image (`dockerfile`)

- Multi-stage: builder `cgr.dev/chainguard/python:latest-dev` installs
  `requirements.txt` with `pip install --user`.
- Runtime `cgr.dev/chainguard/python:latest`, `WORKDIR /app`.
- Copies `config/` to `/app/config` and `server_monitor.py`.
- Copies site-packages from the hard-coded path
  `/home/nonroot/.local/lib/python3.11/site-packages` (comment in the file:
  update when the Python version changes).
- `ENTRYPOINT ["python", "-u", "/app/server_monitor.py"]`.

```bash
docker build -f dockerfile -t server-monitor .
```

## Compose (`docker-compose.yaml`)

- Service and container `ark-server-monitor`, `image: server-monitor` (no
  `build:`; build the image first with the tag `server-monitor`).
- Volume `./config:/app/config` (config and status file).
- `restart: unless-stopped`.

```bash
docker compose -f docker-compose.yaml up -d
```

## CI / release

Not defined in the repository.
