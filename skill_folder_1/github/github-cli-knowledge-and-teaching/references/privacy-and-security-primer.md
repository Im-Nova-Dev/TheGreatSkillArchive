# Privacy & Security Primer

## Credentials
- Never paste tokens, passwords, or keys in chat or shared docs.
- Use GitHub CLI auth (`gh auth login`) — never hardcode.
- Rotate exposed credentials immediately.

## Repo Visibility
- Private repos for practice if you want secrecy.
- Public repos: anyone can see; do not commit secrets.

## `.gitignore` Essentials
- `.env` files
- `*.pem`, `*.key`
- `node_modules/`
- `venv/`
- IDE configs (`.idea/`, `.vscode/`)

## SSH vs HTTPS
- SSH: no password per push (key-based)
- HTTPS: simpler for beginners, can use credential store

## GitHub Security Features
- Dependabot alerts
- Secret scanning
- Code scanning
- Required reviews / status checks

## Demo Output Reminder
When showing commands, never show real credentials. Mask them in recordings.
