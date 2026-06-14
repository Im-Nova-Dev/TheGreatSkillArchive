# Idempotent Creator Cron Pattern

## Problem: Backlog Depletion on Skip

The `deep-research-pack-creator.py` script (and similar creator crons) has a flaw: **it removes the picked item from the backlog even when skipping because the skill already exists**.

```python
# Line 168-171 in deep-research-pack-creator.py
idx = random.randrange(len(items))
item = items[idx]
items = [entry for entry in items if entry is not item]  # REMOVES ALWAYS
save_backlog(items)

# Then on line 180-182:
if already_exists(cat, slug):
    print(f"Skipped: existing skill {cat}/{slug}")
    sys.exit(1)  # Exit AFTER removing from backlog
```

## Consequence

- All 10 topics in `TOPICS_RAW` already exist as skills
- Each run picks one, removes it from backlog, finds skill exists, skips
- Backlog shrinks until < 3 items, then refills from `TOPICS_RAW` (same 10 topics)
- **Infinite cycle: script will always skip, never creates anything new**

## Fix Pattern 1: Conditional Backlog Removal

Only remove from backlog on successful creation. Also apply silent skip behavior (exit 0, no output):

```python
if already_exists(cat, slug):
    # Silent skip: exit 0 with no output
    # Do NOT remove from backlog on skip
    sys.exit(0)

# Only here if creating:
items = [entry for entry in items if entry is not item]
save_backlog(items)
```

## Fix Pattern 2: Pre-filter Backlog

Filter out already-existing skills when loading/initializing backlog:

```python
def load_backlog():
    items = ...  # load from file or TOPICS_RAW
    # Filter: keep only items whose skill does NOT exist
    filtered = [i for i in items if not already_exists(i.get("category"), i.get("slug"))]
    if not filtered:
        print("All backlog topics already exist as skills. Exiting silently.")
        sys.exit(0)
    return filtered
```

## Fix Pattern 3: Separate "Available" vs "Completed" Lists

Track completed topics separately so the backlog naturally drains and stays empty when done:

```json
// backlog.json
{
  "available": [...],
  "completed": [...]
}
```

## General Rule for Creator Crons

**A creator cron that skips must NOT mutate the backlog.** The backlog represents "work to try." If the work was already done (skill exists), the item should stay available for other potential uses, or be moved to a "completed" archive only on actual success.

## Applied To This Script

The `deep-research-pack-creator.py` at `~/.hermes/scripts/deep-research-pack-creator.py` needs one of the above fixes to become productive. Until fixed, it will produce zero new skills and log "Skipped" on every run.

## Current Status (Confirmed 2026-06-06)

- All 10 `TOPICS_RAW` topics already exist as skills under `~/.hermes/skills/` with `SKILL.md` + 3 reference files each
- Backlog (`deep-research-backlog.json`) contains 4 items — all 4 already exist as skills
- Token log (`token-usage-log.jsonl`) shows 20 successful `Created deep pack` entries total
- Script behavior confirmed: picks random item → removes from backlog → finds skill exists → exits 1 with "Skipped"
- **Result**: Infinite skip cycle; zero new skills produced on every run until fix applied