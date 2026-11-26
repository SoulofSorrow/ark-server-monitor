# AGENTS.md

Instructions for AI coding agents working in this repository. Tool-agnostic;
`CLAUDE.md` imports this file.

## Project

ARK server monitor: single Python script (`server_monitor.py`) that polls
configured ARK servers over TCP in a loop and sends an e-mail via SMTP when a
server goes offline or comes back online. Config in `config/config.yaml`,
last known status in `config/previous_status.yaml`. Runs locally or in a
Docker container (Chainguard Python image). Dependency: PyYAML. License
GPL-3.0 (`LICENSE`).

## Read first

1. `docs/README.md` (index).
2. The topic doc for the area you touch:

| Area | Doc |
| --- | --- |
| Control flow, functions, status logic | `docs/architecture.md` |
| `config/config.yaml` keys | `docs/configuration.md` |
| `dockerfile`, `docker-compose.yaml` | `docs/deployment.md` |

## Commands

```bash
pip install -r requirements.txt      # PyYAML
python server_monitor.py             # run (reads ./config/config.yaml relative to the CWD)
docker build -f dockerfile -t server-monitor .
docker compose -f docker-compose.yaml up -d
```

There is no test suite, no linter config and no CI in the repository.
`Makefile` only contains repository setup helpers (`.editorconfig`,
`.gitignore`, `.dockerignore`, git hook, git identity); it has no build or
test targets.

Cheap syntax check without side effects:

```bash
python3 -c "import ast; ast.parse(open('server_monitor.py', encoding='utf-8').read())"
```

## Definition of done

- `server_monitor.py` still parses; behaviour change verified by a manual run
  against a test server where possible (say so if not).
- Affected topic doc in `docs/` updated.
- New file `docs/changes/YYYY-MM-DD-<slug>.md` (template in
  `.claude/skills/document-change/SKILL.md`), listed in `docs/README.md`.
- User-visible change: update `README.md` and `README.de.md` together.

## Hard rules

- Never commit real SMTP credentials, RCON passwords, server IPs or e-mail
  addresses in `config/config.yaml`; keep placeholders.
- Never print or log `rcon_password` or the SMTP password.
- A failing server or SMTP error must not end the monitoring loop for the
  other servers.
- Paths `config/config.yaml` and `config/previous_status.yaml` are relative to
  the working directory; the container uses `WORKDIR /app` and mounts
  `./config` to `/app/config`. Keep them in sync.
- Do not run `make set-git-local` or `make install-hooks`: they change local
  git config and hooks.
- No emojis in new code, logs or docs.

## Language

| Artifact | Language |
| --- | --- |
| Code identifiers | English |
| Code comments, console output, e-mail texts | German (existing) |
| `README.md`, `docs/`, `AGENTS.md`, commit messages | English |
| `README.de.md` | German |

Commits: imperative subject, no tool attribution trailers.

## Project skills

Located in `.claude/skills/<name>/SKILL.md`.

| Skill | Use for |
| --- | --- |
| `document-change` | Writing the `docs/changes/` record |
