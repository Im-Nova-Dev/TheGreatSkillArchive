# GitHub Security Best Practices

- Enable 2FA on GitHub account
- Use `gh auth login` instead of copying tokens manually
- Prefer SSH keys over HTTPS for automation
- Review Dependabot alerts
- Never commit `.env` or secrets
- Use branch protection rules on main
- Require PR reviews before merge
- Rotate any leaked token immediately

## Teaching Segments
- **Demo**: `gh auth status` to check auth method
- **Exercise**: Create a repo with branch protection
- **Discussion**: Why CI + branch protection together reduce risk
