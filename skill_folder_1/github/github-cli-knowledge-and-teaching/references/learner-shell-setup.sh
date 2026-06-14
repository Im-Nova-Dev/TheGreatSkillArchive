#!/usr/bin/env bash
# Beginner-friendly Git + gh shell additions.
# Intended for local terminal setup, not globally forced.
# Review each line before use.

set -euo pipefail

# 1. Make Git status small and readable
git config --global status.short true
git config --global status.branch true

# 2. Default branch name for new repos
git config --global init.defaultBranch main

# 3. Editor preference - choose one and edit as needed
# git config --global core.editor "nvim"
# git config --global core.editor "nano"
# git config --global core.editor "code --wait"

# 4. Friendlier log by default (alias, not overriding real git log)
git config --global alias.lg "log --oneline --decorate --graph --all"

# 5. Optional: keep credentials in store instead of cache
# Plain text on disk; review security implications.
# git config --global credential.helper store

# 6. Optional: fetch all remotes in one command
git config --global fetch.all true

echo "Git shell setup complete."
echo "Run these to verify:"
echo "  git status -sb"
echo "  git config --global --list"
