---
name: hermes-agent
description: "Configure, extend, or contribute to Hermes Agent."
version: 2.1.0
category: autonomous-ai-agents
---
  linked_files:
    references:
      - references/cli-reference.md
      - references/configuration.md
      - references/credential-pools.md
      - references/extensions.md
      - references/gateway.md
      - references/mcp-cron-webhooks.md
      - references/sessions-profiles.md
      - references/system-architecture.md
      - references/tools-skills.md


# Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research. It runs in terminals, messaging platforms, and IDEs, and works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others).

Key features: skills-based self-improvement, persistent memory, multi-platform gateway, provider-agnostic design, profiles, and extensible tooling (MCP, plugins, cron, webhooks).

Docs: https://hermes-agent.nousresearch.com/docs/

## When To Use This Skill

- Setting up Hermes or changing model/provider
- Configuring gateway, tools, skills, MCP servers
- Spawning parallel agents with worktrees
- Troubleshooting Hermes CLI behavior
- Contributing to Hermes or writing custom skills

## Quick Start

```bash
hermes setup
hermes chat -q "What is the capital of France?"
hermes model
hermes doctor
```

## Reference Files

| Topic | File |
|-------|------|
| CLI commands | `references/cli-reference.md` |
| Configuration | `references/configuration.md` |
| Tools and skills | `references/tools-skills.md` |
| MCP, cron, webhooks | `references/mcp-cron-webhooks.md` |
| Messaging gateway | `references/gateway.md` |
| Sessions and profiles | `references/sessions-profiles.md` |
| Credential pools | `references/credential-pools.md` |
| Extensions and insights | `references/extensions.md` |
| System architecture | `references/system-architecture.md` |

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Skills** | Reusable procedures saved as markdown docs under `~/.hermes/skills/` |
| **Memory** | Persistent notes across sessions |
| **Profiles** | Isolated Hermes instances with their own config, skills, and memory |
| **Gateway** | Multi-platform bridge for Telegram, Discord, Slack, email, and others |
| **MCP** | Model Context Protocol for external tool servers |
| **Cron** | Scheduled agent runs |
| **Webhooks** | HTTP-triggered agent runs |

## Common Patterns

```bash
# Chat with a specific model
hermes chat -q "complex task" -m anthropic/claude-sonnet-4 -t terminal,web

# Resume last session
hermes -c

# Isolated worktree mode
hermes -w feature-x

# Check config and health
hermes config check
hermes doctor --fix
```

---

## Skill Authoring (formerly `hermes-agent-skill-authoring`)

### When to Use

- Writing new skills for `~/.hermes/skills/` or in-repo skills
- Improving existing skill structure, frontmatter, or content
- Converting session-specific workflows into class-level umbrellas

### Class-Level Umbrella vs Instance

Prefer **class-level umbrellas** — one skill covering a domain with `references/`, `templates/`, `scripts/` for variants.

```
~/.hermes/skills/<category>/<class-name>/
├── SKILL.md
├── references/
├── templates/
└── scripts/
```

### Required Frontmatter

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars
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

### Size Limits & Split Threshold

- Description: ≤1024 chars (enforced)
- Full SKILL.md: ≤100,000 chars (aim 8-15k for umbrellas)
- **Split at ~320 lines** with few `linked_files` → move detail to `references/<topic>.md`

### Structure Template

```markdown
# <Title>

## Overview
1-2 paragraphs on purpose and scope.

## When to Use
- concrete triggers
- counter-triggers / "Don't use for:"

## Core workflow or decision tree
Exact commands, preferred tools, terminal recipes.

## Reference Files
| File | When to open | Why it matters |

## Common Pitfalls
Numbered mistakes and their fixes.

## Verification Checklist
- [ ] post-action checks
```

### Common Pitfalls

1. **Too many narrow skills** → group under one umbrella + references
2. **`skill_manage create` for in-repo** → writes to `~/.hermes/skills/`, not repo; use `write_file`
3. **Leading whitespace before `---`** → validator checks `content.startswith("---")`
4. **Generic description** → start with "Use when ..."
5. **Missing metadata** → version/author/license/metadata expected by peers

---

## Cron Patterns (formerly `hermes-cron-patterns`)

### When to Use

- Creating recurring automation (intel collection, audits, scheduled agent runs)
- Chaining skills in cron jobs
- Silent-skip collection jobs that only notify on new findings

### Schedule Syntax

```bash
# Supported
every 30m
every 2h
0 */6 * * *
0 9 * * *
2026-06-01T09:00:00

# NOT supported
@every 3m
3m (bare duration)
```

### Recurrence

```bash
cronjob(action="create", repeat=0, schedule="every 10m", ...)
# repeat=0 or -1 = forever, repeat=1 = once, omit = one-shot
```

### Silent Skip Pattern

```text
Every run:
1. Do X
2. If no fresh result, skip silently
3. Otherwise deliver short summary
```

Use `no_agent=True` + `script=` — empty stdout = silent delivery.

### Toolset Restriction

| Job Type | Toolsets |
|----------|----------|
| Research/intel | `["web"]` |
| Maintenance/audit | `["terminal", "file"]` |
| Shell-only checks | `["terminal"]` |

### Chaining Skills

```bash
cronjob(action="create", skills=["skill-library-maintenance"], ...)
```

### Intel Collection Patterns

- **Math/Theory**: See `references/math-theory-intel-collection.md`
- **Science**: Check `/home/nova/.hermes/intel/science/topic-index.md` before creating skills
- **Finance**: Check `/home/nova/.hermes/intel/finance/knowledge-index.md`

### Cleanup & Consolidation

- Intel archive cleanup: `0 */12 * * *` — move stale files to archive
- Burst creator consolidation: replace N crons @ 1m with single `knowledge-domain-curator` @ 5m
- Skill consumption tracking: weekly cron for `use_count == 0` skills >30 days old

### Common Pitfalls

1. **Bare duration schedules** — use `every 30m` not `30m`
2. **Script path** — must be in `~/.hermes/scripts/`
3. **Missing `repeat=0`** — defaults to one-shot
4. **Over-loading toolsets** — restrict to minimum needed
