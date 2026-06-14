# Commit Message Guide for Students

Good commits tell a story.

## Structure

```
type(scope): short description

Longer body if needed.
```

## Type Guide

- `feat` — new behavior
- `fix` — bug fix
- `refactor` — restructure without changing behavior
- `docs` — documentation only
- `test` — tests only
- `chore` — dependencies, tooling
- `style` — formatting, whitespace
- `perf` — performance improvement
- `build` — build system or dependencies

## Examples

Good:
- `feat(auth): add password reset`
- `fix(api): handle null user response`
- `docs: update install instructions`

Bad:
- `update`
- `fix`
- `changes`

## One-Line Rule

If your commit were the only message someone saw, would they understand what changed and why?

## For Students

Start with:
- one scope
- one verb
- concrete outcome

Avoid:
- vague nouns
- commit many things in one message
- emotional language

## Future Skills

Later learn:
- recovering from split commit
- amendment for small fixes
- interactive rebase for cleanup
