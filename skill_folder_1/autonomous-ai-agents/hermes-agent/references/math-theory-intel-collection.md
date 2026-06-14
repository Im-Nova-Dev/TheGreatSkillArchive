# Math & Theory Intel Collection Cron Pattern

Use this when the cron job is `find arXiv/paper -> save intel -> create or enhance teaching skill` for mathematics, theoretical computer science, and quantitative theory.

## Directory Structure

- Intel files: `/home/nova/.hermes/intel/math-and-theory/YYYY-MM-DD_topic-key.md`
- Topic index: `/home/nova/.hermes/intel/math-and-theory/topic-index.md`
- Run log: `/home/nova/.hermes/intel/math-and-theory/run-log.md`

## Pattern

1. **Search existing skill tree first** (`skills_list(category="quantitative-theory")` and `skills_list(category="university-cs")`). If a class-level teaching skill already covers the topic, enhance it; do not create a new narrow skill.

2. **Check topic index** (`/home/nova/.hermes/intel/math-and-theory/topic-index.md`) for the mapped topic name before writing a new intel file or creating a new skill.

3. **Derive topic key** as `lowercase, hyphens, no dates`, for example:
   - `sharp-low-degree-thresholds-planted-vs-planted`
   - `entropy-sum-product-lower-bounds`
   - `erdos-unit-distance-disproof`
   - `gate-elimination-constructive-circuit-lower-bounds`

4. **Deduplication**: If the index already contains that key under a different date prefix, treat the item as already indexed unless the new item materially changes the theory; otherwise skip creating a duplicate skill.

5. **When adding a new class-level skill**, place it under `quantitative-theory/` (for theory/TCS results) or `university-cs/` (for textbook-style CS fundamentals) and update `topic-index.md` with both the intel file and the skill slug.

6. **Preferred intel file naming**: `YYYY-MM-DD_topic-key.md` in `/home/nova/.hermes/intel/math-and-theory/`.

7. **Run log**: Append a one-line entry to `run-log.md` with date, source, topic, and action taken.

## Topic Index Format

The `topic-index.md` should maintain a table:

| Topic Key | Intel File | Skill Slug | Date Added |
|-----------|------------|------------|------------|
| sharp-low-degree-thresholds-planted-vs-planted | 2026-06-06_sharp-low-degree-thresholds-planted-vs-planted.md | quantitative-theory/sharp-low-degree-thresholds-planted-vs-planted | 2026-06-06 |

## Sources to Scan

- arXiv: cs.CC (Computational Complexity), math.CO (Combinatorics), cs.LG (Machine Learning), cs.DS (Data Structures), math.PR (Probability)
- Hacker News for discussion of new results
- Math blogs (Terence Tao, Gil Kalai, etc.)
- Major conference proceedings (STOC, FOCS, SODA, ITCS, CCC, NeurIPS, ICML, ICLR)

## Deduplication Heuristics

- Skip if skill name substring matches any existing skill in quantitative-theory or university-cs (check last 20 runs via run-log.md)
- Prefer timeless theory but include recent interesting papers
- One skill per run, high compactness

## Tool Infrastructure Note (2026-06-06)

The `write_file` and `skill_manage(action='create')` tools exhibit a parameter-dropping bug under context pressure where large `content`/`file_content` payloads are lost. Workaround:

1. Use `write_file` with small content to create file
2. Use `patch(mode='replace')` with `old_string`/`new_string` to write full content
3. Or use `skill_manage(action='write_file')` with `file_content` for support files

This is an infrastructure issue, not a skill constraint.