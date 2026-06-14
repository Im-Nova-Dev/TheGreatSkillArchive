#!/usr/bin/env python3
"""Generate a competency rubric from a list of skills."""

from __future__ import annotations

def rubric(skills: list[str]) -> str:
    lines = ["| Skill | Level 1 | Level 2 | Level 3 | Level 4 |", "|-------|---------|---------|---------|---------|"]
    for skill in skills:
        lines.append(
            f"| {skill} | Needs hand-holding | With hints | Independent | Coaches others |"
        )
    return "\n".join(lines)


def main() -> int:
    skills = [
        "git status reading",
        "Commit message hygiene",
        "Branch navigation",
        "Merge without conflict",
        "Merge conflict resolution",
        "Push / pull / fetch",
        "PR creation",
        "PR review",
        "GitHub Actions basics",
        "Git alias usage",
    ]
    print(rubric(skills))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
