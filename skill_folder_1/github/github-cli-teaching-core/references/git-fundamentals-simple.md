# Git Fundamentals — Simple Explanations for New Students

These are the concepts people need before they can use Git comfortably on the command line.

## 1. What is Git?

Git is a history tool.

- It does not “upload to GitHub” by itself.
- It records snapshots of your files over time.
- Those snapshots are stored in a hidden `.git` folder inside your project.

Analogy: Git is like “Save Game” slots for a project. You can revisit any previous save, branch into an alternate timeline, or reset.

## 2. The Three Places

Git tracks files across three areas:

- Working tree — your actual files on disk (the ones you open in an editor)
- Staging area — a temporary list of changes you want in the next snapshot
- Git repository (`.git`) — permanent snapshot history

Flow of a change:

working tree → `git add` → staging area → `git commit` → git repository

`git status` always tells you what is in each area.

## 3. What is a Commit?

A commit is one saved snapshot.

It contains:
- the file states at that moment
- a message you write
- metadata: author, date, parent commit(s)

A commit does not mean “send to GitHub”. It only saves locally.

## 4. Branch = Timeline

A branch is a movable name for a commit.

- `main` is one branch.
- A feature branch is a second timeline starting from the same point.
- Branches diverge when the timeline splits.

`git checkout -b new-branch` = create a new timeline and switch to it.

## 5. HEAD

`HEAD` is “where am I right now”.

- Usually `HEAD` points to the current branch.
- When you commit, `HEAD` and the branch move forward together.

## 6. Remote vs Local

- Local: commits on your machine, internet not needed.
- Remote: a copy of the repo on GitHub, GitLab, etc.
- `git push` copies local commits to a remote branch.
- `git pull` = fetch + merge/rebase from remote.

## 7. Common Mistakes Explained

Mistake: “I committed and something broke.”
Fix: `git revert` creates a new commit that undoes a previous commit. `git reset` rewrites history; use carefully.

Mistake: “I committed to the wrong branch.”
Fix: `git cherry-pick <sha>` to copy the commit to the correct branch, then reset/revert on the wrong branch.

Mistake: “I lost commits.”
Fix: `git reflog` remembers every place HEAD has been. Use it as a time machine.

## 8. What a “Pull Request” Is

- A PR is a request to merge one branch into another.
- It lives on GitHub, not in Git itself.
- `git` manages commits.
- `gh` manages PRs.

Simplification: a PR is a conversation + proposal. It says “please review my commits and merge them into main.”

## 9. merge, rebase, squash

Teach one concept per sentence:

- `merge` — join two timelines and keep the full memory of both with a merge commit.
- `rebase` — rewrite your branch so it looks like you started from a newer point on the other branch.
- `squash` — combine many commits into one commit before merging.

Safe defaults for beginners:
- Use merge commits first.
- Avoid `rebase` until they are comfortable with merge.
- Squash is helpful when one commit per PR is enough.

## 10. Git vs GitHub

- Git = history engine, runs locally.
- GitHub = website that hosts a copy of the repo, adds issues, PRs, Actions.

You can use Git without GitHub. GitHub makes collaboration easier.

## 11. One-Line Teaching Hooks

- “Commit early, commit locally.”
- “Push when you want someone else to see it.”
- “Branch for each idea.”
- “Pull before you push.”
- “Reflog is your time machine.”
