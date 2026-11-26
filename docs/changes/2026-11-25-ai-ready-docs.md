---
date: 2026-11-25
type: docs
scope: docs, agent tooling
files: [AGENTS.md, CLAUDE.md, .claude/settings.json, .claude/skills/document-change/SKILL.md, docs/README.md, docs/architecture.md, docs/configuration.md, docs/deployment.md, docs/changes/2026-11-25-ai-ready-docs.md, README.md, README.de.md]
breaking: false
---
# Agent-ready documentation and project skills

## Context

- The repository had no `docs/` folder and no instructions for AI coding
  agents.
- The application is a single script (`server_monitor.py`); docs are sized
  accordingly.

## Change

- `docs/README.md`: index of docs and change records, maintenance rules.
- `docs/architecture.md`: functions, loop, status and notification logic.
- `docs/configuration.md`: keys of `config/config.yaml`, used and unused.
- `docs/deployment.md`: `dockerfile`, `docker-compose.yaml`.
- `AGENTS.md`: tool-agnostic agent instructions (commands, definition of done,
  hard rules, language table, skill list).
- `CLAUDE.md`: imports `AGENTS.md` via `@AGENTS.md`, Claude Code notes.
- `.claude/settings.json`: allows the `ast.parse` syntax check and read-only
  `make` targets; asks before running the script, Docker, `git push` and
  `make` targets that write files, hooks or git config; denies reading `.env`
  and `config/config.yaml`.
- `.claude/skills/document-change/SKILL.md`: change record template.
- `README.md`, `README.de.md`: section pointing to `docs/` and `AGENTS.md`.

## Decisions

- Only the `document-change` skill: no other recurring multi-step task exists
  in this single-script tool.
- No application code, build files, config or dependencies changed.

## Usage / Verification

```bash
python3 -m json.tool .claude/settings.json
python3 -c "import ast; ast.parse(open('server_monitor.py', encoding='utf-8').read())"
ls docs docs/changes .claude/skills
```

## Follow-ups

- `config/config.yaml` has no `to:` key: the recipient list item is parsed as
  part of `email.enabled`, so `email.to` is missing and e-mails fail.
- The status request in `check_server_status()` is not a Source RCON packet;
  a successful TCP connect plus any reply is treated as online and the raw
  reply as player list. The socket has no timeout, so `recv()` can block the
  loop.
- Template keys `email.enabled`, `email.use_ssl`, `email.from`,
  `root_server_ip`, `log_file`, `log_backup_count` are not read by the code.
- `README.md` lists `pythonping` as a requirement; the code does not use it
  and `requirements.txt` only lists `PyYAML` (no trailing newline).
- `dockerfile` hard-codes `python3.11` site-packages while using the
  `latest` Chainguard tags; `docker-compose.yaml` uses `version: '3.3'` and an
  image without a build or registry reference.
- `config/previous_status.yaml` is runtime state but committed.
- `Makefile` has no build, test or tag targets; contains a personal e-mail in
  `GIT_EMAIL` and emojis in the `info` target.
- Missing standard files: `.editorconfig`, `CHANGELOG.md`, `CONTRIBUTING.md`,
  `.pre-commit-config.yaml`, `.gitignore`, `.dockerignore`.
