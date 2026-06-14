# Team Git Workflow — Template

Use this as a starting point for documenting how a team uses Git and GitHub.

## 1. Branch Model

State the branching strategy in plain terms:
- What is the main branch?
- Are there long-lived integration branches?
- How are features cut?
- How are hotfixes handled?

Example:
- `main` — always deployable
- `develop` — integration for next release
- `feat/*` — feature branches from `develop`
- `fix/*` — bug fix branches
- `hotfix/*` — urgent fixes from `main`

## 2. Naming

Branch:
- `feat/short-description`
- `fix/short-description`
- `chore/short-description`

Commit:
- Conventional Commits: `type(scope): description`

## 3. Reviewing

- PRs require at least 1 approval
- CI must pass before merge
- Typical review SLA: within X hours/days
- Use `gh pr review` to approve or request changes

## 4. Merging

- Preferred merge strategy: squash
- Delete branch after merge
- Do not push after force push to shared branches

## 5. Keeping Up to Date

- Rebase or merge from target branch daily
- Before opening PR, ensure branch is up to date
- Use `git pull --rebase` or `git fetch && git rebase`

## 6. GitHub Setup

- Branch protection rules on:
  - `main`
  - `develop`
- Required status checks: CI, lint, tests
- Required reviews: yes/no
- Disable force push on protected branches
- Enable auto-merge: recommended
- Secrets handled via `gh secret`

## 7. Common Commands

Take the terminal-github-cheatsheet and trim it to only what this team uses. Keep it to one page.

## 8. Troubleshooting

- Who do I contact for GitHub access problems?
- Where do we log GitHub access requests?
- Who fixes branch protection when it blocks a release?
