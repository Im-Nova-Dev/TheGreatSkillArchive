# Terminal GitHub Cheat Sheet

## Auth & Setup

```bash
gh auth login                   # interactive login
gh auth status                  # show login
git config --global user.name "Name"
git config --global user.email "email@example.com"
git config --global credential.helper store
```

## Repos

```bash
gh repo clone owner/repo
gh repo create my-repo --public --clone
gh repo fork owner/repo --clone
gh repo view
gh repo list
git remote -v
```

## Day-to-Day Workflow

```bash
git status -sb
git add <file>
git commit -m "type(scope): message"
git push
gh pr create --title "..." --body "..."
gh pr list
gh pr view
gh pr diff
gh pr checkout N
```

## Branching

```bash
git checkout -b feat/foo
git branch -a
git push -u origin HEAD
gh issue develop 42 --checkout   # create branch from issue
```

## PR & Review

```bash
gh pr checks
gh pr checks --watch
gh pr review N --approve --body "LGTM"
gh pr review N --request-changes --body "See inline"
gh pr review N --comment --body "Suggestion"
gh pr merge --squash --delete-branch
gh pr close N
```

## Issues

```bash
gh issue list
gh issue create --title "..." --body "..."
gh issue view 42
gh issue comment 42 --body "..."
gh issue close 42
gh issue edit 42 --add-label bug
```

## GitHub Actions

```bash
gh workflow list
gh run list --limit 10
gh run view RUN_ID
gh run view RUN_ID --log-failed
gh run rerun RUN_ID
gh workflow run ci.yml --ref main
gh secret set API_KEY --body "..."
```

## Git Recovery

```bash
git log --oneline --decorate --graph --all
git reflog
git reset --soft HEAD~1
git restore --staged <file>
git restore <file>
git cherry-pick <sha>
```

## Scripting + API

```bash
gh api repos/{owner}/{repo}/issues
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/{o}/{r}/issues | python3 -c "..."
export GITHUB_TOKEN="ghp_..."
gh api graphql -f query='query { viewer { login } }'
```

## Good Habits

```bash
# Before push
git status -sb
git diff main...HEAD --stat

# Before PR
git log main..HEAD --oneline
gh pr checks

# Before merge
gh pr diff
gh pr view --json mergeable,mergeStateStatus
```
