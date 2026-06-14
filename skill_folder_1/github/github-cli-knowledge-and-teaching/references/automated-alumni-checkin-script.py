#!/usr/bin/env python3
"""alumni-checkin.py
Generate a friendly weekly check-in message for alumni."""

from __future__ import annotations
import datetime as dt


def main() -> int:
    today = dt.date.today()
    print(f"Hi alumni, it's {today}.")
    print("Quick check-in:")
    print("- One Git win this week?")
    print("- One thing still confusing?")
    print("- One repo you'd like to contribute to?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
