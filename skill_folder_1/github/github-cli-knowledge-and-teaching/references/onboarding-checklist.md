# Git + GitHub Onboarding Checklist

This is a checklist to hand to a new learner at the start of a lesson or cohort.

## Before the first lesson

- [ ] Install Git (`git --version`)
- [ ] Install `gh` CLI (optional but strongly recommended)
- [ ] Create GitHub account
- [ ] Confirm internet access and that GitHub is reachable
- [ ] Set global identity:
  - [ ] `git config --global user.name "Name"`
  - [ ] `git config --global user.email "email@example.com"`
- [ ] Optional: set editor:
  - [ ] `git config --global core.editor "nvim"` or preferred editor
- [ ] Optional: set credential helper:
  - [ ] `git config --global credential.helper store`
- [ ] Verify auth:
  - [ ] `gh auth login`
  - [ ] `gh auth status`
  - [ ] Or confirm HTTPS token / SSH key works with a test clone

## First-day capabilities

By the end of the first session the learner should be able to:

- [ ] Run `git status` and explain every line
- [ ] Create a repo with `git init`
- [ ] Stage and commit a file
- [ ] Push to GitHub
- [ ] Create a PR from the terminal
- [ ] View CI status
- [ ] Merge the PR and delete the branch

## Progression milestones

- Milestone 1 — comfortable `git add`, `commit`, `status`
- Milestone 2 — create and switch branches
- Milestone 3 — handle a review and push fixes
- Milestone 4 — recover from a bad state using reflog or amend
- Milestone 5 — fork and contribute upstream
- Milestone 6 — read CI logs and fix failing checks
- Milestone 7 — change merge strategy or rebase intentionally
- Milestone 8 — read workflow YAML and explain pipeline steps

## Lesson check cadence

Use warm-up quiz at the start of each session. Use drills at the end of each session. Use scenario recipes as homework prompts.
