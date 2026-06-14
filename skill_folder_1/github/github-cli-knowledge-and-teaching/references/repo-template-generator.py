#!/usr/bin/env python3
"""Create a simple repo template structure."""

from __future__ import annotations
from pathlib import Path


def create(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "README.md").write_text("# Project Title\n\nShort description.\n")
    (path / ".gitignore").write_text("__pycache__/\nvenv/\n.env\n")
    (path / "CONTRIBUTING.md").write_text("## How to Contribute\n\n- Open an issue\n- Create a branch\n- Open a PR\n")
    (path / "LICENSE").write_text("MIT License — add year and owner.\n")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, default=Path("new-repo"))
    args = ap.parse_args()
    create(args.path)
    print(f"Created repo template at {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
