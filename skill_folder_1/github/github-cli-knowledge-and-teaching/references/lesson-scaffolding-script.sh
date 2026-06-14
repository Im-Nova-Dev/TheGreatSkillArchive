#!/usr/bin/env bash
# lesson-scaffolding.sh
# Creates a ready-to-teach Git demo environment.
# Designed for instructors running live Git lessons.
# Review before using.

set -euo pipefail

REPO_NAME="${1:-lesson-demo}"
BRANCH_NAME="${2:-feat/demo}"
COMMIT_MSG="${3:-chore: scaffold lesson repo}"

mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# Initialize repo
git init
git config status.short true
git config status.branch true
git config init.defaultBranch main

# Create initial files
cat > README.md <<EOF
# $REPO_NAME
EOF

cat > .gitignore <<EOF
__pycache__/
node_modules/
.venv/
EOF

# First commit
git add README.md .gitignore
git commit -m "docs: add README and gitignore"

# Create feature branch
git switch -c "$BRANCH_NAME"

# Add a file commonly used in demos
cat > demo.txt <<EOF
demo change
EOF

git add demo.txt
git commit -m "test: add demo file"

# Return to main
git switch main

# Summary
echo "Scaffolded: $REPO_NAME"
echo "Branches:"
git branch -a
echo "Commits:"
git log --oneline --decorate --graph --all -n 5

# Optional: publish to GitHub if gh is logged in
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "Publishing to GitHub..."
  gh repo create "$REPO_NAME" --public --source . --push
fi
