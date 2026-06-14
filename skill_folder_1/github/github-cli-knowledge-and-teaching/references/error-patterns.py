#!/usr/bin/env python3
"""
Git and GitHub teaching prompt generator.

Produces a randomized prompt for a learner to diagnose and fix.
Run this in lesson mode: give one prompt at a time and ask the learner
to predict the right command before revealing the answer.

Categories:
- git state
- remote
- branch
- merge / rebase
- github workflow
"""

from __future__ import annotations
import json
from pathlib import Path
from textwrap import indent

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "prompts" / "prompts.json"

PROMPTS = {
    "git_state": [
        {
            "name": "unstaged change visible",
            "scenario": "You edited README.md. Run `git status`. What does it show?",
            "expected": [
                "modified:   README.md",
                "no changes added to commit",
            ],
            "fix": "git add README.md",
        },
    ],
    "remote": [
        {
            "name": "remote not set",
            "scenario": "`git push` fails. The learner hasn't set a remote. What should they do?",
            "expected": ["git remote add origin <url>", "git remote -v"],
            "fix": "git remote add origin <url>",
        },
    ],
    "branch": [
        {
            "name": "commit to wrong branch",
            "scenario": "You committed a feature change to `main` by accident. You want that change on `feat/foo`. What do you do?",
            "expected": [
                "git switch feat/foo",
                "git cherry-pick <sha>",
            ],
            "fix": "git cherry-pick <sha>",
        },
    ],
    "merge_rebase": [
        {
            "name": "divergent history",
            "scenario": "Your branch and `main` have both moved since you started. `git merge main` gives a merge commit. Describe this in plain English.",
            "expected": [
                "merge commit",
                "combines two timelines",
                "Git can't fast-forward",
            ],
            "fix": "Explain merge commit conceptually.",
        },
    ],
    "github_workflow": [
        {
            "name": "review requested changes",
            "scenario": "A reviewer asked for changes on PR 12 before merging. What are the next 3 terminal commands?",
            "expected": [
                "edit files",
                "git add",
                "git commit",
                "git push",
                "gh pr review 12 --comment",
            ],
            "fix": "edit, stage, commit, push, reply. PR auto-updates.",
        },
    ],
}


def build_prompts() -> list[dict]:
    items = []
    for category, entries in PROMPTS.items():
        for e in entries:
            items.append({
                "id": f"{category}::{e['name']}",
                "category": category,
                "name": e["name"],
                "scenario": e["scenario"],
                "expected_keywords": e["expected"],
                "answer": e["fix"],
            })
    return items


def main() -> int:
    prompts = build_prompts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(prompts, indent=2), encoding="utf-8")
    print(f"wrote {len(prompts)} prompts to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
