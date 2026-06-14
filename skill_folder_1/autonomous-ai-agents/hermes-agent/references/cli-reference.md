---
topic: cli-reference
source: hermes-agent
---

# CLI Reference

## Quick Start

```bash
hermes setup
hermes chat -q "What is the capital of France?"
hermes model
hermes doctor
```

## Global Flags

| Flag | Effect |
|------|--------|
| `--version, -V` | Show version |
| `--resume, -r SESSION` | Resume by ID/title |
| `--continue, -c [NAME]` | Resume by name or most recent |
| `--worktree, -w` | Isolated git worktree mode |
| `--skills, -s SKILL` | Preload skills |
| `--profile, -p NAME` | Use named profile |
| `--yolo` | Skip dangerous-command approval |
| `--pass-session-id` | Include session ID in system prompt |

## Chat Flags

| Flag | Effect |
|------|--------|
| `-q, --query TEXT` | Single query |
| `-m, --model MODEL` | Model override |
| `-t, --toolsets LIST` | Toolset filter |
| `--provider PROVIDER` | Force provider |
| `-v, --verbose` | Verbose output |
| `-Q, --quiet` | Suppress banner/spinner |
| `--checkpoints` | Enable `/rollback` |
