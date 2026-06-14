# 1-on-1 Coaching Scripts

## Session 1: Status Diagnosis
1. Ask the learner to describe a recent merge/push they found confusing.
2. Recreate the state in a temp repo.
3. Walk `git status` → identify untracked/staged/index states.
4. Fix together.

## Session 2: Branching Practice
1. Ask learner to create two branches with work on each.
2. Merge with and without conflict.
3. Debrief: what differs?

## Session 3: PR Review
1. Have learner open a PR against YOUR repo.
2. You review it, then have them review yours.
3. Walk through approval vs change-request.

## Session 4: Personal Workflow
1. Build a `.gitignore` and commit flow together.
2. Teach `git log --graph --decorate --oneline --all`.
3. Introduce `git stash` with a real interruption scenario.

## Session 5: Recovery / Rescue
1. Simulate the “oh no” moment:
   - detached HEAD
   - force-pushed branch
   - lost commits
2. Introduce `git reflog` and restore pattern.

## Coaching Rules
- Ask “what do you see?” before answering
- Let them type; you narrate
- After they solve it, repeat it once from scratch
