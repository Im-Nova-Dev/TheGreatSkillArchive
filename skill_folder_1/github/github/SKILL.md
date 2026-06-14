---
name: github
description: "Comprehensive GitHub workflow: repo management, PR workflow, issues, code review, auth. Use for any GitHub CLI (gh) or API task — repo setup, branch/PR management, issue triage, review process, authentication."
version: 1.0.0
category: github
tags: [github, gh, repo, pr, issues, code-review, auth, workflow]
---

# GitHub Workflow

Comprehensive class-level skill covering all GitHub operations via `gh` CLI and API. Replaces the former narrow skills: `github-auth`, `github-code-review`, `github-issues`, `github-pr-workflow`, `github-repo-management`.

## When to Use

- Any task involving GitHub repositories, PRs, issues, or authentication
- Setting up repos, branch protection, secrets, releases, Actions workflows
- Creating, reviewing, and merging pull requests
- Issue triage, labeling, milestones, project boards
- Code review process: checklists, commenting style, approval workflow
- GitHub authentication (PAT, SSH, gh auth, tokens)

## Quick Reference

| Task | Primary Commands |
|------|------------------|
| **Auth** | `gh auth login`, `gh auth status`, `gh auth token` |
| **Repo create/clone** | `gh repo create`, `gh repo clone`, `gh repo fork` |
| **PR workflow** | `gh pr create`, `gh pr view`, `gh pr checkout`, `gh pr merge`, `gh pr checks` |
| **Issues** | `gh issue create`, `gh issue list`, `gh issue view`, `gh issue close` |
| **Code review** | `gh pr review`, `gh pr comment`, `gh pr diff` |
| **Repo settings** | `gh repo edit`, `gh api repos/:owner/:repo` |
| **Actions/Workflows** | `gh workflow list`, `gh run list`, `gh run view` |

---

## 1. Authentication

### Setup

```bash
# Interactive login (stores token in keychain)
gh auth login

# With token from stdin (CI-friendly)
echo $GH_TOKEN | gh auth login --with-token

# Check status
gh auth status
```

### Token Scopes

| Scope | Use Case |
|-------|----------|
| `repo` | Full repo access (private + public) |
| `workflow` | Update GitHub Actions workflows |
| `admin:org` | Org admin (branch protection, etc.) |
| `read:org` | Read org membership |
| `gist` | Create gists |

### SSH vs HTTPS

```bash
# Set default to SSH
gh config set git_protocol ssh

# Set default to HTTPS
gh config set git_protocol https
```

---

## 2. Repository Management

### Create / Clone / Fork

```bash
# Create new repo
gh repo create my-project --private --description "My project" --clone

# Clone existing
gh repo clone owner/repo

# Fork
gh repo fork owner/repo --clone
```

### Repository Settings

```bash
# View repo info
gh repo view owner/repo --json name,description,visibility,defaultBranchRef

# Edit settings
gh repo edit owner/repo --enable-issues --enable-wiki --delete-branch-on-merge

# Branch protection
gh api repos/owner/repo/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {"strict": true, "contexts": ["ci"]},
  "enforce_admins": true,
  "required_pull_request_reviews": {"required_approving_review_count": 1},
  "restrictions": null
}
EOF
```

### Secrets & Variables

```bash
# List secrets
gh secret list

# Set secret (reads from stdin or --body)
gh secret set MY_SECRET --body "value"
gh secret set MY_SECRET < secret.txt

# Repository variables
gh variable list
gh variable set DEPLOY_ENV --body "production"
```

### Releases

```bash
# Create release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes" --generate-notes

# Upload assets
gh release upload v1.0.0 ./dist/* --clobber
```

### GitHub Actions Workflows

```bash
# List workflows
gh workflow list

# View workflow runs
gh run list --workflow=ci.yml --limit=10

# Re-run failed
gh run rerun <run-id> --failed
```

---

## 3. Pull Request Workflow

### Prerequisites

- Fork or clone the repo
- Create a feature branch: `git checkout -b feature/xyz`
- Make commits with conventional messages

### Creating a PR

```bash
# Push branch and create PR
git push -u origin feature/xyz
gh pr create --title "feat: add xyz" --body "$(cat pr-body.md)" --base main

# Or with draft
gh pr create --draft --title "feat: add xyz" --body "WIP"
```

### PR Templates

Common templates in this skill's `templates/` directory:
- `templates/pr-body-bugfix.md`
- `templates/pr-body-feature.md`

### Managing CI

```bash
# Watch CI status
gh pr checks --watch

# View failed logs
gh run view <run-id> --log-failed

# Auto-fix common CI failures (lint, format)
# See references/auto-fixing-ci-failures.md
```

### Reviewing & Merging

```bash
# Request review
gh pr edit --add-reviewer @user1,@user2

# Approve
gh pr review --approve --body "LGTM"

# Request changes
gh pr review --request-changes --body "Please fix X"

# Comment
gh pr comment --body "Question about line 42"

# Merge (squash by default)
gh pr merge --squash --delete-branch

# Merge with rebase
gh pr merge --rebase --delete-branch

# Merge with merge commit
gh pr merge --merge --delete-branch
```

