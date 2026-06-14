---
title: Skill Authoring Guide
source: formerly hermes-agent-skill-authoring
---

# Skill Authoring Guide (Consolidated)

## Overview

Target shapes:

1. **Class-level umbrella (default for reusable knowledge):** `~/.hermes/skills/<category>/<class-name>/SKILL.md` plus `references/`, `templates/`, and `scripts/` under that directory. This is the form that scales across many concrete variants.
2. **Instance-level node (rare; use only when a skill is inherently one concrete workflow):** `~/.hermes/skills/<category>/<name>/SKILL.md`.
3. **In-repo:** `/home/nova/hermes-agent/skills/<category>/<name>/SKILL.md` — committed, shipped with the package. Use `write_file` + `git add`. `skill_manage(action='create')` writes to user-local, not the repo tree.

## When to Use

- User asks you to add, expand, improve, or restructure skills in the local library
- You are turning a concrete workflow or piece of knowledge into a reusable class-level skill
- You are editing an existing skill under `~/.hermes/skills/` or an in-repo shipped skill

## Required Frontmatter

Source of truth: `tools/skill_manager_tool.py::_validate_frontmatter`. Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with `\n---\n` before the body.
- Parses as a YAML mapping.
- `name` field present.
- `description` field present, ≤ **1024 chars** (`MAX_DESCRIPTION_LENGTH`).
- Non-empty body after the closing `---`.

Peer-matched shape used by many skills under `skills/`:

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Use when <trigger>. <one-line behavior>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill, another-skill]
---
```

`version` / `author` / `license` / `metadata` are NOT enforced by the validator, but peer skills often include them.

## Size Limits

- Description: ≤ 1024 chars (enforced).
- Full SKILL.md: ≤ 100,000 chars.
- Strong class umbrellas usually sit in the **8-14k char** range. If you're pushing past 20k, split into `references/*.md` and reference them from SKILL.md.

## Split Threshold (Non-Negotiable)

When a SKILL.md body exceeds ~320 lines and has fewer than a few `linked_files` entries, split it:

- Move detailed session-specific content into `references/<topic>.md`.
- Keep SKILL.md as a focused index with trigger guidance, key commands, and a `Reference Files` table.
- Add `linked_files` entries pointing to each new reference.
- Preserve the original frontmatter shape.

This applies to both in-repo and user-local skills.

## Skill Shape: Class-Level Umbrella vs Instance

Prefer class-level umbrellas whenever the knowledge applies to multiple concrete variants, brands, tools, languages, or scenarios. If a batch draft begins as many narrow instance skills, stop and group them under one umbrella with `references/`, `templates/`, and `scripts/` instead of creating a flat duplication list.

- Each umbrella owns one `SKILL.md`.
- Detailed or scenario-specific material goes in `references/<topic>.md`.
- Reusable starter content goes in `templates/<name>.<ext>`.
- Rerunnable verification or fixture content goes in `scripts/<name>.<ext>`.

Instance-level skills are still valid when the skill is inherently one workflow and cannot reasonably be split.

## Class-Level Umbrella Structure

Use this directory form for domain skills:

```
├── SKILL.md
├── references/
│   ├── topic.md
│   └── provider-quirks.md
├── templates/
│   └── example-config.yaml
└── scripts/
    └── verify-install.sh
```

Recommended SKILL.md body sections:

```
# <Title>

## Overview
1-2 paragraphs on purpose and scope.

## When to Use
- concrete triggers
- counter-triggers / "Don't use for:"

## Core workflow or decision tree
Exact commands, preferred tools, and terminal recipes when known.

## Reference Files
| File | When to open | Why it matters |

## Common Pitfalls
Numbered mistakes and their fixes.

## Verification Checklist
- [ ] post-action checks
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable body + pitfalls are the minimum.

## Local Skill Improvement Pattern

When improving a user-local skill:

1. Read with `skill_view(name, file_path)` when available.
2. Patch with `skill_manage(action='patch', ...)` for small focused changes.
3. For bulk or multi-file umbrella restructuring, `execute_code` + `pathlib.Path.write_text` is the most reliable bulk-write path for generated `SKILL.md` and reference files.
4. After fixing, update the nearest umbrella/index so search/loaders can find the result.

## Reference Files

- `references/class-level-umbrella-pattern.md` — class-level umbrella authoring pattern with frontmatter constraints, body layout, split thresholds, and class-vs-instance guidance

## Cross-Referencing Other Skills

`metadata.hermes.related_skills` unions both trees (`skills/` in-repo and `~/.hermes/skills/`) at load time. You CAN reference a user-local skill from an in-repo skill, but it won't resolve for other users who clone the repo fresh. Prefer referencing only in-repo skills from in-repo skills. If a frequently-referenced skill lives only in `~/.hermes/skills/`, consider promoting it to the repo.

## Editing Existing In-Repo Skills

- **Small fix:** `skill_manage(action='patch', name=..., old_string=..., new_string=...)` works fine on in-repo skills.
- **Major rewrite:** `write_file` the whole `SKILL.md`.
- **Adding supporting files:** `write_file` to `skills/<category>/<name>/references/<file>.md`, `templates/<file>`, or `scripts/<file>`.
- **Commit** the edit — in-repo skills are source, not runtime state.

## Common Pitfalls

1. **Creating too many narrow instance skills.** If you find yourself generating many skills that share one domain and most of their structure, you probably want one class-level umbrella plus `references/` for the variants.
2. **Using `skill_manage(action='create')` for an in-repo skill.** It writes to `~/.hermes/skills/`, not the repo tree. Use `write_file` for in-repo creation.
3. **Leading whitespace before `---`.** The validator checks `content.startswith("---")`; any leading blank line fails validation.
4. **Description too generic.** Peer descriptions start with "Use when ..." and describe the trigger class. "Use when debugging X" > "Debug X".
5. **Forgetting author/license/metadata.** Not validator-enforced, but peer skills have it; omitting makes the skill look half-finished.
6. **Writing a skill that duplicates a peer.** Before creating, inspect sibling directories. Prefer extending an existing umbrella to creating a narrow sibling.
7. **Expecting the current session to see the new skill.** It won't. The skill loader is initialized at session start. Verify in a fresh session or via `skill_view` using the exact path.

## Verification Checklist

- [ ] File is at `skills/<category>/<name>/SKILL.md` (or intended user-local path)
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] `name`, `description` present; `description` ≤ 1024 chars
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Total file ≤ 100,000 chars (aim for 8-15k for class umbrellas)
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Common Pitfalls` → `## Verification Checklist`
- [ ] `related_skills` references resolve in-repo (or are explicitly OK to be user-local)
- [ ] `git add`/`git commit` completed on in-repo skills