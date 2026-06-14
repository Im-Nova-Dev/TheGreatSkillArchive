# Git + Docker Workflow

## Why
Containers make environments reproducible.

## Use Cases
- Sharing a setup that always works
- Testing Git commands safely
- CI pipelines

## Commands
```
docker run --rm -v $(pwd):/repo alpine/git status
docker run --rm -v $(pwd):/repo alpine/git log --oneline
```

## Teaching Demo
Show how a disposable container can run Git commands without installing Git locally.
