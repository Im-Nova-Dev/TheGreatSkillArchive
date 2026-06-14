#!/usr/bin/env python3
"""
Quiz generator from git-cli-knowledge-and-teaching glossary terms.

Usage:
    python quiz-generator.py all
    python quiz-generator.py beginner
    python quiz-generator.py intermediate
    python quiz-generator.py advanced
    python quiz-generator.py random 5
"""

from __future__ import annotations
import json
import random
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REF = BASE.parent / "references" / "glossary-terms.md"

TERMS = {
    "beginner": [
        ("repository", "A project folder plus a hidden .git folder that stores history."),
        ("commit", "A saved snapshot of your project at one point in time."),
        ("branch", "A movable name for a commit; a separate timeline."),
        ("merge", "Combining two timelines into one."),
        ("clone", "Making a local copy of a remote repository."),
        ("remote", "A URL pointing to another copy of the repo, usually on GitHub."),
        ("origin", "The default name for the remote you cloned from."),
        ("push", "Sending your local commits to a remote."),
        ("pull", "Downloading remote commits and merging them into your current branch."),
        ("fetch", "Downloading remote commits without merging."),
        ("diff", "The line-by-line differences between two states."),
        ("HEAD", "The special pointer that says where you are now."),
        ("working tree", "The files you actually edit on disk."),
        ("staging area", "The temporary list of changes earmarked for the next commit."),
        (".gitignore", "A file that tells Git which files to ignore."),
        ("status", "Current state of the working tree and staging area."),
        ("PR", "A request to merge one branch into another, hosted on GitHub."),
        ("issue", "A GitHub feature for tracking work."),
        ("fork", "A personal copy of someone else's repository under your account."),
        ("star", "GitHub's bookmark feature for repos."),
    ],
    "intermediate": [
        ("reflog", "A local log of where HEAD has moved; useful for recovery."),
        ("cherry-pick", "Copy one commit onto another branch."),
        ("rebase", "Rewrite your branch so it appears to start from a different base."),
        ("squash", "Combine multiple commits into one."),
        ("fast-forward", "When merging, simply moves the branch pointer forward."),
        ("merge commit", "A special commit with two parents, created by git merge."),
        ("detached HEAD", "HEAD points directly to a commit instead of a branch."),
        ("upstream", "The original repo you forked from, used to keep your fork in sync."),
        ("downstream", "A consumer or fork of your repository."),
        ("origin/main", "The main branch as it exists on the remote named origin."),
        ("protection rules", "GitHub settings that enforce review, status checks, or permissions before merging."),
        ("auto-merge", "GitHub feature that merges automatically once checks pass."),
        ("workflow", "A GitHub Actions YAML file describing automated steps."),
        ("run", "One execution of a workflow."),
        ("artifact", "A file produced by a workflow run."),
        ("secret", "Encrypted environment variable for Actions workflows."),
        ("label", "Colored tag attached to issues and PRs."),
        ("review", "Feedback on a PR before merging."),
    ],
    "advanced": [
        ("blob", "Git object that stores file content."),
        ("tree", "Git object that stores directory structure and references to blobs."),
        ("object database", "Everything inside .git/objects; immutable content-addressed storage."),
        ("SHA-1", "The 40-character hash that names every Git object."),
        ("DAG", "Directed acyclic graph; the shape of Git history."),
        ("reachability", "Whether one commit can be reached by following parent links from HEAD."),
        ("rerere", "Reuse recorded resolution; Git remembers how you resolved a conflict."),
        ("bisect", "Binary search through history to find the commit that introduced a bug."),
        ("filter-repo", "Rewrite history by adding/removing files, paths, or messages."),
        ("credential helper", "Program Git uses to remember or cache login credentials."),
        ("mode", "Unix file permission bits stored with each tracked file."),
        ("worktree", "Multiple working trees sharing the same .git directory."),
        ("submodule", "A Git repo inside another Git repo, checked out at a specific commit."),
        ("pre-push hook", "Script that runs before git push."),
        ("pre-commit hook", "Script that runs before git commit."),
    ],
}


def ask(term: str, definition: str) -> bool:
    print(f"Term: {term}")
    input("Press Enter to see definition...")
    print(f"Definition: {definition}")
    return input("Did you know this? (y/n): ").strip().lower() == "y"


def main() -> int:
    args = sys.argv[1:] or ["all"]
    mode, *rest = args
    count = int(rest[0]) if rest and rest[0].isdigit() else None

    if mode == "all":
        pool = [(t, d) for group in TERMS.values() for t, d in group]
    elif mode in TERMS:
        pool = TERMS[mode]
    elif mode == "random":
        pool = [(t, d) for group in TERMS.values() for t, d in group]
        random.shuffle(pool)
        pool = pool[: count or len(pool)]
    else:
        print(f"Unknown mode: {mode}. Use: all beginner intermediate advanced random [count]")
        return 1

    known = 0
    total = len(pool)
    for term, definition in pool:
        if ask(term, definition):
            known += 1

    print(f"Score: {known}/{total} known")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
