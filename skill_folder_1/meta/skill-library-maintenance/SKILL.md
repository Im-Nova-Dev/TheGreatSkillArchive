---
name: skill-library-maintenance
description: Maintain a healthy Hermes skill library. Covers auditing for duplicates, refreshing umbrella indexes, avoiding duplicate create failures, and keeping class-level structure over flat one-off entries.
---

# Skill Library Maintenance

Use this skill when the local skill library has grown, when umbrellas are stale, when batch writes produced duplicate or off-topic skills, or when you want to verify skill contents for stability or security risks.

## Duplicate resolution pattern
When the same skill name exists at the root level and under a category subdirectory:
1. Prefer the category-subdirectory entry as the primary.
2. Diff the two SKILL.md files and merge any unique details from the root duplicate into the primary.
3. Remove the root duplicate to eliminate lookup ambiguity.

**Pitfalls learned (2026-06-06):**
- **Content asymmetry:** Root skills sometimes have MORE content than category versions (e.g., `go-cli-development`, `ion-trap-quantum-computing`). Always diff both before deciding primary — don't assume category is stronger.
- **Stale "already removed" claims:** A skill's description may claim it already removed a duplicate when both still exist (e.g., `arch-pacman-keyring-repair`). After deleting the actual duplicate, clean up the surviving skill's description.
- **`absorbed_into` requires existing target:** `skill_manage(action='delete', absorbed_into='...')` fails if the target skill doesn't exist. Ensure primary exists first, or omit `absorbed_into` if primary is already live.
- **Three-way collisions:** A name can exist at root, in one category, AND be recreated. Resolution order: delete category → delete root → recreate primary with full merged content.
- **Ambiguous collision error:** "Ambiguous skill name: N skills match" doesn't show full paths. Call `skill_view` with the bare name to enumerate matches, then load each explicitly by path.

## Security auditing
Use `scripts/security-audit-skills.py` to triage risky content across the skill tree. Tune the rule set iteratively: start broad, review hits, then sharpen patterns to reduce false positives while keeping genuine risks. Treat matches as triage leads, not verdicts.

## Cron-driven skill creation pattern
When repeatedly creating skills from web research, use a recurring cron with: `enabled_toolsets: ["web"]`, `skills: ["skill-library-maintenance"]`, a rotation or topic strategy, and a built-in fallback to adjacent domains before skipping silently. Deliver a 3-bullet summary (collected topic, skill created/skipped, any error).

**Session reference**: See `references/backlog-injection-workflow.md` for the 2026-06-06 run where the backlog was exhausted and manual injection + repeated runs created 8 new technology skills.

### `random-skill-elaborator.py` pitfall
The bundled `random-skill-elaborator.py` script (often used by `skill-generator` crons) has a race/design flaw:
1. It pops a random item from the backlog, **then** checks if the skill exists.
2. If the skill already exists, it prints "Skipped: existing skill" and exits — **without putting the item back** in the backlog.
3. The backlog then refills with `DEFAULT_BACKLOG` (56 items), most of which already have skill directories.
4. Repeated runs burn through the entire backlog, producing only "Skipped" output.

**Fix pattern** (apply via `skill_manage(action='patch')` to the script or by wrapping the cron):
- Pre-filter the backlog against existing skill directories before picking: `existing = {d.name for d in Path(LIBRARY).rglob('**/SKILL.md').parent}`; select only items whose slug doesn't exist.
- Or: if skipped, re-append the item to the backlog so it isn't lost.
- Better: make the cron drive **expansion** of thin skills (add references/, templates/, scripts/) rather than just creating stubs. The `technology/` category currently has 52 auto-generated ~1KB stubs — they need class-level content, not more stubs.

**Confirmed workaround (2026-06-06)**: When the backlog is exhausted of novel items, manually inject new skills into `skill-backlog.json` before running the script. Pre-filtering against existing `SKILL.md` directories is the robust fix. See `references/random-skill-elaborator-fix.md` for the full patch and root-cause analysis.

**Session 2026-06-06 (this run)**: Cron executed `random-skill-elaborator.py --extend-missing` 12 times. All runs printed "Skipped: existing skill technology/..." because all 45 backlog items + the 8 injected in the prior workaround already have skill directories (63 total in `technology/`). The fix documented in `references/random-skill-elaborator-fix.md` was **not applied** to the actual script — the script still pops one item, checks existence, and exits on skip. The backlog file (`skill-backlog.json`) remains a static DEFAULT_BACKLOG refill with no progress toward new skills. Technology category has 63 skills but only 45 backlog entries; future cron runs will continue to skip silently until the script is patched or the backlog is expanded with genuinely novel items.

