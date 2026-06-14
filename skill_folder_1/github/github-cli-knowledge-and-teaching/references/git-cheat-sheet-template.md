# Git Cheat Sheet Template

| Task | Command |
|------|---------|
| Start | `git init` |
| Clone | `git clone <url>` |
| Status | `git status` |
| Stage all | `git add -A` |
| Stage hunk | `git add -p` |
| Commit | `git commit -m "msg"` |
| Amend | `git commit --amend` |
| Log | `git log --oneline --graph --all` |
| New branch | `git switch -c <name>` |
| Switch | `git switch <name>` |
| Merge | `git merge <name>` |
| Rebase | `git rebase main` |
| Remote add | `git remote add origin <url>` |
| Push | `git push -u origin <branch>` |
| Pull with rebase | `git pull --rebase` |
| Fetch prune | `git fetch --prune` |
| Stash | `git stash` |
| Stash pop | `git stash pop` |
| Reflog | `git reflog` |
| Cherry-pick | `git cherry-pick <sha>` |

## GitHub CLI
| Task | Command |
|------|---------|
| Auth | `gh auth login` |
| Repo view | `gh repo view` |
| Issue create | `gh issue create` |
| PR create | `gh pr create` |
| PR view | `gh pr view` |
| PR checkout | `gh pr checkout <id>` |
| PR review | `gh pr review --approve` |
| PR merge | `gh pr merge <id>` |
| Run list | `gh run list` |
