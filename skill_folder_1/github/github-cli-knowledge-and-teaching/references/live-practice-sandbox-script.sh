#!/usr/bin/env bash
# live-practice-sandbox.sh
# Creates a disposable Git sandbox for live practice.
# Usage: bash live-practice-sandbox.sh [sandbox-name]
# Default sandbox name: git-sandbox

set -euo pipefail

NAME="${1:-git-sandbox}"
ROOT="/tmp/${NAME}"

rm -rf "$ROOT"
mkdir -p "$ROOT"
cd "$ROOT"

git init -b main

git config user.name "Trainee"
git config user.email "trainee@example.com"

for f in README.md LICENSE CONTRIBUTING.md; do
  [ -f "$f" ] || echo "Placeholder: $f" > "$f"
done

git add -A
git commit -m "chore: initial commit"

echo "Sandbox ready: $ROOT"
echo "Next: git switch -c feature/hello"
echo "Then: echo 'hello' >> README.md && git commit -am 'feat: add greeting'"
