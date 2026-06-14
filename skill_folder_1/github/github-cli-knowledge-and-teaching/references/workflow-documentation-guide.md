# How to Document Your Git Workflow

Good workflow documentation answers three questions: what, why, and when.

## 1. Start with the “what”

List the branches the team uses and what each means.

## 2. Explain the “why”

For each rule, state the reason.
Bad: “We use squash merge.”
Good: “We use squash merge so `main` stays legible without merge commits, and every merge maps to one shipped change.”

## 3. Say “when”

Rules without timing are hard to enforce.

Examples:
- “Before opening a PR, pull the latest `main`.”
- “Before merging, ensure CI is green and a reviewer approved.”
- “After merge, delete the branch.”

## 4. Make it a checklist

Checklists are easier for humans and automation.

## 5. Keep one version of truth

Put the workflow in:
- `CONTRIBUTING.md` in the repo
- the team wiki
- a repo-specific onboarding doc

## 6. Review it periodically

Every major incident is a chance to improve the workflow doc.
