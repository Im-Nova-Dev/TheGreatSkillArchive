---
name: skill-backlog-enrichment
description: "Enrich auto-generated stub skills from the skill backlog with real content, references, templates, and scripts"
version: 0.1.0
category: technology
---

# Skill Backlog Enrichment

## Overview

The `random-skill-elaborator.py` script creates stub SKILL.md files from a backlog of 57 technology skill concepts. However, these stubs are minimal templates — they contain only frontmatter, a one-paragraph description, and placeholder sections. This skill covers the workflow for enriching those stubs into class-level skills with deep content, `references/` directories, `templates/`, and `scripts/`.

## When To Use

- After running the backlog elaboration script and discovering all items already exist as stubs
- When a skill in `~/.hermes/skills/technology/` has only auto-generated content (dated today, placeholder workflow)
- When you need to convert a stub skill into a production-ready class-level skill

## Workflow

### 1. Audit the stub

```bash
# Check if a skill is a stub (auto-generated today, has placeholder content)
read_file(path="~/.hermes/skills/technology/<skill-name>/SKILL.md")
```

Signs of a stub:
- Frontmatter `version: 0.1.0`
- Description matches the backlog entry exactly
- "Auto-generated on YYYY-MM-DD" in Reference Notes
- Workflow section has generic 3-step template
- No `references/`, `templates/`, or `scripts/` directories

### 2. Enrich the SKILL.md

Replace placeholder sections with:
- **Prerequisites**: What must exist before using this skill
- **Core Concepts**: Domain knowledge the agent needs
- **Detailed Workflow**: Numbered steps with exact commands, not generic placeholders
- **Pitfalls & Edge Cases**: Real failure modes discovered in practice
- **Verification Steps**: How to confirm the skill worked
- **Related Skills**: Links to other technology skills this composes with

### 3. Add support files

Use `skill_manage(action='write_file', file_path='references/...')` for:
- Domain research excerpts (API docs, paper summaries, provider quirks)
- Error transcripts and reproduction recipes
- Configuration examples from real usage

Use `skill_manage(action='write_file', file_path='templates/...')` for:
- Boilerplate configs the skill produces
- Known-good scaffolding the agent can copy and modify

Use `skill_manage(action='write_file', file_path='scripts/...')` for:
- Deterministic verification probes
- Fixture generators
- Commands the skill invokes programmatically

### 4. Update the skill's SKILL.md with pointers

Add a **Support Files** section listing each file with a one-line purpose so future agents know they exist.

## Enrichment Priority

Not all stubs need equal depth. Prioritize:
1. Skills you'll actually use in the next session
2. Skills that compose with other active skills
3. Skills with complex domain knowledge (quantum, bio, distributed systems)
4. Skills with provider-specific quirks (edge, satellite, crypto)

## Example: Enriching `quantum-sim-scaffold`

```bash
# 1. Read the stub
# 2. Research quantum circuit simulation frameworks (Qiskit, Cirq, PennyLane, QuTiP)
# 3. Write references/frameworks.md with comparison table
# 4. Write templates/qiskit-circuit.py starter
# 5. Write scripts/verify-install.py that probes for working simulator
# 6. Patch SKILL.md with real workflow, pitfalls, and support file pointers
```

## Pitfalls

- **Don't mirror upstream docs** — references/ should be condensed knowledge banks, not full copies
- **Don't create session-specific skills** — the skill name must be class-level (e.g., `quantum-sim-scaffold`, not `qiskit-setup-today`)
- **Don't add environment-dependent fixes as durable rules** — missing binaries, unconfigured creds, fresh-install errors are not skill content
- **Verify before writing** — run the commands in templates/scripts yourself before committing them to the skill
- **Backlog depletion stall** — The `random-skill-elaborator.py` script picks random items but **does not remove them from the backlog when the skill already exists** (it only logs "Skipped" and exits 0). This causes the same items to be picked repeatedly, preventing the backlog from ever depleting below the refill threshold (8 items). When auditing, check `~/.hermes/data/skill-backlog.json` — if all items already have skill directories, the script will infinite-loop on skips. Fix options: (a) patch the script to `pop` skipped items permanently, or (b) manually clear the backlog file to trigger a fresh DEFAULT_BACKLOG refill.

## Verification

After enrichment, the skill directory should have:
- `SKILL.md` with substantive content (not placeholders)
- `references/` with ≥1 `.md` file
- `templates/` or `scripts/` with ≥1 file (if applicable)
- All files referenced in SKILL.md

## Related Skills

- `hermes-agent-skill-authoring` — for SKILL.md structure and validation
- `technology/agent-tool-auditor` — for auditing tool usage patterns in skills
- `technology/mcp-server-generator` — for scaffolding MCP servers as templates
