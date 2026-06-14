#!/usr/bin/env python3
"""course-packet-pdf-generator.py
Generate a printable PDF packet from selected markdown references."""

from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path


def build_pdf(sources: list[Path], out: Path) -> int:
    combined = "\n\n".join(s.read_text(encoding="utf-8") for s in sources)
    md = out.with_suffix(".md")
    md.write_text(combined, encoding="utf-8")
    print(f"Wrote combined markdown: {md}")
    try:
        subprocess.run([
            "pandoc", str(md), "-o", str(out),
            "--pdf-engine=xelatex",
            "-V", "geometry:margin=1in",
        ], check=True)
    except FileNotFoundError:
        print("pandoc not found; keeping markdown only.")
        return 1
    print(f"PDF generated: {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, nargs="+", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    return build_pdf(args.src, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
