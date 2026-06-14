# Dotfile Management Workshop

## Why
Learners will customize their environment. Teach them to save it.

## Tools
- Bare Git repo in `~/.cfg`
- GNU Stow
- Chezmoi

## Minimal Demo
```
git init --bare $HOME/.cfg
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
config checkout
```

## Discussion
What should be versioned? What should stay local (secrets)?
