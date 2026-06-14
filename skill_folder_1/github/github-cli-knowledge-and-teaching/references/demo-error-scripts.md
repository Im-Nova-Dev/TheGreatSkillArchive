# Demo Error Scripts

Use these to intentionally break things in a controlled demo.

## Script 1 — Forgotten Stage

```bash
echo "forgot to stage" >> README.md
git commit -m "update"
```

Expected error:
```
nothing added to commit but untracked file present
```
Lesson: `git commit` only includes staged changes.

---

## Script 2 — Detached HEAD

```bash
git switch main
git checkout HEAD~1
git status
```

Expected state:
```
HEAD detached at ...
```
Lesson: `HEAD` now points directly to a commit.

---

## Script 3 — Merge Conflict

```bash
git init demo && cd demo
echo base > file.txt && git add . && git commit -m "init"
git switch -c A && echo A > file.txt && git add . && git commit -m "A"
git switch main
git switch -c B && echo B > file.txt && git add . && git commit -m "B"
git switch main && git merge A && git merge B
```

Expected: conflict markers in `file.txt`
Lesson: conflicts are normal.

---

## Script 4 — Behind Remote

```bash
git clone https://github.com/cli/cli.git /tmp/cli-demo
cd /tmp/cli-demo
git switch -c old-topic
# Now another person merged changes to main
git pull --rebase
```

Expected:
```
CONFLICT ... or success after replay
```
Lesson: branches drift; update before pushing.