**Session 2026-06-06 (cron job repeat)**: Another cron run executed the script 20+ times. Every run skipped instantly — the backlog is completely exhausted of novel items. Technology category has 63 skill directories (including 8 created in the prior workaround), while `DEFAULT_BACKLOG` only has 56 unique entries. The pre-filter fix from `references/random-skill-elaborator-fix.md` remains unapplied to the production script. Without the fix, the cron will perpetually burn through DEFAULT_BACKLOG refills and report only skips.

**Backlog duplicate detection (2026-06-06)**: The current `skill-backlog.json` contains duplicate entries — `provenance-chain-verifier` (2x) and `synthetic-media-verifier` (2x) appear twice in the 45-item backlog. This means the effective novel-item pool is even smaller (~43 unique slugs). When the pre-filter fix is applied, these duplicates should be deduped before pre-filtering against existing skills.

**Session 2026-06-06 (comprehensive audit)**: Library has **tripled to ~3,482 skills** from ~1,067. Technology category now at **180 skills** (not 63). Godot category at **~800 micro-skills** (not 150+). Three auto-generator scripts (`random-skill-generator` 181 runs, `random-social-skill-generator` 225 runs, `deep-research-pack-creator` 240 runs = **646 total runs**) creating massive stub/duplicate pollution. **9 burst crons @ 1m still active** causing scheduler congestion. The `random-skill-elaborator.py` pre-filter fix is documented but **still unapplied**. Technology category has exhausted novel-item pool completely — all 56 DEFAULT_BACKLOG slugs + 8 injected = 64 skills exist; future runs will skip perpetually. **Fix verified necessary**: retire `random-skill-generator` and `random-social-skill-generator` crons; reduce `deep-research-pack-creator` to every 10m; create single `knowledge-domain-curator` cron @ 5m with domain rotation.

```python
# Quick pre-filter before picking
existing = {p.parent.name for p in Path(LIBRARY).rglob('**/SKILL.md')}
available = [item for item in backlog if item["slug"] not in existing]
# then pick from `available` instead of the full backlog
```

## Intel archive cleanup pattern
For cron jobs that generate intel files under `/home/nova/.hermes/intel/`, add a companion cleanup cron on a 12h schedule (`0 */12 * * *`):
1. Scan each intel subdirectory for files older than 7 days.
2. Check whether any skill SKILL.md references the intel file (grep for path/filename).
3. Move stale, unreferenced files to `/home/nova/.hermes/intel/archive/<subdir>/`.
4. Detect duplicate filenames or obvious title duplicates across subdirs; move weaker versions to archive.
5. Write a one-line summary to `/home/nova/.hermes/intel/meta/audit/archive-log-YYYY-MM-DD.md`.
6. Skip silently if nothing qualifies.
This prevents unbounded intel directory growth and cross-domain duplication.

## Burst creator consolidation pattern
When multiple creator crons run on the same short interval (e.g., 9 crons @ every 1m), they create scheduler congestion, duplicate topic selection, and race conditions. Consolidate into a single rotating `knowledge-domain-curator` cron on `every 5m` with:
- Explicit cross-skill deduplication: `skills_list()` before creating, check for existing coverage.
- Domain rotation: cycle through a fixed list of categories per run.
- Shared state file (`/tmp/curator-state.json`) tracking last domain and created skill names to avoid immediate repeats.
- Fallback to adjacent domains only after primary domain yields nothing new.
- Pause or delete the individual burst crons after consolidation.

