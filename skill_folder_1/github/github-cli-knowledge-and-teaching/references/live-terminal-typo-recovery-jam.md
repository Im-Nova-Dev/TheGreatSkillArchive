# Live Terminal Typo Recovery Jam

## Setup
Intentionally type a wrong command and react in real time.

## Drill 1: Misspelled Branch
- `gti switch -c fix/typo`
- Observe “command not found”
- Teach: read the error, check spelling, retry

## Drill 2: Wrong File Path
- `git add readme.md` (actually README.md)
- `git status` shows untracked and modified confusion
- Fix: `git add README.md`

## Drill 3: Argument Mix-Up
- `git commit -m` with missing message
- Git opens editor unexpectedly
- Recovery: close editor, reissue with message

## Game Rules
- Fastest correct recovery wins
- Must explain what happened before moving on
