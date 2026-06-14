# Common Git and GitHub Errors — Explained Simply

Use this as a reference for learners when they encounter errors.

## Git Errors

- `fatal: not a git repository`
  - Cause: you are not in a Git repo
  - Fix: `git init` or `cd` to the correct folder

- `error: src refspec main does not match any`
  - Cause: no commits yet or wrong branch name
  - Fix: `git commit` first, then verify branch name with `git branch`

- `fatal: refusing to merge unrelated histories`
  - Cause: starting a new repo with the same directory as an existing repo
  - Fix: `git pull origin main --allow-unrelated-histories` or start fresh

- `CONFLICT (content): Merge conflict in README.md`
  - Cause: both sides changed the same lines
  - Fix: read markers `<<<<<<<`, `=======`, `>>>>>>>`, choose one side, `git add`, `git commit`

- `error: pathspec 'feature' did not match any file(s) known to git`
  - Cause: branch does not exist or typo
  - Fix: `git branch -a` to list branches

- `Your branch is ahead of 'origin/main' by 1 commit`
  - Cause: you pushed but local and remote differ
  - Fix: `git push` or `git pull` depending on intent

- `fatal: You are not currently on a branch`
  - Cause: detached HEAD
  - Fix: `git switch main` or `git switch -c new-branch`

## GitHub / gh Errors

- `remote: Permission to user/repo denied`
  - Cause: wrong account, missing SSH key, or wrong token
  - Fix: `gh auth status`, check SSH keys, or switch remote URL

- `gh: command not found`
  - Cause: `gh` is not installed
  - Fix: install `gh` or use `git` + `curl` fallback

- `GraphQL error: Resource not accessible by integration`
  - Cause: missing permissions or token scope
  - Fix: verify workflow permissions and token scopes

- `422 Unprocessable Entity` when creating PR
  - Cause: branch does not exist, PR already exists, or invalid body
  - Fix: verify branch name with `git branch` and check open PRs

## CI Errors

- `ModuleNotFoundError`
  - Cause: missing dependency
  - Fix: add dependency to requirements or lockfile

- `lint failure: line too long`
  - Cause: style violation
  - Fix: run formatter locally and recommit

- `timeout failure`
  - Cause: process took too long
  - Fix: optimize the step or increase timeout in workflow

## Interpretation Guidance

Teach students to:
1. Read the first line only first (“what failed?”)
2. Look for file paths and line numbers
3. Search the repo for the failing file
4. Re-run the failing command locally if possible
