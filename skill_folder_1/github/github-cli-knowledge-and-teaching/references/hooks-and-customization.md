# Git Hooks and Customization

Use this to lighten repetitive Git tasks.

## What Are Hooks

Git hooks are scripts that run automatically on Git events.

## Common Hooks

- `pre-commit` — run before commit
- `pre-push` — run before push
- `post-commit` — run after commit
- `post-merge` — run after merge

## Example: pre-commit Lint Check

Create `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ruff check .
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Example: pre-push Lint and Tests

Create `.git/hooks/pre-push`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ruff check .
python -m pytest -q
```

## What To Avoid

- Network calls in hooks
- Long-running tasks in pre-commit; use CI instead
- Hardcoding secrets in hook scripts

## Teaching Tip

Hooks are automation, not punishment. Frame them as guardrails.
