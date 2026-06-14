# Frequently Asked Questions — Git and GitHub

Keep this handy during lessons.

## Git Basics

Q: Is Git the same as GitHub?
A: No. Git is the local history tool. GitHub is a remote hosting platform.

Q: Do I need the internet to use Git?
A: No. You only need it for push, pull, fetch, and `gh`.

Q: What is the difference between `git add` and `git commit`?
A: `add` stages files for the next commit. `commit` saves them into history.

Q: What does `git status` show?
A: the state of the working tree and staging area.

Q: Can I undo a commit?
A: Yes. Use `git revert` for shared history, `git commit --amend` or `git reset` for private history.

## Branches

Q: Why create a branch?
A: To isolate an idea so it does not break `main`.

Q: What is the default branch?
A: Often `main`, but Git does not require any specific name.

Q: What happens if I delete a branch?
A: The label is removed. The commits remain in the repository and in reflog.

Q: What is a merge commit?
A: A commit with two parents created by `git merge`.

Q: When should I use rebase?
A: Only on private branches. It rewrites history for a cleaner timeline.

## Remotes

Q: What is `origin`?
A: The default remote name after clone.

Q: What is `upstream`?
A: The convention for the original repo you forked from.

Q: Why use `git remote -v`?
A: To see where your local repo is connected.

## GitHub

Q: What is a PR?
A: A request to merge one branch into another on GitHub.

Q: Who can merge a PR?
A: Anyone with write access, depending on branch protection rules.

Q: What are GitHub Actions?
A: Automations that run when GitHub events happen.

Q: What does `gh` do that `gh` does not do better with the browser?
A: It makes GitHub operations fast, scriptable, and keyboard-driven.

## Mistakes

Q: I committed to `main`. Is it bad?
A: Not if no one else pulled. Use `git reset --hard HEAD~1` or move the commit to a branch.

Q: How do I fix a bad merge?
A: Use `git reset --hard` before push. After push, prefer `git revert` or a new fix commit.

Q: I lost a commit after deleting a branch. Can I recover?
A: Yes. Use `git reflog` to find the SHA and check it out.

Q: I pushed a secret. What should I do?
A: Rotate the secret immediately. Then rewrite history with `git filter-repo` and force push if necessary.

Q: Is `git push --force` safe?
A: Only on private branches. For shared branches, use `git push --force-with-lease`.
