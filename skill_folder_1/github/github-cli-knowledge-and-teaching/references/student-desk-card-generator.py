#!/usr/bin/env python3
"""Generate a printable desk card with common Git commands."""

from __future__ import annotations

CARD = """
+-------------------------------------+
|            GIT DESK CARD            |
+-------------------------------------+
| Check state:    git status          |
| Stage:          git add -A          |
| Commit:         git commit -m ""    |
| History:        git log --oneline --graph
| New branch:     git switch -c <n>   |
| Merge:          git merge <n>       |
| Push:           git push -u origin <n>
| PR:             gh pr create        |
| Recover:        git reflog          |
+-------------------------------------+
"""


def main() -> int:
    print(CARD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
