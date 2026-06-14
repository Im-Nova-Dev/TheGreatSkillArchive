# First-PR Teaching Script

Repeatable script for a learner who has never opened a PR from the terminal.

## Setup

- Confirm GitHub account exists
- Confirm `git`, `gh`, and internet access
- Choose a repo name like `demo` or their project name

## Step 1 — Why terminal?

"Using GitHub in the terminal means:
- faster keyboard flow
- easier automation
- full history in one place
- less context switching"

## Step 2 — Mental model

"Git saves local snapshots.
GitHub shares them.
`git` manages snapshots.
`gh` manages sharing."

## Step 3 — Auth

```bash
gh auth login
git config --global user.name "Their Name"
git config --global user.email "email@example.com"
```

## Step 4 — Repo

```bash
mkdir demo && cd demo
git init
echo "# demo" > README.md
git add README.md
git commit -m "docs: add README"
gh repo create demo --public --source . --push
```

Show the repo URL and `gh browse`.

## Step 5 — Second commit

```bash
echo "update" >> README.md
git add README.md
git commit -m "docs: update README"
git push
```

## Step 6 — Pull request

```bash
gh pr create --title "docs: update README" --body "Small follow-up."
```

Show `gh pr list` and `gh pr view`.

## Step 7 — Checks and merge

```bash
gh pr checks --watch
gh pr merge --squash --delete-branch
```

## Step 8 — Reflection

```bash
git checkout main && git pull
gh browse
```

Ask:
- What did `git add` do?
- What did `git commit` do?
- What did `git push` do?
- Where did the PR live: local machine or GitHub?
- Why was `gh` useful?
