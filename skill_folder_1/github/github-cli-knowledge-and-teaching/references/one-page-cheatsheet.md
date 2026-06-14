# Git and GitHub — One-Page Cheatsheet

## Core Mental Model

- `git` manages history
- `gh` manages GitHub
- Only `git` moves code

## Before You Push

```bash
git status -sb
git diff main...HEAD --stat
```

## Daily Commands

```bash
git status -sb
git add <file>
git commit -m "type(scope): message"
git push
gh pr create --title "..." --body "..."
gh pr checks
gh pr view
```

## Branching

```bash
git switch -c feat/foo
git branch -a
git switch main
git branch -d feat/foo
```

## Review

```bash
gh pr checkout N
git diff main...HEAD
gh pr review N --approve|--request-changes|--comment
```

## Merge

```bash
gh pr merge --squash --delete-branch
git checkout main && git pull
```

## Recovery

```bash
git reflog
git restore <file>
git restore --staged <file>
git reset --soft HEAD~1
```

## Common Pitfalls

- `git commit` does not upload. `git push` does.
- `git diff` shows unstaged changes unless you use `--staged`.
- Three dots `main...HEAD` means “changes in this branch.”
- `origin` is the remote you cloned from; `upstream` is the repo you forked from.