## Godot micro-skill consolidation guidance
The `godot/` category has **~800 micro-skills** tripled from ~150 organized into deep subtrees (e.g., `retro-2d-advanced-gdscript/`, `retro-2d-camera-and-scenes/`, `retro-2d-input-and-controls/`, `retro-2d-animation-and-characters/`, `retro-2d-feedback/`, `retro-2d-polish-and-juice/`, `retro-2d-level-design/`, `retro-2d-gameplay-systems/`, `retro-2d-combat-and-enemies/`, `retro-2d-world-design/`, `retro-2d-data-driven/`, `retro-2d-events-and-states/`, `retro-2d-save-data-systems/`, `retro-2d-templates/`, `retro-2d-language-deep-dives/`, `retro-2d-genre-tutorials/`, `retro-2d-specific-tutorials/`, `retro-2d-complete-projects/`, `retro-2d-editor-plugins/`, `retro-2d-optimization/`, `retro-2d-physics-deep-dive/`, `retro-2d-testing-and-debugging/`, `retro-2d-tools-and-editor/`, `retro-2d-multiplayer/`, `godot-2d-advanced/`, `godot-2d-fundamentals/`, `godot-3d-game-development/`, `godot-shaders-and-materials/`, `godot-tutorial-series/`, `godot-community-and-learning/`, `godot-general-mastery/`). Many are single-concept skills that should be merged into class-level umbrellas:
- `gdscript-advanced-patterns-and-metaprogramming` ← absorb `coroutines-and-yield-patterns`, `tween-alternatives-and-animation-state-machines`, `metaprogramming-and-class_name-extensions`, `custom-type-hints-and-typed-dictionaries`, `reflection-and-object-pools-optimization`, `performance-pitfalls-in-gdscript-and-mitigation`, `signal-organization-and-decoupled-messaging`
- `retro-2d-camera-systems` ← absorb all `camera-and-scene` micro-skills
- `retro-2d-input-systems` ← absorb all `input-and-controls` micro-skills
- `retro-2d-optimization` ← absorb all `optimization` micro-skills
- `retro-2d-ui-systems` ← absorb all `ui-design` micro-skills
- `retro-2d-data-driven` ← absorb all `data-driven` micro-skills
- `retro-2d-events-and-states` ← absorb all `events-and-states` micro-skills
- `retro-2d-save-systems` ← absorb all `save-data-systems` micro-skills
- `retro-2d-feedback` ← absorb all `feedback` micro-skills
- `retro-2d-physics` ← absorb all `physics-deep-dive` micro-skills
- `retro-2d-testing` ← absorb all `testing-and-debugging` micro-skills
- `retro-2d-editor-tools` ← absorb all `tools-and-editor` micro-skills
Use `skill_manage(action='patch')` to merge content into the primary umbrella, then `skill_manage(action='delete', absorbed_into='<primary>')` for each secondary.

## Language-specific fragmentation (NEW 2026-06-06)
Per-language async/concurrency topics are duplicated across multiple skills. Create per-language consolidation umbrellas:
- **Rust**: 100 skills — `rust-async-and-tokio` + `rust-concurrency-patterns-advanced` + `rust-fearless-concurrency` → `rust-async-fundamentals`
- **Go**: 95 skills — `go-concurrency-patterns` + `go-concurrency-patterns-advanced` + `go-concurrency-foundations` → `go-concurrency-fundamentals`
- **TypeScript**: 60 skills — `typescript-advanced-types` + `typescript-type-system-deep-dive` + `typescript-type-system-mastery` → `typescript-type-system`
- **Python**: 60+60 skills — `python-async-advanced` + `python-async-advanced-patterns` + `python-async-and-asyncio-deep-dive` (both `python/` and `modern-python/`) → `python-async-fundamentals`

## Auto-generator pollution (NEW 2026-06-06)
Three scripts have **646 combined runs** creating thousands of stub/duplicate skills:
- `random-skill-generator` (181 runs) — exhausted backlog, all skips
- `random-social-skill-generator` (225 runs) — exhausted backlog, all skips
- `deep-research-pack-creator` (240 runs) — still producing but diminishing returns

**Fix**: Retire first two crons; reduce third to every 10m; replace all with single `knowledge-domain-curator` @ 5m with domain rotation.

## Security remediation gap
The security audit script (`scripts/security-audit-skills.py`) finds CRITICAL/HIGH/MEDIUM issues but there is no automated remediation cron. After each audit run, schedule or trigger a follow-up that:
- Reads the audit output (stdout/stderr or log file).
- For each CRITICAL finding: attempt automatic fix (e.g., replace `curl | bash` with download-then-execute, remove hardcoded secrets, replace `rm -rf` with safer alternative).
- For HIGH/MEDIUM: add a TODO comment or create a tracking issue in the skill's references.
- Log remediation attempts to `/home/nova/.hermes/intel/meta/audit/security-remediation-YYYY-MM-DD.md`.

