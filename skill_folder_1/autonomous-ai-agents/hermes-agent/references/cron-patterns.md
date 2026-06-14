---
title: Cron Patterns Reference
source: formerly hermes-cron-patterns
---

# Cron Patterns Reference

## Longevity Rule

`cronjob action='create'` defaults to one-shot behavior in some environments. To make a job recurring, set `repeat=0` immediately after creation or include it in the initial create call if supported.

```python
cronjob(action="create", repeat=0, schedule="every 10m", ...)
```

Repeat values:
- `repeat=0` or `repeat=-1` — repeat forever
- `repeat=1` — run once
- omit `repeat` for default one-shot behavior

## Schedule Syntax

Use only the supported forms:
- Interval: `every 30m`, `every 2h`, `every 15m`, `every 1m`
- Duration/cron: `0 */6 * * *`, `0 9 * * *`
- Timestamp: `2026-06-01T09:00:00`

Unsupported forms:
- `@every 3m` — rejected
- bare durations like `3m` alone — not equivalent to an interval here

## Script Placement Rule

`script` must be a bare filename relative to `~/.hermes/scripts/`. If the script lives elsewhere, either move/copy it into `~/.hermes/scripts/` or invoke it from a wrapper script in that directory.

## Silent Skip Pattern

For collection jobs that should not spam the user when nothing new is found, use this prompt structure:

```
Every run:
1. Do X.
2. If no fresh result appears, skip silently.
3. Otherwise deliver a short summary.
```

`no_agent=True` + `script=...` delivers the script's stdout as the message. Empty stdout means silent delivery.

## Toolset Restriction

Limit cron agent toolsets to only what is needed. Examples:
- `["web"]` for research/intel collection
- `["terminal", "file"]` for maintenance/audit scripts
- `["terminal"]` for shell-only checks

## Chaining Skills

Attach existing skills to a cron via `skills=["skill-library-maintenance"]`. Use umbrella maintenance skills for guardrails on skill-creation jobs.

## Common Schedules

- every 10m
- 0 */6 * * *
- 0 9 * * *
- 2026-06-01T09:00:00

## Telegram Delivery Contract

**Official pattern:** do NOT call `send_message`. Cron runtime automatically delivers the agent's final response to the bound Telegram target for this workspace. The assistant only needs to produce the message text as its final response, with targeting context embedded if the runtime requires it.

Target chat for this workspace: `8760897362` (`telegram`).

**Fallback/list format** (when explicit Telegram delivery metadata is needed in the response):
```
If a dedicated Telegram-sending tool or Hermes integration is available in this environment,
it should target chat_id `8760897362` with target `telegram`.
```

For review: look to `references/target_chats.md` for canonical bound chat IDs.

## Repeating Skill-Update Cron with Tool Output

For recurring skill-growth reports:
1. Preserve prior state in `/tmp/skill-tracker-state.json` with `{"last_count":N,"last_run":"ISO"}`.
2. On each run, read state, compute delta from `skills_list`, then overwrite the state file.
3. Send only the final formatted message in one `send_message` call; do not also try to log it as a separate side effect unless explicitly requested.

## Math & Theory Intel Collection Cron Pattern

See `references/math-theory-intel-collection.md` for the full pattern covering mathematics, theoretical computer science, and quantitative theory intel collection (arXiv, math blogs, conferences).

## Science Intel Collection Cron Pattern

Use this when the cron job is `find item -> save intel -> create or enhance teaching skill`.

1. Search the existing skill tree first. If a class-level teaching skill already covers the topic, enhance it; do not create a new narrow skill.
2. After finding a substantively new item, check `/home/nova/.hermes/intel/science/topic-index.md` for the mapped topic name before writing a new intel file or creating a new skill.
3. Derive the topic key as `lowercase, hyphens, no dates`, for example `muon-g-2-magnetic-moment`.
4. If the index already contains that key under a different date prefix, treat the item as already indexed unless the new item materially changes the science; otherwise skip creating a duplicate skill.
5. When adding a new class-level science umbrella, place it under the matching category (`physics`, `quantum`, `biotech`, etc.) and update `topic-index.md` with both the intel file and the skill slug.

## Finance Intel Collection Cron Pattern

Use this when the cron job is `find item -> save intel -> create or enhance teaching skill` for trading, market microstructure, quant strategies, derivatives, crypto/DeFi, macro, or portfolio theory.

