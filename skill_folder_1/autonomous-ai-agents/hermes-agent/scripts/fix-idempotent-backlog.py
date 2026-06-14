#!/usr/bin/env python3
"""
Patch for deep-research-pack-creator.py to make it idempotent.

Applies Fix Pattern 1: Conditional Backlog Removal
Only removes item from backlog on SUCCESSFUL creation, not on skip.

Also fixes backlog file path bug:
- Original: `/home/nova/.hermes/scripts/../data/deep-research-backlog.json` (wrong)
- Fixed: `/home/nova/.hermes/data/deep-research-backlog.json` (correct)
"""

import sys

SCRIPT_PATH = "/home/nova/.hermes/scripts/deep-research-pack-creator.py"

def main():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    # Fix 1: Backlog file path correction
    # Original: BACKLOG_FILE = os.path.join(SCRIPT_DIR, "..", "data", "deep-research-backlog.json")
    # This resolves to /home/nova/.hermes/scripts/data/deep-research-backlog.json (WRONG)
    # Correct path: /home/nova/.hermes/data/deep-research-backlog.json
    old_backlog_path = 'BACKLOG_FILE = os.path.join(SCRIPT_DIR, "..", "data", "deep-research-backlog.json")'
    new_backlog_path = 'BACKLOG_FILE = os.path.join(os.path.expanduser("~/.hermes"), "data", "deep-research-backlog.json")'

    if old_backlog_path not in content:
        print("WARNING: Could not find backlog path line. Script may have changed.")
    else:
        content = content.replace(old_backlog_path, new_backlog_path)
        print("Fixed backlog file path")

    # Fix 2: Conditional backlog removal (Fix Pattern 1)
    # Find the problematic block (lines ~168-182)
    old_block = '''    idx = random.randrange(len(items))
    item = items[idx]
    items = [entry for entry in items if entry is not item]
    save_backlog(items)
    category = item.get("category", "technology")
    base_slug = item.get("slug", safe_slugify(item.get("name", "topic")))
    topic = item.get("name", base_slug.replace("-", " ").title())
    seeds = item.get("seeds", [base_slug])
    if not seeds:
        seeds = [base_slug.replace("-", " ")]
    cat = safe_slugify(category)
    slug = base_slug
    if already_exists(cat, slug):
        print(f"Skipped: existing skill {cat}/{slug}")
        sys.exit(1)'''

    new_block = '''    idx = random.randrange(len(items))
    item = items[idx]
    category = item.get("category", "technology")
    base_slug = item.get("slug", safe_slugify(item.get("name", "topic")))
    topic = item.get("name", base_slug.replace("-", " ").title())
    seeds = item.get("seeds", [base_slug])
    if not seeds:
        seeds = [base_slug.replace("-", " ")]
    cat = safe_slugify(category)
    slug = base_slug
    if already_exists(cat, slug):
        # Silent skip: exit 0 with no output (per Silent skip pattern in hermes-cron-patterns)
        # Do NOT remove from backlog on skip - keep item for future runs
        sys.exit(0)
    # Only remove from backlog on SUCCESSFUL creation:
    items = [entry for entry in items if entry is not item]
    save_backlog(items)'''

    if old_block not in content:
        print("ERROR: Could not find expected code block for conditional removal. Script may have changed.")
        print("Search for 'items = [entry for entry in items if entry is not item]'")
        sys.exit(1)

    new_content = content.replace(old_block, new_block)

    with open(SCRIPT_PATH, "w") as f:
        f.write(new_content)

    print(f"Patched {SCRIPT_PATH}")
    print("Applied Fix Pattern 1: Conditional Backlog Removal")
    print("Applied Fix: Backlog file path correction")
    print("Now the script only removes from backlog on successful skill creation.")
    print("Now the script uses the correct backlog path: ~/.hermes/data/deep-research-backlog.json")

if __name__ == "__main__":
    main()