# Quick Reference Poster (Markdown)

```
╔═══════════════════════════════════════════════╗
║          GIT / GH QUICK REFERENCE            ║
╠══════════════════════╦════════════════════════╣
║ First-Time Setup     ║ git config --global…   ║
╠══════════════════════╬════════════════════════╣
║ Initialize Repo      ║ git init               ║
║ Clone Repo           ║ git clone <url>        ║
╠══════════════════════╬════════════════════════╣
║ Check Status         ║ git status / s         ║
║ Stage Files          ║ git add -A             ║
║ Commit               ║ git commit -m "msg"    ║
║ View History         ║ git log --oneline --graph --all ║
╠══════════════════════╬════════════════════════╣
║ Branch New           ║ git switch -c <name>   ║
║ Switch Branch        ║ git switch <name>      ║
║ Merge                ║ git merge <name>       ║
║ Rebase               ║ git rebase main        ║
╠══════════════════════╬════════════════════════╣
║ Add Remote           ║ git remote add …        ║
║ Push                 ║ git push -u origin …   ║
║ Pull                 ║ git pull --rebase       ║
╠══════════════════════╬════════════════════════╣
║ GitHub: Issue        ║ gh issue create        ║
║ GitHub: PR           ║ gh pr create           ║
║ GitHub: View PR      ║ gh pr view <id>        ║
║ GitHub: Merge PR     ║ gh pr merge <id>       ║
║ GitHub: Actions      ║ gh run list            ║
╚══════════════════════╩════════════════════════╝
```

## Emergency Fixes
- Undo last commit (keep changes): `git reset --soft HEAD~1`
- Unstage file: `git restore --staged <file>`
- Discard local changes: `git restore <file>`
- Remove untracked files: `git clean -fd`
