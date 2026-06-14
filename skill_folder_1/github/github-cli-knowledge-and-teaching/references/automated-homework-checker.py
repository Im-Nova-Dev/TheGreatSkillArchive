#!/usr/bin/env python3
"""Simple homework checker for Git assignments.

Usage:
  python3 automated-homework-checker.py --repo /path/to/student/repo

Returns exit code 0 if all checks pass, 1 otherwise.
 Prints human-readable report.
"""

from __future__ import annotations
import argparse
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
        return [("git repo", False, ".git directory missing")]

    status = run(["git", "status", "--porcelain"], repo)
    clean = status == ""
    results.append(("clean working tree", clean, status if not clean else "ok"))

    log = run(["git", "log", "--oneline", "--all"], repo)
    has_commits = bool(log.splitlines())
    results.append(("has commits", has_commits, f"{len(log.splitlines())} commits"))

    branches = run(["git", "branch", "--list"], repo)
    has_branch = bool(branches)
    results.append(("has branch", has_branch, branches))

    readme = repo / "README.md"
    results.append(("has README.md", readme.exists(), readme.name))

    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    args = ap.parse_args()

    results = check(args.repo)
    passed = 0
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}: {detail}")
        if ok:
            passed += 1

    print(f"\nResult: {passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
