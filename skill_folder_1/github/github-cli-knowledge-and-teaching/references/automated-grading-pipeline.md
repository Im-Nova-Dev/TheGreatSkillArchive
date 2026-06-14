# Automated Grading Pipeline

## Concept
CI checks assignment repos for correctness.

## Checks
- `git log --oneline` has expected number of commits
- Expected branch names exist
- PR exists and is linked to issue
- Tests pass via Actions

## YAML Outline
```
name: grade
on: push
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash .github/grade.sh
```