## Skill consumption tracking gap
Current library shows creation >> consumption (most skills use_count/view_count = 1–2). Add a cron or hook that:
- Runs weekly, reads `.usage.json`.
- Identifies skills with `use_count == 0` and `created_at > 30 days ago`.
- Archives or marks for review (move to `archived/` subdir or add `state: "stale"` to usage entry).
- Updates `library-skill-index` to remove stale entries.
- Reports top/bottom skills by usage to inform curation priorities.

## Excessive expansion diminishing returns
When the user requests continuous expansion (“keep expanding as much as possible”), after many repeated bulk batches the agent will generate duplicate/placeholder content that requires cleanup rather than creation. After 20+ repeated bulk batches without strategic pivot, recommend consolidation options:
- merge duplicates,
- create an index from existing artifacts,
- build a plan from existing content,
- consolidate micro-topics into class-level umbrellas.
Continuing to emit a large number of new flat stubs is low-value and creates churn.

## Maintenance workflow
1. **Audit**
   - List skills by category; inspect `scripts/audit-skills.py` for size/link quality and `scripts/security-audit-skills.py` for suspicious code.
   - Spot duplicates and stale umbrellas.
2. **Resolve**
   - Merge overlaps into one class-level skill.
   - Delete only off-topic or stale entries.
3. **Refresh**
   - Update umbrella indexes after adds or deletes.
   - Keep class-level skill structure intact.
4. **Security sanity check**
   - Run `scripts/security-audit-skills.py` and review hits.
   - Treat matches as triage leads, not verdicts.
   - Inspect full skill source; confirm or dismiss each hit before action.

## Recovery and QA workflows

1. **Recover from failed batch writes**
   - When many create calls fail together, stop and inspect.
   - Check which skill directories or files were partially written.
   - Repair both the intended skill and any near-duplicate files before continuing.

2. **Gap checking**
   - After adding or patching skills, list skills in the target category.
   - Verify intended skills are present.
   - Check for off-topic or nonsensical entries and remove them.

3. **Consistency check**
   - Skill names must be class-level and self-descriptive.
   - Avoid session-specific names, version identifiers, or ephemeral labels.
   - If something looks underdeveloped, refine it instead of expanding without correction.

## Key rules

- Prefer class-level umbrellas to many narrow one-session skills.
- Check whether a skill directory exists before calling create again.
- Patch existing skills when correcting content; don't recreate without checking.
- Keep indexes accurate and up to date.
- Avoid environment-specific failure notes as durable rules.
- Stop blind batching after repeated failures. Do targeted patching and verification before continuing.
- After repeated bulk expansions, favor consolidation over raw creation.

## Batch category expansion
When a category is significantly below target size and batch expansion is requested:
- Add focused class-level skills that fit the existing umbrella.
- Preserve existing sibling skills; do not overwrite or duplicate them.
- Verify resulting counts after writes to confirm intended skills are present.
- Avoid ephemeral/session-specific names, version tags, or PR-code-style labels.

## Skill count tracking
Use `scripts/skill-count-logger.sh` to append timestamped skill counts to a markdown log. The script counts `SKILL.md` files under `~/.hermes/skills/` and writes entries to `/home/nova/Documents/skill-count-log.md`. A cron job `skill-count-logger` runs this **every 10 minutes**.

## Optimize existing crons for skill density
When asked to maximize skill output from existing crons:
1. Attach `skill-library-maintenance` to every skill-creator cron so it auto-loads the maintenance playbook.
2. Update prompts to prefer extending existing skills over creating new ones.
   - Only create a new skill if no existing class-level skill covers the topic.
   - Add a fallback to broaden the search to adjacent domains before skipping silently.
3. If the cron has a script hook, pass an `--extend-missing` or similar flag so the script expands thin skills by default.
4. Require each cron run to deliver a 3-bullet summary: topic selected, action taken, any error.
5. Keep the skill-count logger cron active so changes in skill growth rate are measurable.

## Iterative bulk expansion
When user requests broad or repeated skill creation:
- Treat phrases like "yea keep going", "continue", or "expand it" as continuous build signals until redirected.
- Build incrementally without per-batch confirmation checkpoints.
- If tool restrictions block file writes, use `skill_manage` and memory updates only.
- Do not stop after a fixed number of batches unless the user says stop.