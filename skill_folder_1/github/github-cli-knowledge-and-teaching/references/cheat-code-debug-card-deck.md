# Debug Card Deck

## Card Format

FRONT: Error message
BACK: One-line fix + explanation

### Card 1

- Front: `fatal: not a git repository`
- Back: You’re in the wrong folder. `cd` to where the `.git` directory lives.

### Card 2

- Front: `Your branch and ‘origin/main’ have diverged`
- Back: You have local commits that remote doesn’t, or vice versa. `git status` to inspect.

### Card 3

- Front: `merge conflict`
- Back: Git found the same lines changed differently in two places. Find `<<<<<<<`, `>>>>>>>` markers, choose the truth, then stage and commit.

### Card 4

- Front: `rejected` on push
- Back: Remote has new commits you don’t have. `git pull --rebase`, resolve, then push.

### Card 5

- Front: `detached HEAD`
- Back: You checked out an old commit. Make a branch from it to avoid losing work.

### Card 6
- Front: `refusing to merge unrelated histories`
- Back: Two repos with no common root. Add `--allow-unrelated-histories` if intentional.
''
,

'classroom-policies.md': ,

'hooks-and-customization-extras.md': 