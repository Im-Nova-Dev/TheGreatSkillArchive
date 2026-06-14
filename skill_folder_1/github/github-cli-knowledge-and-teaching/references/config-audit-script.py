#!/usr/bin/env python3
"""config_audit.py
Audit a user Git config for common teaching-relevant settings."""

from __future__ import annotations
import subprocess
import sys

def git(*args: str) -> str | None:
    p = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout.strip()


def main() -> int:
    print("--- Git Config Audit ---")
    user = git("config", "--global", "user.name")
    email = git("config", "--global", "user.email")
    print(f"user.name: {user or 'MISSING'}")
    print(f"user.email: {email or 'MISSING'}")

    aliases = git("config", "--global", "--list")
    alias_count = sum(1 for line in aliases.splitlines() if line.startswith("alias.")) if aliases else 0
    print(f"aliases: {alias_count}")

    # Check recommended aliases
    rec = {"s": "status -s", "lg": "log --oneline --graph --decorate --all"}
    for key, val in rec.items():
        actual = git("config", "--global", f"alias.{key}")
        print(f"  alias.{key}: {'ok' if actual == val else 'missing'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
