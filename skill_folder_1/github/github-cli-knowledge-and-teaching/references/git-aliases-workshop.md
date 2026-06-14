# Git Aliases Workshop

## Why Aliases
- Save keystrokes
- Enforce consistent history patterns
- Make Git fun to type

## Starter Aliases
```
git config --global alias.s "status -s"
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.wip "commit -m 'wip' --no-verify"  # with caution
```

## Advanced Aliases
```
git config --global alias.aliases "!git config -l | grep alias"
git config --global alias.prune "fetch --prune"
git config --global alias.unstage "reset HEAD --"
```

## Exercise
Add three aliases of your own. Bonus: make one shell alias that wraps a `git` + `gh` sequence.

## Discussion
When do aliases hide what’s really happening?
