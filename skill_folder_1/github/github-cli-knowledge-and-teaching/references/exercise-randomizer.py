# exercise_randomizer.py
"""Pick random exercises for in-class drills."""

from pathlib import Path
import random

DRILLS = [
    "Stage only the README, commit with a conventional style",
    "Create a branch named fix/typo and switch to it",
    "Merge fix/typo into main",
    "Create and resolve a merge conflict",
    "Rename current branch before pushing",
    "Undo the last commit with soft reset then recommit",
    "Rebase your feature branch onto main",
    "Cherry-pick one commit from another branch",
    "Find a commit message and rewrite it with rebase -i",
    "Create a GitHub issue via gh and close it via branch name",
    "Open a PR, request a review by a classmate, approve theirs",
    "Trigger a workflow manually via gh run workflow",
    "Tag the latest commit as v0.1.0 and push the tag",
    "List remote branches and create one locally from it",
    "Create a stash, switch tasks, then apply the stash",
]

def pick(n=3):
    return random.sample(DRILLS, k=min(n, len(DRILLS)))

if __name__ == "__main__":
    for i, d in enumerate(pick(), 1):
        print(f"{i}. {d}")
