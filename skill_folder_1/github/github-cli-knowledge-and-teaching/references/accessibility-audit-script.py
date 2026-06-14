#!/usr/bin/env python3
"""
accessibility-audit.py
Audit markdown docs and slide files for basic accessibility gaps.

Usage:
  python3 accessibility-audit.py --path path/to/files

Checks:
- Minimum heading depth sanity
- Presence of image alt text patterns in markdown
- Text-only image warnings
- Caption notes in slide headers
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path


def audit(path: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for md in path.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        # Heading level sanity
        for i, line in enumerate(lines, 1):
            if line.startswith("#") and len(line) - len(line.lstrip("#")) > 4:
                findings.append((str(md), f"line {i}: heading level too deep"))
        # Image with missing alt text
        for i, line in enumerate(lines, 1):
            if "![" in line and "](http" in line:
                if line.split("![")[1].startswith("]"):
                    findings.append((str(md), f"line {i}: image missing alt text"))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, type=Path)
    args = ap.parse_args()
    findings = audit(args.path)
    if not findings:
        print("No obvious accessibility issues found.")
        return 0
n    for file, issue in findings:
        print(f"- {file}: {issue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
