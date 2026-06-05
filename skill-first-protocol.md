# Mandatory Skill-First Protocol

## Purpose
Ensure every agent action is grounded in reusable skills rather than ad-hoc execution. Skills encode proven workflows, pitfalls, and exact commands; ignoring them wastes context and breaks consistency.

## Rule 0 — Highest-Precedence Invariant
Skill-first is not optional. Before **any** `read_file`, `terminal`, `web_search`, `web_extract`, `browser_*`, `execute_code`, `patch`, `memory`, `cronjob`, `delegate_task`, or answer output, the agent must first inspect the skill library and either load a skill or create one. Skipping this step is treated as a workflow violation.

## Step 1 — Scan Before Acting
On every task, including follow-ups and small refinements:
1. Call `skills_list` or otherwise inspect available skills.
2. Match by name, category, tags, or partial relevance.
3. If even one skill looks related, load it with `skill_view` and obey its workflow, commands, and warnings before doing the underlying work.

## Step 2 — Load and Follow
When a matching skill is found:
- Read the full `SKILL.md` content.
- Check linked references, templates, and scripts when the skill points to them.
- Use the skill’s exact commands, paths, and guardrails.
- If the skill has pitfalls, verify them before proceeding.

## Step 3 — Create When Missing
If no skill covers the task domain:
1. Create or patch a skill first.
2. The new skill must include trigger conditions, real commands, pitfalls, and verification steps.
3. After the skill exists, execute the task by following that skill.

## Step 4 — Maintain Discipline
- Do not bypass the skill library because a task feels small or familiar.
- Do not rely on memory or intuition when a skill exists and is current.
- If a skill appears outdated or wrong, patch or replace it immediately rather than ignoring it.

## Enforcement Notes
- Hard-coded reminders in agent memory or persona are required; do not rely on this document alone.
- Agent responses should include skill citation when executing planned work: skill name, file path, and relevant steps.
- Repeated violations should be surfaced explicitly as protocol breaches, not silently absorbed.

## One-line Rule for Derivative Systems
> No action without skill search first. No skill violation tolerated.
