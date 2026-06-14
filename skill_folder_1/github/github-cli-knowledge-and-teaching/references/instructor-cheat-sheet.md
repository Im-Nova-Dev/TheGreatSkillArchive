# Instructor Cheat Sheet (Live Troubleshooting)

## Quick Diagnosis
- `git status` — first thing to run always
- `git log --oneline --graph --all` — see branches at a glance
- `git diff` — see actual changes
- `git reflog` — find lost work

## Frequent Fixes
| Symptom | First Command | Follow-Up |
|---------|---------------|----------|
| Changes won’t stage | `git status` | Check file path and permissions |
| Push rejected | `git pull --rebase` | Resolve, then push |
| Merge conflict | Open conflicted file | Choose side, stage, commit |
| Detached HEAD | `git switch -c <branch>` | Keep your work |
| Lost commit | `git reflog` | `git checkout <sha>` or branch |

## Teaching Phrases
- “What does `git status` say?”
- “Type the command, then read the output aloud.”
- “We can always undo this with `git reflog`.”
