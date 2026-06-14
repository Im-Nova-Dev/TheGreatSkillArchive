# Troubleshooting Flowchart

## Start: Something Went Wrong

```
Error / unexpected output?
   |
   v
Run: git status
   |
   v
Ahead / behind / diverged?
   |
   +---> Yes ---> git pull --rebase ---> resolve ---> push
   |
   v
Files shown as modified but you didn’t touch them?
   |
   +---> Possibly line endings or permissions.
        Try: git config core.autocrlf false / true
   |
   v
Merge conflict?
   |
   +---> Open conflicted file. Look for <<<<<<< markers.
        Choose side, remove markers, git add, git commit.
   |
   v
Detached HEAD?
   |
   +---> git switch -c <new-branch> to preserve work.
   |
   v
Force-pushed? Someone rewrote history on shared branch?
   |
   +---> git fetch + git reset --hard origin/<branch>
        (coordinate with team first)
   |
   v
Refused to merge unrelated histories?
   |
   +---> Confirm intentional. If yes, add --allow-unrelated-histories
   |
   v
Stash not applying cleanly?
   |
   +---> git stash show -p | git apply -R to reverse, then resolve and retry.
   |
   v
Still stuck?
   |
   +---> Use git reflog to find lost commits.
        Ask in community / office hours.
```
