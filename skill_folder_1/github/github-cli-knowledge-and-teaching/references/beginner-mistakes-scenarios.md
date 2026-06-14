# Beginner Git Scenarios — Before and After

Use these to teach through realistic mistakes.

---

## Scenario 1 — Forgot to Stage

Before:
```bash
echo "new line" >> README.md
git commit -m "update"
```

After:
```bash
echo "new line" >> README.md
git add README.md
git commit -m "update"
```

Lesson: `git commit` only saves staged changes.

---

## Scenario 2 — Wrong Branch

Before:
```bash
# Accidentally committed on main
# Now wants it on a feature branch
git commit -m "feature work"
```

After:
```bash
git switch -c feature/new-work
git cherry-pick HEAD
git switch main
git reset --hard HEAD~1
```

Lesson: use reflog and cherry-pick to move commits safely.

---

## Scenario 3 — Message Too Vague

Before:
```bash
git commit -m "update"
```

After:
```bash
git commit -m "docs: clarify install steps"
```

Lesson: commit messages answer what and why.

---

## Scenario 4 — Massive Unsorted Changes

Before:
```bash
git add .
git commit -m "changes"
```

After:
```bash
git add -p
git commit -m "feat: login form"
git add -p
git commit -m "fix: typo"
```

Lesson: small commits make diffs readable.

---

## Scenario 5 — Stale Branch Before PR

Before:
```bash
git push
gh pr create --title "feature" --body "..."
# reviewer says: please rebase onto latest main
```

After:
```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

Lesson: update branch before opening PR.

---

## Scenario 6 — Accidental Secret Commit

Before:
```bash
echo "API_KEY=abc123" >> config.py
git add config.py
git commit -m "add config"
git push
```

After:
```bash
# Immediately rotate the exposed key on GitHub
# Remove from history
git filter-repo --path config.py --invert-paths
git push origin --force
```

Lesson: never commit secrets; rotate first if exposed.
