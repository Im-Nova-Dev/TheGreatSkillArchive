# Instructor Emergency Pocket Guide

## One-Page printable.

## First Commands
- `git status` — diagnose first
- `git log --oneline --graph --all` — where are we?
- `git reflog` — find lost work

## Common Emergencies
| Crisis | Fast Fix |
|--------|----------|
| Push rejected | `git pull --rebase`
| Merge conflict | resolve + add + commit
| Detached HEAD | `git switch -c <branch>`
| Force-push needed | `git push --force-with-lease`
| Hook blocking | `--no-verify` (explain why risky) |

## Teaching Fixes
- Demo slower, not faster
- Ask the room: “What does `git status` say?”
- Pair stuck learner with helper
- Use fallback repo if setup broken
