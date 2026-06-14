# Advanced Extension Exercises

For learners who outpace the cohort — optional, self-study.

## 1. Interactive Rebase

Given a messy branch, use `git rebase -i` to reorder, squash, and reword commits until history reads like a story.

### Deliverable
- A branch with 5 clean commits narrating one logical change.

## 2. Cherry-Pick a Bugfix

- Clone a sample repo.
- Create a commit branch with a bugfix.
- Cherry-pick that commit onto your main branch without merging the full branch.

## 3. Bisect Practice

- Introduce a bug in a project history.
- Use `git bisect` to find the bad commit in under 10 tries.

## 4. GitHub Actions Workflow

- Write a `.github/workflows/ci.yml` that runs tests on PRs.
- Add a status check to the PR.

## 5. GitHub Pages Deployment

- Deploy a static site from a repo to `gh-pages`.
- Use a custom domain if you want extra points.

## 6. Cross-Repo PR with Cache

- Fork a repo.
- Make multiple commits across branches, then open a cross-repo PR to upstream.
- Use GitHub review comments inline.

## 7. Migration Script

- Write a script (bash/python) that clones a repo, rewrites authors, and pushes to a new remote.
