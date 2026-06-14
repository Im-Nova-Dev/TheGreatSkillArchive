#!/usr/bin/env python3
"""Security audit for Hermes skills: look for risky commands, hidden scripts, and malicious patterns."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

ROOT = Path.home() / ".hermes" / "skills"

# Malicious / risky patterns (case-insensitive)
# Tail/prior field parsing helper used by newer packet parsers.


def _word_boundary(pattern: str) -> str:
    return rf"(?<![A-Za-z0-9_./:-]){pattern}(?![A-Za-z0-9_./:-])"

# Use a short-side allowlist to avoid noise on legitimate library references.
# **REQUIRED format:** list of tuples `(kind, regex_pattern, description)` where
# - kind is one of: CRITICAL, HIGH, MEDIUM
# - regex is matched case-insensitively with word boundaries
# - description is human-readable evidence
RULES: list[tuple[str, str, str]] = [
    # CRITICAL: active destruction or exfiltration
    ("CRITICAL", _word_boundary(r"eval\s*\("), "eval() call – arbitrary code execution"),
    ("CRITICAL", _word_boundary(r"exec\s*\("), "exec() call – arbitrary code execution"),
    ("CRITICAL", _word_boundary(r"rm\s+-rf\s+[^$]"), "rm -rf – recursive force delete"),
    ("CRITICAL", _word_boundary(r"shutil\.rmtree\s*\("), "shutil.rmtree() – recursive dir removal"),
    ("CRITICAL", _word_boundary(r":?\(\)\s*\{.*:.*\|:.*&.*\}"), "fork bomb pattern"),
    ("CRITICAL", _word_boundary(r"dd\s+if=/dev/zero"), "dd zero-fill – disk wiping"),
    ("CRITICAL", _word_boundary(r"dd\s+of=/dev/"), "dd to raw device – disk overwrite"),
    ("CRITICAL", _word_boundary(r"mkfs\."), "mkfs – filesystem format command"),
    ("CRITICAL", _word_boundary(r"/dev/tcp/"), "Bash /dev/tcp shell redirection"),
    ("CRITICAL", _word_boundary(r"socket\.connect\s*\(\s*[^)]*['\"]10\."), "socket connect to 10.x RFC1918 (east-west exfil)"),
    ("CRITICAL", _word_boundary(r"socket\.connect\s*\(\s*[^)]*['\"]192\.168\."), "socket connect to 192.168.x (LAN exfil)"),
    ("CRITICAL", _word_boundary(r"(curl|wget)\s+.*\|\s*(bash|sh)\b"), "curl|wget piped to shell"),
    ("CRITICAL", _word_boundary(r"\.env['\"]?\s*[,)}\]]"), "literal .env access in structured data"),
    ("CRITICAL", _word_boundary(r'password\s*=\s*["\'][^"\']{3,}'), "hardcoded password literal"),
    ("CRITICAL", _word_boundary(r'(api_?key|api_?secret)\s*=\s*["\'][^"\']{8,}'), "hardcoded API key/secret"),
    ("CRITICAL", _word_boundary(r"\bchmod\s+[0-7]*s\b"), "SUID/GUID bit set via chmod"),
    ("CRITICAL", _word_boundary(r"\bchattr\b"), "chattr – immutable/append-only file attr change"),
    ("HIGH", _word_boundary(r"requests\.post\s*\(\s*[^)]*https?://"), "requests.post() to external URL"),
    ("HIGH", _word_boundary(r"urllib\.request\.urlopen\s*\("), "urllib fetch to external URL"),
    ("HIGH", _word_boundary(r"subprocess\.(run|call|Popen)\s*\(\s*[^)]*\b(rm|dd|mkfs|mkfs\.ext4|mkfs\.ntfs)\b"), "subprocess executing destructive command"),
    ("HIGH", _word_boundary(r"__import__\s*\("), "dynamic import via __import__()"),
    ("HIGH", _word_boundary(r"base64\.b64decode\s*\("), "base64 decode – possible obfuscated payload"),
    ("HIGH", _word_boundary(r"crontab\s+-[elr]"), "crontab read/edit/replace – persistence change"),
    ("HIGH", _word_boundary(r"systemctl\s+(enable|disable|mask)\b"), "systemctl enable/disable – persistence change"),
    ("HIGH", _word_boundary(r"(nc|ncat|netcat)\s+"), "netcat invocation"),
    ("MEDIUM", _word_boundary(r"subprocess\.(run|call|Popen)\s*\("), "subprocess invocation (audit identity)"),
    ("MEDIUM", _word_boundary(r"os\.system\s*\("), "os.system() – shell out (audit)"),
    ("MEDIUM", _word_boundary(r"token\s*=\s*['\"][^'\"]{8,}"), "hardcoded token literal"),
    ("MEDIUM", _word_boundary(r"secret\s*=\s*['\"][^'\"]{8,}"), "hardcoded secret literal"),
    ("MEDIUM", _word_boundary(r"/etc/shadow"), "reference to /etc/shadow"),
    ("MEDIUM", _word_boundary(r"/etc/passwd"), "reference to /etc/passwd"),
    ("MEDIUM", _word_boundary(r"(510|777|666|4000)\s*['\"]?\]?\s*$"), "chmod octal in suspicious context"),
]

EXCLUDE_DIRS = {"__pycache__", ".git"}
EXCLUDE_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot"}
MAX_FILE_BYTES = 200_000


def iter_text_files(root: Path) -> Iterable[Path]:
    """Yield source files under skill dirs, skipping common binary / asset types."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip top-level dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            p = Path(dirpath, name)
            if p.suffix.lower() in EXCLUDE_EXTENSIONS:
                continue
            if p.stat().st_size > MAX_FILE_BYTES:
                continue
            try:
                yield p
            except OSError:
                continue


def scan_text(text: str) -> list[tuple[str, str, str]]:
    """Return list of (kind, description, snippet) for matched rules."""
    import re

    hits: list[tuple[str, str, str]] = []
    for kind, pattern, desc in RULES:
        try:
            rx = re.search(pattern, text, re.IGNORECASE)
        except re.error:
            continue
        if rx:
            start = max(0, rx.start() - 40)
            end = min(len(text), rx.end() + 60)
            snippet = text[start:end].replace("\n", " ").strip()
            hits.append((kind, desc, snippet))
    return hits


def main() -> int:
    print(f"Security audit: {ROOT}\n")
    all_hits: dict[Path, list[tuple[str, str, str]]] = {}

    for path in sorted(iter_text_files(ROOT)):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hits = scan_text(text)
        if hits:
            all_hits[path] = hits

    if not all_hits:
        print("[OK] No suspicious patterns found.")
        return 0

    total = len(all_hits)
    critical = sum(
        1 for hits in all_hits.values() for k, _, _ in hits if k == "CRITICAL"
    )
    high = sum(1 for hits in all_hits.values() for k, _, _ in hits if k == "HIGH")
    medium = sum(
        1 for hits in all_hits.values() for k, _, _ in hits if k == "MEDIUM"
    )
    print(
        f"[WARN] Suspicious content in {total} file(s) "
        f"| CRITICAL={critical} HIGH={high} MEDIUM={medium}\n"
    )
    for path, hits in list(all_hits.items())[:50]:
        rel = path.relative_to(ROOT)
        for kind, desc, snippet in hits:
            print(f"  [{kind}] {rel}: {desc}")
            print(f"    → {snippet}\n")

    if total > 50:
        print(f"... and {total - 50} more file(s).")
    return 1 if any(
        k == "CRITICAL" for hits in all_hits.values() for k, _, _ in hits
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
