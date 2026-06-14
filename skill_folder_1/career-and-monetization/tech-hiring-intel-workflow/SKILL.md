---
name: tech-hiring-intel-workflow
description: Collect, validate, and operationalize software engineering job-market intelligence for technical professionals. Use when the task involves hiring trends, contract demand, freelance niches, AI-related hiring signals, or side-project monetization patterns relevant to engineering careers.
---

# Tech Hiring & Career Intel Workflow

## When to use this skill
Use for recurring career and monetization intelligence collection targeting technical professionals: remote contracts, freelance niches, hiring trends, AI impact on roles, open-source opportunities, and engineering-relevant creator economy tactics.

## Core workflow
1. **Source-first**: find one substantive 2026-era signal from reputable operators (Pragmatic Engineer, hiring trend reports, compensation and vacancy trackers, major layoff announcements, or platform shift evidence). Prioritize named sources with numbers over opinion pieces.
2. **Verify**: ensure at least one concrete metric (headcount %, role count, YoY %, company name, date). Skip generic motivational content.
3. **Save intel**: write a markdown report to `/home/nova/.hermes/intel/career/` using the naming pattern `<topic>-<yyyy-mm>.md`.
4. **Create/enhance skill**: if the evidence created a reusable technique, create or patch a teaching skill under `career-and-monetization/` using `skill_manage` so future runs can reuse the workflow.
5. **If nothing substantive found**: broaden to adjacent domains: digital products, teaching, consulting, SaaS side projects, AI automation, template/plugin marketplaces.

## Intel report structure
- `# <Topic> Intelligence — <Date/Period>`
- `Collected: <ISO date>`
- `Source: <name, URL, date>`
- `## What Changed` — one-paragraph driver
- `## Hard Numbers` — bullet list of rankings, percentages, counts
- `## Stability / Risk Signal` — which employers/sectors are up or down
- `## Demand Shift` — skills, roles, or geographies gaining premium
- `## Contract / Freelance Angle` — near-term pricing and project signals
- `## Actionable Takeaway` — one paragraph a technical professional can act on this week

## Rules
- Favor signals, numbers, names, and exact evidence over vague advice.
- Skip generic motivational content.
- Do not fabricate data; if primary signal yields no numbers, broaden search before writing.
- Silent mode: if no substantive intel is available, respond with `[SILENT]`.

## Related skills
- `career-and-monetization/*` for rate negotiation, contracting, platform migration, portfolio selection, and freelancer positioning skills.
