# Visual Handouts — Git and GitHub

These are text diagrams meant to be copied into notes, docs, or slide decks.

---

## Handout 1 — The Three Areas

```
working tree   <-- you edit files here
     |
  git add
     |
 staging area  <-- next-commit preview
     |
  git commit
     |
 .git repo     <-- permanent history
```

---

## Handout 2 — First Commits Timeline

```
main:  A -- B -- C
                |
feature:        D -- E
```

`main` and `feature` share A-B-C, then diverge.

---

## Handout 3 — Merge Commit

Before:
```
main:       M1 -- M2
                      \
feature:                F1
```

After `git merge feature`:
```
main:       M1 -- M2 -- M3 (merge commit)
                      \      /
feature:                F1
```

---

## Handout 4 — Fast-Forward

Before:
```
main:       M1 -- M2
feature:                F1
```

After `git merge feature`:
```
main:       M1 -- M2 -- F1
```

No merge commit; `main` simply moves forward.

---

## Handout 5 — Rebase

Before:
```
main:                M2
feature:  F1 -- F2
```

After rebasing `feature` onto `main`:
```
main:                M2 -- F1' -- F2'
feature:  F1 -- F2
```

The branch is rewritten relative to the new base.

---

## Handout 6 — Fork Contribution Flow

```
upstream owner/repo
        |
      fork under your account
        |
     clone to your laptop
        |
     work on branch
        |
     push to your fork
        |
     open PR to upstream
```

---

## Handout 7 — Remote Names

```
origin      = your clone remote
upstream    = the repo you forked from
```

Common flow:
```
git fetch origin
git fetch upstream
git rebase upstream/main
git push origin
```

---

## Handout 8 — PR States

```
open -> review -> changes requested -> updated -> approved -> merged
                                            \
                                              closed / not planned
```

---

## Handout 9 — Command Safety Levels

```
L1 read-only:      git status git log git diff git branch
L2 additive:       git add git commit git push git fetch
L3 rewrite local:  git commit --amend git rebase -i
L4 destructive:    git reset --hard git push --force
L5 recovery:       git reflog git bisect
```