### Complete Workflow Example

See `references/complete-workflow-example.md` for end-to-end walkthrough.

---

## 4. Issues Workflow

### Creating Issues

```bash
# Interactive
gh issue create

# With template
gh issue create --title "Bug: ..." --body "$(cat templates/bug-report.md)"

# Assign labels and milestone
gh issue create --label "bug,high-priority" --milestone "v1.1"
```

### Triage & Management

```bash
# List issues
gh issue list --state open --label bug --assignee @me

# View issue
gh issue view 123 --comments

# Add labels
gh issue edit 123 --add-label "triaged"

# Close with keyword (auto-links from PR)
gh issue close 123 --reason "completed"
# or in PR body: "Closes #123"
```

### Issue Templates

See `templates/bug-report.md` and `templates/feature-request.md`.

### Projects & Boards

```bash
# List projects
gh project list

# View project items
gh project item-list <project-id> --format json
```

---

## 5. Code Review

### Review Checklist

1. **Correctness** — Does it solve the problem? Tests pass?
2. **Tests** — New tests for new behavior? Edge cases covered?
3. **Readability** — Clear names, comments where needed, no cleverness
4. **Breaking changes** — API changes documented? Migration path?
5. **Security** — No secrets, proper auth, input validation
6. **Performance** — No N+1, unnecessary allocations, hot path bloat
7. **Documentation** — README, docstrings, changelog updated?

### Commenting Style

- **Ask questions publicly** — "What happens if X is nil here?"
- **Suggest instead of command** — "Consider extracting this to a helper" vs "Extract this"
- **Praise good changes** — "Nice cleanup of the error handling"
- **Use GitHub's review categories** — Comment, Approve, Request changes

### Review Process

```bash
# Start review
gh pr view 123 --json files --jq '.files[].path' | xargs -I {} gh pr diff 123 -- {}

# Submit review
gh pr review 123 --approve --body "LGTM. Minor nit: ..."
gh pr review 123 --request-changes --body "Please address X"
```

### CI-First Mindset

- Never approve before CI passes
- Check `gh pr checks` before reviewing
- Re-review after fixes pushed

---

## 6. Useful Commands Reference

| Category | Commands |
|----------|----------|
| **Auth** | `gh auth login`, `gh auth status`, `gh auth token`, `gh auth refresh` |
| **Repo** | `gh repo create`, `gh repo clone`, `gh repo fork`, `gh repo view`, `gh repo edit`, `gh repo delete` |
| **PR** | `gh pr create`, `gh pr list`, `gh pr view`, `gh pr diff`, `gh pr checkout`, `gh pr merge`, `gh pr close`, `gh pr reopen`, `gh pr checks`, `gh pr review`, `gh pr comment` |
| **Issue** | `gh issue create`, `gh issue list`, `gh issue view`, `gh issue edit`, `gh issue close`, `gh issue reopen`, `gh issue comment` |
| **Actions** | `gh workflow list`, `gh workflow run`, `gh run list`, `gh run view`, `gh run rerun`, `gh run watch` |
| **Secrets** | `gh secret list`, `gh secret set`, `gh secret delete` |
| **Release** | `gh release create`, `gh release list`, `gh release view`, `gh release upload`, `gh release delete` |
| **API** | `gh api /repos/:owner/:repo`, `gh api --paginate /repos/:owner/:repo/issues` |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/prerequisites.md` | Required setup (gh, git, auth) |
| `references/review-checklist.md` | Detailed review checklist |
| `references/auto-fixing-ci-failures.md` | Common CI failure patterns and fixes |
| `references/conventional-commits.md` | Commit message format |
| `references/ci-troubleshooting.md` | Debugging CI failures |
| `references/branch-protection.md` | Branch protection rule patterns |
| `references/github-api-cheatsheet.md` | Raw API endpoints for advanced use |
| `templates/pr-body-bugfix.md` | Bug fix PR template |
| `templates/pr-body-feature.md` | Feature PR template |
| `templates/bug-report.md` | Issue bug report template |
| `templates/feature-request.md` | Issue feature request template |

---

## Common Pitfalls

1. **Forgetting `gh auth login`** — Run `gh auth status` first
2. **Wrong base branch** — Always verify `--base` in `gh pr create`
3. **Missing conventional commits** — Use `feat:`, `fix:`, `docs:`, etc.
4. **Approving before CI passes** — Always check `gh pr checks`
5. **Not linking issues** — Use "Closes #123" in PR body
6. **Large PRs** — Break into smaller, reviewable chunks
7. **Ignoring review feedback** — Address every comment; don't leave unresolved

---

## Verification Checklist

- [ ] `gh auth status` shows authenticated
- [ ] `gh repo view` works for target repo
- [ ] Branch created and pushed
- [ ] PR created with descriptive title/body
- [ ] CI passes (`gh pr checks`)
- [ ] Review completed (approvals obtained)
- [ ] Merged with appropriate strategy
- [ ] Branch deleted (local and remote)
- [ ] Issue closed via PR keywords