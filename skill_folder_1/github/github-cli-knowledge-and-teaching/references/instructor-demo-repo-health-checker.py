#!/usr/bin/env python3
"""Verify a demo repo is clean and ready for a session."""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        return f"ERROR: {' '.join(cmd)}\n{p.stderr.strip()}"
    return p.stdout.strip()


def check(repo: Path) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    if not (repo / ".git").exists():
        return [("git repo", False, ".git missing")]

    status = run(["git", "status", "--porcelain"], repo)
    results.append(("clean", status == "", status or "ok"))

    log = run(["git", "log", "--oneline", "--all"], repo)
    lines = log.splitlines()
    results.append(("has commits", bool(lines), f"{len(lines)} commits"))

    branches = run(["git", "branch", "-a"], repo)
    results.append(("has branches", bool(branches), branches))

    return results


def main() -> int:
    repo = Path(".").resolve()
    results = check(repo)
    passed = 0
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}: {detail}")
        if ok:
            passed += 1
    return 0 if passed == len(results) else 1
