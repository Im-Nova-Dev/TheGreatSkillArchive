# Simple Branching Strategies — Explained Plainly

Use this as a teaching map from trivial projects to team workflows.

## 1. The Main-Only Hobby Project

Best for:
- solo student
- very small projects
- exercises and drills

Rules:
- Work on `main`
- Commit often
- If you want an experiment, create a branch and delete it after

Why: reduces cognitive load. Git and GitHub are still valuable.

## 2. One-Feature Branch

Best for:
- solo learner introducing a feature
- any beginner after the first PR

Rules:
- `main` stays stable
- branch name like `feat/foo`
- merge back into `main` via PR

Why: teaches the core PR loop with minimal risk.

## 3. Gitflow Lite

Best for:
- team homework assignments
- small products

Branches:
- `main` — releasable state
- `develop` — integration branch
- `feat/*`, `fix/*` — merged into `develop`
- `hotfix/*` — merged into `main` + `develop`

Why: introduces integration and release concepts without heavy ceremony.

## 4. Trunk-Based Development

Best for:
- more advanced students
- teams with CI/CD

Branches:
- `main` — always deployable
- short-lived feature branches
- feature flags for incomplete work

Why: encourages small PRs and fast delivery.

## 5. Open Source Contributor Model

Best for:
- contributing to public repos
- hacktoberfest style work

Workflow:
- fork upstream
- add `upstream` remote
- create feature branch in your fork
- open PR against upstream
- keep fork in sync with upstream

Why: teaches collaboration across repos.

## Teaching Guidance

For novices:
- Start with strategy 1, then 2
- Avoid more than two branches until they can merge without help
- The goal is knowing *when* to branch, not mastering a methodology