1. Search the existing skill tree first (`skills_list(category="finance-strategies")`). If a class-level teaching skill already covers the topic, enhance it; do not create a new narrow skill.
2. After finding a substantively new item, check `/home/nova/.hermes/intel/finance/knowledge-index.md` (and `/home/nova/.hermes/skills/finance/knowledge-index.md`) for the mapped topic name before writing a new intel file or creating a new skill.
3. Derive the topic key as `lowercase, hyphens, no dates`, for example `variance-risk-premium`, `funding-rate-arbitrage`, `order-flow-imbalance`.
4. If the index already contains that key under a different date prefix, treat the item as already indexed unless the new item materially changes the strategy; otherwise skip creating a duplicate skill.
5. When adding a new class-level finance umbrella, place it under `finance-strategies/` and update both knowledge indexes with the intel filename and skill slug.
6. Preferred intel file naming: `YYYY-MM-DD_topic-key.md` in `/home/nova/.hermes/intel/finance/`.
7. Maintain search tags in the skill index for cross-referencing (tick-size, VRP, DVOL, LOBFrame, etc.).

## Intel Archive Cleanup Cron Pattern

For cron jobs that generate intel files under `/home/nova/.hermes/intel/`, add a companion cleanup cron on a 12h schedule (`0 */12 * * *`):
1. Scan each intel subdirectory for files older than 7 days.
2. Check whether any skill SKILL.md references the intel file (grep for path/filename).
3. Move stale, unreferenced files to `/home/nova/.hermes/intel/archive/<subdir>/`.
4. Detect duplicate filenames or obvious title duplicates across subdirs; move weaker versions to archive.
5. Write a one-line summary to `/home/nova/.hermes/intel/meta/audit/archive-log-YYYY-MM-DD.md`.
6. Skip silently if nothing qualifies.

This prevents unbounded intel directory growth and cross-domain duplication.

## Burst Creator Consolidation Pattern

When multiple creator crons run on the same short interval (e.g., 9 crons @ every 1m), they create scheduler congestion, duplicate topic selection, and race conditions. Consolidate into a single rotating `knowledge-domain-curator` cron on `every 5m` with:
- Explicit cross-skill deduplication: `skills_list()` before creating, check for existing coverage.
- Domain rotation: cycle through a fixed list of categories per run.
- Shared state file (`/tmp/curator-state.json`) tracking last domain and created skill names to avoid immediate repeats.
- Fallback to adjacent domains only after primary domain yields nothing new.
- Pause or delete the individual burst crons after consolidation.

## Security Audit + Remediation Pair Pattern

Pair every security audit cron (e.g., `0 */6 * * *`) with a remediation cron that:
- Runs shortly after the audit (e.g., `30 */6 * * *`).
- Reads the audit output (stdout/stderr or log file).
- For each CRITICAL finding: attempt automatic fix (e.g., replace `curl | bash` with download-then-execute, remove hardcoded secrets, replace `rm -rf` with safer alternative).
- For HIGH/MEDIUM: add a TODO comment or create a tracking issue in the skill's references.
- Log remediation attempts to `/home/nova/.hermes/intel/meta/audit/security-remediation-YYYY-MM-DD.md`.

## Skill Consumption Tracking Cron Pattern

Add a weekly cron (`0 9 * * 1`) that:
- Reads `.usage.json` from the skill library.
- Identifies skills with `use_count == 0` and `created_at > 30 days ago`.
- Archives or marks for review (move to `archived/` subdir or add `state: "stale"` to usage entry).
- Updates `library-skill-index` to remove stale entries.
- Reports top/bottom skills by usage to inform curation priorities.

## Idempotent Creator Cron Pattern

Creator crons that generate skills (e.g., `deep-research-pack-creator.py`) must not mutate their backlog on skip. If the target skill already exists, the item must stay in the backlog (or move to a "completed" archive) — not be removed. See `references/idempotent-creator-cron.md` for the detailed problem, consequences, and three fix patterns.

**Ready-to-apply fix:** `scripts/fix-idempotent-backlog.py` — run with `python3 scripts/fix-idempotent-backlog.py` from skill directory to apply Fix Pattern 1 (conditional backlog removal) to `deep-research-pack-creator.py`.

**Status tracking:** `references/deep-research-pack-creator-status.md` — current state, fix verification steps, and remaining backlog topics.