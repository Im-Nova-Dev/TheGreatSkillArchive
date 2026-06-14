# Repo Permissions Worksheet

## Scenario
You are the admin of a team repo.

## Tasks
- Add a collaborator with write access
- Add a team with read access
- Enable branch protection on main
- Require PR review before merge
- Set required status checks (CI)

## Commands
```
gh repo edit --enable-issues true
gh secret set FOO --body "bar"
```

## Reflection
Why does least-privilege matter?
