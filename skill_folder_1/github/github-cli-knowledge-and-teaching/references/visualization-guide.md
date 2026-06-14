# Git Visualization Guide

Use this to make Git histories visible.

## Command

```bash
git log --oneline --decorate --graph --all
```

Example output:
```
* abc123 (HEAD -> feature, origin/feature) feat: add login
* def456 on login UI
| * 789xyz (origin/main, main) docs: readme update
|/
* 111222 init
```

## What To Look For

- `*` marks commits
- Lines show parentage and branch positions
- Labels in parentheses show branch names and tags
- `HEAD` shows current position

## Exercises

1. Show `main` only versus branch history
2. Show `--all` versus current branch
3. Show history after merge
4. Show history after rebase
5. Show detached HEAD state

## Tips

- Use `--simplify-by-decoration` to see only tagged commits
- Use `--all --graph --oneline --decorate` daily as visualization habit
- Use `git log --graph --all --oneline --decorate -n 10` for short history window
