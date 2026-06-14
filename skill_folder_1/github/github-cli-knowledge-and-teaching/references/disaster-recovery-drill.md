# Disaster Recovery Drill

Simulate repo corruption and let learners practice recovery.

## Scenarios
1. **Lost Branch**: `git branch -D feature/x` then recover via reflog
2. **Bad Rebase**: `git rebase --abort` to recover
3. **Force Push**: simulate and restore with `git reflog` + reset
4. **Detached HEAD**: make commits, then save by branching
5. **Broken `.git`**: recover object from `.git/objects` backup

## Flow
- Instructor announces “disaster”
- Learners diagnose using `git status` / `git reflog`
- Recover within 5 minutes
- Debrief: what did Git remember?
