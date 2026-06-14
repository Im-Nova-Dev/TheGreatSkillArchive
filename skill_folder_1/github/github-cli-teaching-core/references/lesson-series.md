# Git and GitHub Lesson Series — Slide-Ready Markdown

Use this as a complete teaching series. Each lesson is one markdown section.

---

## Lesson 1 — What Git Is and Why It Matters

Key ideas:
- Git is a history tool
- It works locally first
- GitHub is one remote provider

Demo:
- `git status`
- `git init`
- create file, commit, log

Takeaway:
- Git remembers. You can always go back.

---

## Lesson 2 — The Three Areas of Git

Key ideas:
- working tree
- staging area
- `.git` repository

Demo:
- `git status` after add and after commit
- `git diff`

Takeaway:
- `add` = stage, `commit` = save

---

## Lesson 3 — Commits and Messages

Key ideas:
- commits are snapshots
- good messages matter

Demo:
- `git commit -m "feat: add login"`
- `git log --oneline`

Takeaway:
- a good message answers what and why in one line

---

## Lesson 4 — Branches

Key ideas:
- branch = movable label
- `main` is convention, not magic
- branches diverge from shared history

Demo:
- `git switch -c feature`
- `git log --graph --oneline --all`

Takeaway:
- branch per idea

---

## Lesson 5 — Merging

Key ideas:
- merge commit
- fast-forward
- conflict basics

Demo:
- `git merge feature`
- create conflict, resolve

Takeaway:
- merge means join timelines

---

## Lesson 6 — Remotes and Push

Key ideas:
- clone, origin, push, pull
- local vs remote

Demo:
- `gh repo create ... --clone`
- `git push`
- `gh pr create`

Takeaway:
- push makes work visible to others

---

## Lesson 7 — Pull Requests

Key ideas:
- PR is a conversation
- reviews, comments, checks

Demo:
- open PR
- `gh pr view`, `gh pr diff`
- `gh pr checks`

Takeaway:
- a PR is not just a button, it is a workflow

---

## Lesson 8 — GitHub Actions and CI

Key ideas:
- workflow, run, check
- reading logs

Demo:
- `gh run list`
- `gh run view`
- `gh run view --log-failed`

Takeaway:
- red checks are clues, not stop signs

---

## Lesson 9 — Forking and Contributing

Key ideas:
- fork = personal copy
- upstream = original repo
- triangular workflow

Demo:
- `gh repo fork owner/repo --clone`
- add upstream
- push and open upstream PR

Takeaway:
- forking is how open source scales contributions
