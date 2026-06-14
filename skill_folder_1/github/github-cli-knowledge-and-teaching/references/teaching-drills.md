# GitHub in the Terminal — Teaching Drills

Use these exercises in order. Each drill builds muscle memory and reduces future steering.

## Drill 1: First PR in 10 Minutes

Purpose: build confidence. Reduce the gap between idea and visible PR on GitHub.

Sequence:
1. `mkdir demo && cd demo && git init`
2. Create README.md
3. `git add . && git commit -m "docs: add README"`
4. `gh repo create demo --public --source . --push`
5. `echo "more" >> README.md && git add . && git commit -m "docs: update README"`
6. `git push`
7. `gh pr create --title "docs: update README" --body "Small follow-up."`
8. `gh pr checks --watch`
9. `gh pr merge --squash --delete-branch`
10. `gh browse` to review the merged result

Exit condition: the user can do this without asking what to type next.

## Drill 2: Branch Hygiene

Purpose: reduce "I committed to the wrong branch" panic.

Sequence:
1. `git checkout -b wip/typo`
2. Make a change and commit
3. Rename: `git branch -m wip/typo fix/readme-typo`
4. Push renamed branch: `git push origin fix/readme-typo`
5. Open a PR, merge, delete local + remote branch

Exit condition: `git status -sb` becomes reflexive.

## Drill 3: Review Loop

Purpose: experience the full feedback cycle.

Sequence:
1. Open a PR with an intentional style issue
2. Reviewer catches it with `gh pr review --request-changes`
3. Fix, commit, push
4. Review again and merge

Exit condition: user understands review comments are process, not criticism.

## Drill 4: CI Recovery

Purpose: interpret CI logs instead of fearing red checks.

Sequence:
1. Break CI intentionally
2. Push, open PR
3. `gh pr checks --watch`
4. `gh run list --branch $(git branch --show-current) --limit 3`
5. `gh run view <RUN_ID> --log-failed`
6. Fix, commit, push, verify green

Exit condition: user finds the failing file and line without help.

## Drill 5: Fork Contribution Loop

Purpose: move from teammate to open-source contributor.

1. `gh repo fork owner/repo --clone`
2. `git remote add upstream https://github.com/owner/repo`
3. `git fetch upstream`
4. Feature branch, small change, push to fork
5. Open upstream PR, respond to maintainer feedback
6. Watch PR merge upstream

Exit condition: seeing their own contribution land in another repo.

## Drill 6: Conflict Resolution

Purpose: normalize merge conflicts instead of fearing them.

1. Two branches from main with conflicting edits
2. Merge branch A into main
3. Merge branch B -> conflict
4. Read markers, choose, `git add`, complete merge

Exit condition: user reads `<<<<<<`, `=======`, `>>>>>>>`, picks one side, and finishes the merge.
