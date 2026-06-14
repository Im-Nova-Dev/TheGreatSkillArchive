# Release Checklist Template

## Before Release
- [ ] All target PRs merged to main
- [ ] Version bumped in files
- [ ] Changelog updated
- [ ] Tests passing on main
- [ ] Tag created: `git tag vX.Y.Z && git push origin vX.Y.Z`
- [ ] GitHub release notes drafted

## After Release
- [ ] Release published on GitHub
- [ ] Artifacts built and available
- [ ] Announcements sent
- [ ] Monitoring dashboards checked

## Commands
```
git checkout main
git pull --rebase
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --notes "Release notes here"
```
