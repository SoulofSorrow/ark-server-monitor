@AGENTS.md

## Claude Code specifics

- `.claude/settings.json` allows the syntax check and denies reading
  `config/config.yaml` (holds SMTP and RCON credentials in real use).
- Running the script opens network connections and may send e-mails; ask
  before running it.
