# Live Demo Script Pack

Use this for instructor-led demos. Each script has timing, narration, commands, and checkpoints.

---

## Demo A — First Repo in 5 Minutes

Timing: 5 minutes
Audience: complete beginner
Goal: prove Git is usable immediately

Setup:
- Open terminal
- Verify `git --version` and `gh --version`

Script:
"Git remembers everything. GitHub shares it. Let's save something and make it visible."

Commands:
- `mkdir live-demo && cd live-demo`
- `git init`
- `echo "# live-demo" > README.md`
- `git add README.md`
- `git commit -m "docs: add README"`
- `git status`
- `git log --oneline`
- `gh repo create live-demo --public --source . --push`
- `gh browse`

Checkpoint:
- repo visible on GitHub
- learner can describe what `git push` did

---

## Demo B — Branch Timeline

Timing: 8 minutes
Audience: beginner
Goal: branches are labels, not copies

Commands:
- `git init demo && cd demo`
- `echo main > file.txt && git add . && git commit -m "init"`
- `git switch -c feature`
- `echo feature > file.txt && git add . && git commit -m "feature"`
- `git switch main`
- `git log --graph --oneline --all`

Checkpoint:
- learner explains why `file.txt` changed back on `main`

---

## Demo C — Conflict Resolution

Timing: 10 minutes
Audience: beginner
Goal: conflicts are normal and solvable

Commands:
- `git init conflicts && cd conflicts`
- `echo base > shared.txt && git add . && git commit -m "init"`
- `git switch -c A && echo A > shared.txt && git add . && git commit -m "A"`
- `git switch main`
- `git switch -c B && echo B > shared.txt && git add . && git commit -m "B"`
- `git switch main && git merge A && git merge B`

Checkpoint:
- learner reads markers and resolves without panic

---

## Demo D — Review Loop

Timing: 12 minutes
Audience: beginner/intermediate
Goal: full PR review workflow

Commands:
- create repo with CI-friendly workflow
- feature branch, change, push
- `gh pr create`
- `gh pr checks --watch`
- `gh pr review N --request-changes`

Offer learner a chance to fix and re-push.

Checkpoint:
- reviewer approves and merges

---

## Demo E — Recovery Drills

Timing: 10 minutes
Audience: beginner
Goal: confidence in mistakes

Commands:
- `git init recovery && cd recovery`
- `echo a > a.txt && git add . && git commit -m "a"`
- `echo b > b.txt && git add . && git commit -m "b"`
- `git reset --hard HEAD~1`
- `git reflog`
- `git checkout -b recovered HEAD@{2}`

Checkpoint:
- learner states aloud: “Reflog is my time machine”

---

## Demo F — CI Diagnosis

Timing: 10 minutes
Audience: intermediate
Goal: read logs instead of fearing red checks

Commands:
- create repo with intentionally failing workflow
- `gh pr create`
- `gh pr checks --watch`
- `gh run list`
- `gh run view <id> --log-failed`
- fix code, commit, push, verify green

Checkpoint:
- learner identifies failing step from log without help
