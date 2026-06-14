# Repo Cleanup Exercise

## Goals
Tidy a messy repo without losing history.

## Steps
1. List all branches. Delete merged ones.
2. Prune deleted upstream branches: `git fetch --prune`.
3. Remove old tags.
4. Rewrite messy commit messages in last 5 commits (rebase -i).
5. Verify `.gitignore` covers builds, secrets, and IDE files.

## Reflection
- What would happen if you deleted an unmerged branch?
- When should you NOT rewrite history?
