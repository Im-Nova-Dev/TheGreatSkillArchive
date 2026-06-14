#!/usr/bin/env python3
"""Generate simple text-based branch diagrams."""

from __future__ import annotations

def diagram(commits: list[str]) -> str:
    lines = ["git log --oneline --graph --all", ""]
    for i, c in enumerate(commits):
        if i == len(commits) - 1:
            lines.append(f"* {c}")
        else:
            lines.append(f"* {c}")
            lines.append("|")
    return "\n".join(lines)


def main() -> int:
    commits = [
        "Initial commit",
        "Add README",
        "Start feature",
        "Finish feature",
        "Merge feature",
        "Hotfix",
    ]
    print(diagram(commits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
