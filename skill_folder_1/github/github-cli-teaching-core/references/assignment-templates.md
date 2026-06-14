# Assignment Templates — Git Practice Problems

Use these as homework, workshop prompts, or take-home assessments.

## Assignment 1 — Reflect on History

For each scenario, run `git log --oneline --decorate --graph --all` and explain what the history shows.

1. A linear main branch with 3 commits
2. A main branch and a feature branch that diverged
3. A merged feature branch with a merge commit
4. A rebased feature branch
5. A detached HEAD state

## Assignment 2 — Predict the State

After each command, state what `git status` will show.

1. `git add foo.py`
2. `git commit -m "msg"`
3. `git restore foo.py`
4. `git restore --staged foo.py`
5. `git reset --soft HEAD~1`

## Assignment 3 — Diagnose the Error

Give the learner short error text. Ask them to:
1. Name the symptom
2. Name the most likely cause
3. Give a recovery command

Examples:
- “error: pathspec 'feature' did not match any file(s) known to git”
- “Your branch is ahead of 'origin/main' by 2 commits”
- “CONFLICT (content): Merge conflict in README.md”

## Assignment 4 — Write Good Commits

Give the learner a short set of changes and ask for a title + body.

1. A login bug fix
2. A new CLI flag
3. A README update

Use conventional commit format. Include motivation and scope.

## Assignment 5 — Plan a PR

For a fictional repo, ask the learner to:
1. State the problem
2. Pick a branch name
3. List commit messages
4. Write PR body
5. List review plan

## Assignment 6 — Fork Workflow

For an open-source repo:
1. Find a small repo you use
2. Fork it
3. Create a branch with a minimal fix
4. Write a PR
5. Respond as if you were the maintainer reviewing it

## Assignment 7 — CI Triage

Intentionally fail CI in a small repo:
1. Break lint
2. Find failing job
3. Read log
4. Fix and verify green

Write a short postmortem:
- what failed
- how you found it
- how you fixed it
