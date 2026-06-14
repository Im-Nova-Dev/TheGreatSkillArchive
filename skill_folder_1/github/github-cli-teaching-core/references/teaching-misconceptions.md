# Teaching Git Misconceptions

Common beginner mental models that cause confusion.

## Misconception: "Commit means upload to GitHub"

Reality:
- `git commit` = save a snapshot locally
- `git push` = send local commits to GitHub
- `git fetch` = download without applying
- `git pull` = fetch + merge/rebase

Teach with timeline:
working tree -> git add -> staging -> git commit -> local repo -> git push -> remote

## Misconception: "Git is a backup tool"

Reality:
- Git is a collaboration and history tool
- History is structured narrative, not autosave
- `git revert` is the safe undo, `git reset` rewrites history

## Misconception: "Branch names matter to Git"

Reality:
- Branch = movable label
- `main` and `origin/main` are completely different refs
- Deleting a branch only deletes the label
- Every commit is still in the reflog

## Misconception: "`git checkout` does everything"

Reality:
- Old: `git checkout <branch>` changes branch
- Old: `git checkout -- <file>` discards changes
- Modern: `git switch` changes branch, `git restore` discards changes
- Use modern commands by default unless teaching old environments

## Misconception: "Merging always causes conflicts"

Reality:
- Conflicts mean the same line was changed in two branches
- Conflicts are expected and normal
- Resolution is a first-class skill, not a failure mode

## Misconception: "GitHub and Git are the same thing"

Reality:
- Git: protocol and history engine
- GitHub: social coding platform on top of Git
- You can lose data on GitHub and still have it locally
- `git remote -v` tells you where remotes point
