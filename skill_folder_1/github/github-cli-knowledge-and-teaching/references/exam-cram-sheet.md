# Exam Cram Sheet

## Git Foundations
- Working tree → staging via `git add`
- `git status` shows staged, unstaged, untracked
- `git commit -m "msg"` captures snapshot
- `git log --oneline --graph --all` reads history

## Branching
- `git switch -c <name>` creates and switches
- `git merge` creates merge commit
- Rebase rewrites commit chain (don’t on shared branches)

## Remotes
- `git remote -v`
- `git push -u origin <branch>`
- `git pull --rebase` for clean linear history

## GitHub via CLI
- `gh auth login`
- `gh repo view`
- `gh issue create`
- `gh pr create`
- `gh pr view <id>` / `gh pr checkout <id>`
- `gh pr review --approve`
- `gh pr merge <id>`
- `gh run list`

## Emergency Cheats
- Discard changes: `git restore .`
- Unstage: `git restore --staged <file>`
- Undo last commit: `git reset --soft HEAD~1`
- Recover lost work: `git reflog`
