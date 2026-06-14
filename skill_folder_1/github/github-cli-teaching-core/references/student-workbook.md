# Student Workbook — Git and GitHub Terminal Practice

Use this as a fill-in-the-blank exercise set. Each task includes:
- Goal
- Commands to run
- Expected result
- Reflection question

---

## Task 1 — First Commit

Goal: create a repo and make a commit.

Commands:
1. `mkdir wb && cd wb`
2. `git init`
3. `echo "Hello" > hello.txt`
4. `git add hello.txt`
5. `git commit -m "docs: add hello"`

Expected:
- `git status` shows clean working tree
- `git log --oneline` shows 1 commit

Reflection:
- What did `git add` do?
- What did `git commit` do?
- Did anything go to GitHub yet?

---

## Task 2 — Branch and Switch

Goal: create a branch and work there.

Commands:
1. `git switch -b fix/hello`
2. `echo "Fixed" > hello.txt`
3. `git add hello.txt`
4. `git commit -m "fix: update hello"`

Expected:
- `git status` shows clean
- `git log --oneline --decorate --graph --all` shows two branches

Reflection:
- If you switch back to `main`, does `hello.txt` show "Fixed"?
- Why or why not?

---

## Task 3 — Push a Branch

Goal: send local branch to GitHub.

Commands:
1. `gh repo create workbook --public --source . --push`
2. `git push -u origin HEAD`

Expected:
- `git remote -v` shows origin
- `gh branch list` shows the branch

Reflection:
- What is `origin`?
- What happened when you ran `git push`?

---

## Task 4 — Open a PR

Goal: propose changes via PR.

Commands:
1. `gh pr create --title "fix: update hello" --body "First PR."`

Expected:
- `gh pr list` shows PR
- `gh pr checks` shows pending or completed checks

Reflection:
- Where does the PR live?
- Who can see it?

---

## Task 5 — Merge a PR

Goal: merge and delete branch.

Commands:
1. `gh pr merge --squash --delete-branch`
2. `git checkout main && git pull`
3. `git branch -d fix/hello`

Expected:
- `git log --oneline --decorate --graph --all` shows `main` with new commit
- `gh pr list` shows no open PRs

Reflection:
- What does `--squash` mean here?
- Why delete the branch after merging?

---

## Task 6 — Make a Mistake and Recover

Goal: break and fix.

Commands:
1. Commit something on `main`
2. Realize it should have been a feature branch
3. `git switch -c feat/recovery`
4. `git cherry-pick <last-commit-sha>`
5. `git switch main`
6. `git reset --hard HEAD~1`
7. `git push --force-with-lease`

Expected:
- `main` is back to previous state
- `feat/recovery` has the commit

Reflection:
- What did `git reset --hard` do?
- What does `--force-with-lease` protect against?

---

## Advanced Tasks

### A — Rebase onto Latest Main

Commands:
1. `git fetch origin`
2. `git rebase origin/main`
3. `git push --force-with-lease`

Expected: linear history without merge commit

### B — Resolve a Conflict

Commands:
1. Create two branches from main
2. Merge one with conflicting edit
3. Merge second -> conflict
4. Read markers, choose, `git add`, complete merge

Expected: conflict markers gone, clean commit history

### C — Fork Contribution

Commands:
1. `gh repo fork owner/repo --clone`
2. `git remote add upstream https://github.com/owner/repo`
3. `git fetch upstream`
4. Make change, push to fork, open PR to upstream

Expected: upstream PR visible in original repo
