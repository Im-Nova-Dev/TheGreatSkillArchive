# Git Command Ladder — From Safe to Advanced

Teach commands in this order. Early commands should be repeatable without fear.

## Ladder Level 1 — Safe Commands

These commands do not change history.

- `git status`
- `git diff`
- `git log`
- `git log --oneline --graph --all`
- `git show`
- `git remote -v`
- `git branch`

Why safe: they only inspect.

## Ladder Level 2 — Additive Commands

These commands add or move state without destructive history changes.

- `git add`
- `git add -p`
- `git commit`
- `git commit --message`
- `git switch`
- `git switch -c`
- `git checkout` as legacy for `switch`
- `git push`
- `git fetch`
- `git pull`

Why mainly safe: commits are local and recoverable.

## Ladder Level 3 — Rewriting Private History

Only use on branches no one else is working on.

- `git commit --amend`
- `git rebase -i`
- `git rebase`
- `git reset --soft`
- `git reset --mixed`

Why these are harder: they rewrite commits.

## Ladder Level 4 — Destructive Commands

Treat these as “I know what this changes” tools.

- `git reset --hard`
- `git branch -D`
- `git push --force-with-lease`
- `git push --force`
- `git filter-repo`

Why dangerous: they discard work or rewrite shared history.

## Ladder Level 5 — Recovery Commands

Use these when something went wrong.

- `git reflog`
- `git fsck --lost-found`
- `git bisect start`
- `git bisect run`

Why they matter: they teach that Git is rarely irrecoverable.
