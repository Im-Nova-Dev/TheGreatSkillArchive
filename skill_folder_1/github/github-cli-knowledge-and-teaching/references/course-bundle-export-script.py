#!/usr/bin/env python3
"""Export the teaching skill as a distributable bundle."""

from __future__ import annotations
import shutil
import sys
from pathlib import Path


def bundle(src: Path, out: Path) -> int:
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    zip_path = out.with_suffix(".zip")
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", root=out)
    print(f"Bundle exported: {zip_path}")
    return 0


def main() -> int:
    src = Path(__file__).resolve().parent.parent
    out = src / "bundle"
    return bundle(src, out)


if __name__ == "__main__":
    raise SystemExit(main())
