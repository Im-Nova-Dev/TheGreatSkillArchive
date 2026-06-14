# Backlog Injection Workflow — Session 2026-06-06

## Context
The `random-skill-elaborator.py --extend-missing` script repeatedly skipped because all 56 DEFAULT_BACKLOG items already had skill directories under `~/.hermes/skills/technology/`. The backlog refilled with defaults on each run, producing only "Skipped" output.

## Root Cause (matches documented pitfall)
1. Script pops random item → checks existence → if exists, prints "Skipped" and **exits without re-adding to backlog**
2. Backlog refills with `DEFAULT_BACKLOG` (56 items, all already skilled)
3. Repeated runs burn through backlog with zero new skills created

## Workaround Applied
1. **Listed existing skills** to confirm coverage:
   ```bash
   ls -1 ~/.hermes/skills/technology/ | wc -l  # 52 skills
   ```

2. **Injected 8 new technology skills** into `/home/nova/.hermes/data/skill-backlog.json`:
   - `ml-model-registry-gateway`
   - `federated-learning-coordinator`
   - `wasm-sandbox-runtime`
   - `vector-index-optimizer`
   - `prompt-injection-scanner`
   - `multi-region-failover-orchestrator`
   - `code-sandbox-executor`
   - `distributed-trace-correlator`

3. **Ran script repeatedly** until all 8 created (some runs still hit existing backlog duplicates):
   ```bash
   python3 /home/nova/.hermes/scripts/random-skill-elaborator.py --extend-missing
   ```

## Result
All 8 new skills created at `~/.hermes/skills/technology/<slug>/SKILL.md` with starter templates (~1KB each).

## Permanent Fix Needed
Pre-filter backlog against existing skill directories before picking (as documented in skill):
```python
from pathlib import Path
LIBRARY = Path("~/.hermes/skills").expanduser()
existing = {d.parent.name for d in LIBRARY.rglob("*/SKILL.md")}
available = [item for item in backlog if item["slug"] not in existing]
# Pick from `available` instead of full backlog
```

## Recommendation
- Patch `random-skill-elaborator.py` with the pre-filter, OR
- Wrap cron with a pre-filter step that rewrites `skill-backlog.json` with only unskilled items, OR
- Replace script-driven creation with class-level skill **expansion** (add references/, templates/, scripts/ to existing thin skills) per the maintenance guidance.