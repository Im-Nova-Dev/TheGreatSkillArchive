# Git and GitHub Competency Rubric

Use this to roughly assess learner skill and decide what to teach next.

## Level 1 — Beginner

Can:
- initialize a repo
- make commits locally
- push to GitHub
- open a PR

Should not yet:
- rebase public branches
- force push shared branches
- modify CI/secrets without help

## Level 2 — Intermediate

Can:
- create and switch branches
- resolve merge conflicts
- rebase private branches
- amend and fixup commits
- read CI logs and fix common failures
- review a PR with inline comments

Still needs help with:
- large rebases
- history archaeology with reflog/bisect
- permission errors

## Level 3 — Advanced

Can:
- cherry-pick, rebase, bisect intentionally
- write GitHub Actions workflows
- handle secrets, releases, and branch protection config
- contribute to open-source repos via fork/upstream workflow

Can teach:
- staging strategies with `git add -p`
- cleaning history with `git rebase -i`
- writing readable commit messages

## Level 4 — Expert

Can:
- debug git internals and recovery scenarios
- write git hooks
- script GitHub workflows with `gh` + shell
- mentor others

Uses:
- `git filter-repo` for cleanup
- `git rerere` to automate conflict resolution reuse
- advanced GitHub API for custom tooling
