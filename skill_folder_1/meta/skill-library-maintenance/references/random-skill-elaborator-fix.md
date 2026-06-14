# Fix for `random-skill-elaborator.py` Backlog Burn

## Problem (observed 2026-06-06)

The script picks a random item from the backlog, **then** checks if the skill exists. If it exists, it exits with "Skipped" — **without putting the item back** in the backlog. The backlog then refills with `DEFAULT_BACKLOG` (56 items), most of which already have skill directories. Repeated runs burn through the entire backlog, producing only "Skipped" output.

### Symptoms
- Running `python3 /home/nova/.hermes/scripts/random-skill-elaborator.py --extend-missing` repeatedly prints only "Skipped: existing skill technology/..."
- Backlog file (`skill-backlog.json`) keeps getting refilled with DEFAULT_BACKLOG items that already exist
- No progress toward creating new skills

## Root Cause
The `main()` function pops an item, checks `already_exists()`, and on skip it exits early without removing the item from the backlog or trying another item.

## Fix Applied (patch to `/home/nova/.hermes/scripts/random-skill-elaborator.py`)

```python
def main():
    items = load_backlog()
    if not items:
        print("Queue empty; refilling with defaults")
        items = list(DEFAULT_BACKLOG)
        save_backlog(items)

    # Pre-filter against existing skill directories to avoid burning backlog on skips
    from pathlib import Path
    LIBRARY_PATH = Path(LIBRARY).expanduser()
    existing = {d.parent.name for d in LIBRARY_PATH.rglob("*/SKILL.md")}
    available = [item for item in items if safe_slugify(item["slug"]) not in existing]

    if not available:
        print("No novel items in backlog; all remaining items already have skill directories.")
        sys.exit(0)

    idx = random.randrange(len(available))
    item = available.pop(idx)

    # Remove the picked item from the main backlog too (find by slug)
    picked_slug = safe_slugify(item["slug"])
    items = [i for i in items if safe_slugify(i["slug"]) != picked_slug]

    items = maybe_refill(items)
    save_backlog(items)
    path, status = create_skill(item)
    if status == "already exists":
        # Should not happen due to pre-filter, but guard anyway
        print(f"Skipped: existing skill {item['category']}/{picked_slug}")
        sys.exit(0)
    print(f"Created: {safe_slugify(item['category'])}/{picked_slug}")
    print(f"Title : {item['name']}")
    print(f"About : {item['description']}")
    print(f"Path  : {path}")
    print(f"Remaining in backlog: {len(items)}")
    sys.exit(0)
```

## Key Changes
1. **Pre-filter**: Build `existing` set from actual skill directories on disk before picking
2. **Available list**: Only pick from items whose slug doesn't already exist
3. **Early exit with signal**: If `available` is empty, print clear message and exit 0
4. **Backlog cleanup**: Remove the picked item from the main backlog by slug so it doesn't accumulate
5. **Refill only after success**: `maybe_refill()` runs after successful pick, not before

## Result
- No more "Skipped" spam when backlog is exhausted
- Clear signal when no novel items remain
- Backlog shrinks appropriately as skills are created
- Script becomes suitable for cron use without manual intervention