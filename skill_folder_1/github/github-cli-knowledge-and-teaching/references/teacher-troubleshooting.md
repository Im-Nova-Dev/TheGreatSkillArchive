# Teacher Troubleshooting — Git and GitHub CLI Issues

Quick reference when a new student breaks something during a lesson.

## Student says: “It says I’m not on any branch.”

Likely cause: detached HEAD state.

Fix:
```bash
git status
git switch main
git switch -c new-branch
```

Teach: “HEAD stuck on a commit means you’re not on a branch.”

---

Student says: “I committed to main and now I can’t push.”

Likely cause: branch protection rules, or just messy history.

Fix:
```bash
git log --oneline -n 5
git branch -c new-branch HEAD~1
git switch main
git reset --hard origin/main
```

Teach: “You can always recreate a branch from a commit.”

---

Student says: “I see merge conflicts.”

Fix:
1. Read files with `<<<<<<<`, `=======`, `>>>>>>>`.
2. Choose what to keep.
3. `git add <file>`
4. `git commit`

Teach: “Conflicts are normal.”

---

Student says: “My PR is behind main.”

Fix:
```bash
git fetch origin
git merge origin/main
git push
```

Or:
```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

Teach: “Stay up to date before you open a PR.”

---

Student says: “I can’t find the commit I lost.”

Fix:
```bash
git reflog
git checkout -b recovered <sha>
```

Teach: “Reflog is your time machine.”

---

Student says: “The `gh` command says I’m not authenticated.”

Fix:
```bash
gh auth status
gh auth login
```

Teach: “`gh` is separate from `git`. Logging into GitHub in a browser does not log into `gh`.”

---

Student says: “It says permission denied (publickey).”

Fix:
```bash
ssh -T git@github.com
```

Teach: “SSH and HTTPS are different paths. Pick one and stick with it.”

---

Student says: “I don’t know which remote is which.”

Fix:
```bash
git remote -v
```

Teach: “`origin`, `upstream`, and forks: remotes are just bookmarks.”

---

Student says: “I accidentally staged a secret.”

Fix:
```bash
# Do not push
git restore --staged <file>
git restore <file>
git commit --amend -m "..."   # if already committed
# If already pushed:
git filter-repo --path <file> --invert-paths
git push origin --force
```

Teach: “Never commit secrets. If it happened, stop pushing and act quickly.”
