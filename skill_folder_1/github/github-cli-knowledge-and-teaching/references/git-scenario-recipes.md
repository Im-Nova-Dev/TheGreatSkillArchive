# Git Scenario Recipes — Practical Problem Solving

Quick “problem → command path” references common beginner scenarios.

## Scenario: Find what changed recently

```bash
git status -sb
git log --oneline --decorate --graph --all -n 10
git diff main...HEAD
```

## Scenario: Undo working tree edits

```bash
git restore <file>
git restore .
git checkout -- <file>   # older fallback
```

## Scenario: Unstage a file

```bash
git restore --staged <file>
git reset HEAD <file>      # older syntax
```

## Scenario: Delete the last commit but keep changes

```bash
git reset --soft HEAD~1
```

## Scenario: Delete the last commit and discard changes

```bash
git reset --hard HEAD~1
```

## Scenario: Recover a lost commit

```bash
git reflog
git checkout -b restore <sha-from-reflog>
```

## Scenario: Move a commit from branch A to branch B

```bash
git switch branch-A
git cherry-pick <sha>
git switch branch-B
git cherry-pick <sha>
```

## Scenario: Pull remote updates safely

```bash
git switch main
git pull origin main
git switch my-feature
git merge main
```

## Scenario: Update feature branch without merging main

```bash
git fetch origin
git rebase origin/main
```

## Scenario: Clean up local branches

```bash
git branch -a
git branch -d my-feature
git branch -D my-feature   # force delete if not merged
git remote prune origin
```

## Scenario: Change the last commit message

```bash
git commit --amend -m "new message"
```

## Scenario: Keep commits but remove accidental secrets

1. Rewrite history:
```bash
git filter-repo --path <file-with-secrets> --invert-paths
```

2. If the repo is already on GitHub:
```bash
git push origin --force
```
