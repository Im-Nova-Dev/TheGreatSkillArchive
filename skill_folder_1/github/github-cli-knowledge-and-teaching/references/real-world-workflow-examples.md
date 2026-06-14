# Real-World Git Workflow Examples

Use these when a learner asks “how do teams actually use this?”

## Example 1 — Solo Developer

Goal: keep a small personal project on GitHub.

Rules:
- `main` is the only meaningful branch
- commit often with real messages
- tags for versions
- releases when useful

Commands they actually use:
- `git status`
- `git add -p`
- `git commit -m "..."`
- `git push`
- `gh release create v0.1.0`

Takeaway: even with one branch, Git and `gh` still save time and history.

---

## Example 2 — Weekend Open-Source Contributor

Goal: send a small fix to a public repo.

Rules:
- do not push directly to upstream
- fork first
- short-lived feature branch
- clean, focused PR
- respond to review quickly

Commands:
- `gh repo fork owner/repo --clone`
- `git remote add upstream ...`
- `git fetch upstream`
- `git switch -c fix/...`
- `git push`
- `gh pr create`
- `gh pr checks`
- `gh pr review ...`

Takeaway: collaboration is a conversation, not just a merge.

---

## Example 3 — Small Team Product

Goal: coordinated releases and QA.

Rules:
- protected `main`
- merge via PR after review
- CI required
- `develop` for integration if releases are rare

Commands:
- branches from `develop`
- PRs target `develop`
- hotfixes target `main` and backmerge
- `gh pr merge --squash --delete-branch`
- `gh release create`

Takeaway: process exists to reduce accidents, not to slow people down.

---

## Example 4 — Classroom Assignment

Goal: students submit work via PR.

Rules:
- each student forks
- PR must pass CI
- template-based PR body
- instructor reviews and merges

Commands:
- `gh repo fork class/repo --clone`
- branch per task
- `gh issue list` for task descriptions
- `gh pr create`

Takeaway: Git is also a submission mechanism and audit trail.

---

## Example 5 — Continuous Delivery Pipeline

Goal: every merge can deploy.

Rules:
- `main` always deployable
- tiny PRs
- feature flags for incomplete work
- fast-forward or rebase merges
- semantic releases via `gh release create`

Commands:
- `gh workflow run deploy.yml --ref main`
- `gh run watch <run-id>`
- `gh release create`

Takeaway: Git hygiene is an operational requirement, not decoration.
