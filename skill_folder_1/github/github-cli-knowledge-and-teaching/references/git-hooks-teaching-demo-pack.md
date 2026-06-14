# Git Hooks Teaching Demo Pack

## Demo 1: Reject Bad Commit Message
Hook: `commit-msg`
Show rejection by typing `git commit -m "bad"`.

## Demo 2: Auto-Format Before Commit
Hook: `pre-commit`
Run `black` or `gofmt` in the hook; show how it blocks a bad commit.

## Demo 3: Issue-Branch Linker
Hook: `prepare-commit-msg`
Auto-fills branch name in commit body.

## Teaching Narrative
“Hooks are personal rules Git enforces for you.”

## Audience Reaction
- Beginners: magic
- Advanced: inspiration to write their own

## Safety
Show `SKIP` environment variable or `--no-verify` flag, with warnings about abuse.
