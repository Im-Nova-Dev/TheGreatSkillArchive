# GitHub CLI Update Workflow

## Why Update
New features, bug fixes, and security patches.

## Update Commands
- macOS (brew): `brew upgrade gh`
- Linux (apt): via official repo or binary
- Windows (winget / choco): `winget upgrade GitHub.cli`

## Verify
```
gh --version
gh auth status
```

## Teaching Moment
Update during class if needed; show how to recover from auth state changes after upgrade.
