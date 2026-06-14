# Complete Git Walkthrough — From Zero to Merged PR

Use this as a scripted, narrated walkthrough for a new student.

## Setup

```bash
git config --global user.name "Student"
git config --global user.email "student@example.com"
```

## Step 1 — Create local repo

```bash
mkdir learn-git && cd learn-git
git init
git status
```

Say: “`git status` is your compass. Run it whenever you’re unsure.”

## Step 2 — First save

```bash
echo "# learn-git" > README.md
git add README.md
git status
git commit -m "docs: add README"
git status
git log --oneline
```

Say: “`add` only changes staging. Commit moves it into history.”

## Step 3 — Branch

```bash
git checkout -b docs/typo-fix
echo "first commit on branch" > file.txt
git add file.txt
git commit -m "test: create file"
git log --oneline --decorate --graph --all
```

Say: “`--graph` shows branches like a timeline.”

## Step 4 — Push

```bash
gh repo create learn-git --public --source . --push
git remote -v
```

Say: “`origin` is the nickname for the GitHub URL.”

## Step 5 — Open PR

```bash
git checkout main
git switch -c feat/example
echo "hello from feature" >> file.txt
git add file.txt
git commit -m "feat: add example line"
git push -u origin HEAD
gh pr create   --title "feat: add example line"   --body "Learning PRs. Closes #1 if desired."
gh pr list
gh pr view
gh pr diff
gh pr checks
```

## Step 6 — Review

```bash
git fetch origin pull/$(gh pr view --json number -q .number)/head:review
git diff origin/main...HEAD
gh pr review $(gh pr view --json number -q .number) --comment --body "Looks good"
```

## Step 7 — Merge and cleanup

```bash
gh pr merge --squash --delete-branch
git checkout main
git pull
git branch -d feat/example
git log --oneline --decorate --graph --all
gh browse
```

## Step 8 — Ask reflective questions

1. What did `git add` do versus `git commit`?
2. Where did the PR live: locally or on GitHub?
3. What happened to `main` after merge?
4. What commands can run offline?
5. Why did we say `git switch -c` instead of `git checkout -b`?

## Step 9 — Show them how to recover

```bash
git reflog
```

Say: “Reflog is your time machine. It records where HEAD has been.”

---

Narration tips:
- Run `git status` after every major command.
- Pause after each stage and ask “What do you expect next?”
- Show both success output and common error text.
