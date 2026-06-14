---
name: debugging-testing
description: "Debugging & testing toolbox: Dogfood (exploratory web QA), Kanban orchestrator/worker (multi-agent task routing), Python debugpy (pdb/debugpy recipes), Simplify Code (parallel 3-agent cleanup), Systematic Debugging (reproduction, isolation, bisect, fix validation), Spike (throwaway feasibility experiments). Use for any debugging, testing, QA, or experimental validation workflow."
version: 1.0.0
category: software-development
tags: [debugging, testing, qa, dogfood, kanban, python-debugpy, simplify-code, systematic-debugging, spike, pdb, debugpy]
---

# Debugging & Testing

Unified class-level skill covering debugging, testing, QA, and experimental workflows. Replaces 7 narrow skills: `dogfood`, `kanban-orchestrator`, `kanban-worker`, `python-debugpy`, `simplify-code`, `systematic-debugging`, `spike`.

## When to Use

- Exploratory QA of web apps: systematic browser testing, evidence collection, bug reports
- Multi-agent task orchestration via Kanban: decomposition, routing, worker lifecycle
- Python debugging: pdb/debugpy recipes (local, remote, post-mortem, pytest, Hermes-specific)
- Parallel code cleanup: 3-agent review (reuse, quality, efficiency) of recent changes
- Systematic debugging: reproduction → isolation → hypothesis → fix → validation
- Feasibility spikes: throwaway experiments to validate ideas before building

---

## Decision Guide

| Task | Sub-Tool |
|------|----------|
| Web app QA: navigate, click, test forms, find bugs | **Dogfood** |
| Decompose complex work → route to specialist agents | **Kanban Orchestrator** |
| Execute Kanban tasks: coding, research, review | **Kanban Worker** |
| Python: breakpoint, remote debug, pytest, post-mortem | **Python Debugpy** |
| Clean up recent changes: 3-agent parallel review | **Simplify Code** |
| Debug systematically: repro → bisect → hypothesis → fix | **Systematic Debugging** |
| Validate idea feasibility before committing | **Spike** |

---

## 1. Dogfood (Exploratory Web QA)

### Overview

Systematic exploratory QA testing of web applications using browser tools. 5-phase workflow: Plan → Explore → Collect Evidence → Categorize → Report.

### Prerequisites

- Browser toolset: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision`, `browser_console`, `browser_scroll`, `browser_back`, `browser_press`
- Target URL and testing scope

### Workflow

**Phase 1: Plan**
- Create output dir: `{output_dir}/screenshots/`, `{output_dir}/report.md`
- Build sitemap: landing, navigation, key flows, forms, edge cases

**Phase 2: Explore** (per page)
```bash
browser_navigate(url="https://example.com/page")
browser_snapshot()
browser_console(clear=true)  # Check after EVERY navigation/interaction
browser_vision(question="Describe layout, identify issues", annotate=true)
# Test interactive elements: click, type, tab, scroll
browser_console()  # Check for JS errors after interactions
```

**Phase 3: Collect Evidence**
- Screenshot each issue: `browser_vision(question="Capture issue", annotate=false)`
- Record: URL, repro steps, expected vs actual, console errors, screenshot path
- Classify: Severity (Critical/High/Medium/Low), Category (Functional/Visual/Accessibility/Console/UX/Content)

**Phase 4: Categorize**
- Deduplicate, assign final severity/category, sort by severity

**Phase 5: Report**
- Executive summary + per-issue sections + summary table + testing notes
- Template: `templates/dogfood-report-template.md`

### Critical Tips

- **Always check `browser_console()`** after navigation/interactions — silent JS errors are high-value findings
- Use `annotate=true` for element labels mapping to `@eN` refs
- Test valid AND invalid inputs, scroll long pages, test navigation flows, check edge cases

---

## 2. Kanban Orchestrator (Multi-Agent Task Routing)

### When to Use Board (vs direct execution)

- Multiple specialists needed (research + analysis + writing = 3 profiles)
- Work should survive crash/restart
- Human may interject
- Parallel subtasks possible
- Review/iteration expected
- Audit trail matters

**If none apply** → use `delegate_task` or answer directly.

### Core Rule: Route, Don't Execute

- Do not execute work yourself
- Every concrete task → create Kanban task + assign
- Split multi-lane requests before creating cards
- Run independent lanes in parallel
- Link only true data dependencies (use `parents=[...]`)

### Decomposition Playbook

**Step 0: Discover available profiles**
```bash
hermes profile list
# or ask user: "What profiles do you have set up?"
```

**Step 1: Understand goal** — ask clarifying questions

**Step 2: Sketch task graph** — extract lanes, map to profiles, decide dependencies

**Step 3: Create tasks with links**
```python
t1 = kanban_create(title="research: cost", assignee="<profile-A>", parents=[])
t2 = kanban_create(title="research: perf", assignee="<profile-A>", parents=[])
t3 = kanban_create(title="synthesize", assignee="<profile-B>", parents=[t1, t2])
t4 = kanban_create(title="draft memo", assignee="<profile-C>", parents=[t3])
```

**Step 4: Complete with summary**
```python
kanban_complete(summary="decomposed into T1-T4...", metadata={"task_graph": {...}})
```

### Common Patterns

- **Fan-out + fan-in**: N research cards (no parents) → 1 synthesis card (all as parents)
- **Parallel impl + validation**: impl card + explorer card → reviewer depends on both
- **Pipeline**: planner → implementer → reviewer (each `parents=[previous]`)
- **Same-profile queue**: N tasks, same profile, no deps → serialized

### Goal-Mode Cards (Persistent Workers)

```python
kanban_create(title="Translate docs to French", goal_mode=True, goal_max_turns=15)
```
- Judge evaluates after each turn against title+body as acceptance criteria
- Not done + budget remains → continues in same session
- Budget exhausted → blocked for human review

---

## 3. Kanban Worker (Task Execution)

### Workspace Kinds

| Kind | Behavior |
|------|----------|
| `scratch` | Fresh tmp dir, GC'd on archive |
| `dir:<path>` | Shared persistent directory |
| `worktree` | Git worktree at resolved path |

### Good Handoff Shapes

**Coding task:**
```python
kanban_complete(summary="shipped rate limiter — token bucket, 14 tests pass",
  metadata={"changed_files": ["rate_limiter.py"], "tests_run": 14, "tests_passed": 14,
    "decisions": ["user_id primary, IP fallback"]})
```

**Code needing review (review-required):**
```python
kanban_comment(body="review-required handoff:\\n" + json.dumps({...}))
kanban_block(reason="review-required: rate limiter shipped, needs eyes on fallback choice")
```

**Research task:**
```python
kanban_complete(summary="3 libs reviewed; vLLM wins on throughput",
  metadata={"sources_read": 12, "recommendation": "vLLM", "benchmarks": {...}})
```

### Claiming Created Cards

```python
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF middleware", assignee="web-worker")
kanban_complete(created_cards=[c1["task_id"], c2["task_id"]], ...)
```

### Block Reasons (Decision-Focused)

```python
kanban_comment(body="Full context: I have user IPs from Cloudflare but some behind NATs...")
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth)?")
```

### Retry Diagnostics

Check `kanban_show` for prior runs: `timed_out` → chunk work; `crashed` → reduce memory; `spawn_failed` → profile config issue; `reclaimed` → operator archived; `blocked` → unblock comment should exist.

### Do NOT

- Call `delegate_task` instead of `kanban_create` (delegate = short subtasks; kanban = cross-agent handoffs)
- Call `clarify` (no live user) — use `kanban_comment` + `kanban_block`
- Modify files outside `$HERMES_KANBAN_WORKSPACE`
- Create follow-up tasks assigned to yourself
- Complete unfinished tasks — block instead

---

## 4. Python Debugpy (pdb/debugpy Recipes)

### When to Use

- Local breakpoint debugging
- Launch script under pdb (no source edits)
- Debug pytest tests
- Post-mortem on any exception
- Remote debug with debugpy (attach to running process)
- Debug Hermes-specific processes

### Key References (in `references/python-debugpy/`)

- `overview.md`, `when-to-use.md`
- `pdb-quick-reference.md`
- `recipe-1-local-breakpoint.md` through `recipe-5-remote-debug-with-debugpy.md`
- `debugging-hermes-specific-processes.md`
- `common-pitfalls.md`, `verification-checklist.md`
- `one-shot-recipes.md`

### Quick Patterns

```bash
# Recipe 1: Local breakpoint
python3 -m pdb script.py
# or in code: breakpoint()

# Recipe 2: Launch under pdb (no edits)
python3 -m pdb -c continue script.py

# Recipe 3: Debug pytest test
python3 -m pytest path/to/test.py::test_name -xvs --pdb

# Recipe 4: Post-mortem on any exception
python3 -c "import sys, pdb; sys.excepthook = lambda t,v,tb: pdb.post_mortem(tb); exec(open('script.py').read())"

# Recipe 5: Remote debug with debugpy
# In target: python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client script.py
# In client: python3 -m debugpy --connect host:5678
```

---

## 5. Simplify Code (Parallel 3-Agent Cleanup)

### When to Use

User says: "simplify", "review my code", "clean up my changes", "/simplify"

### Process

**Phase 1: Identify Changes**
```bash
git diff              # uncommitted
git diff HEAD         # if empty, include staged
git diff --staged     # staged only
git diff HEAD~1       # last commit
```

**Phase 2: Launch 3 Reviewers in Parallel**

Each gets COMPLETE diff + repo path. Toolsets: `terminal`, `file`, `search`.

| Reviewer | Focus |
|----------|-------|
| **Code Reuse** | Duplicates existing utils/helpers/constants; hand-rolled logic that utility does |
| **Code Quality** | Redundant state, parameter sprawl, copy-paste variation, leaky abstractions, stringly-typed |
| **Efficiency** | Unnecessary work, missed concurrency, hot-path bloat, TOCTOU, memory issues, broad reads |

**Phase 3: Aggregate & Apply**
- Merge findings, dedupe, discard false positives
- Resolve conflicts: correctness > user focus > readability > micro-perf
- Apply with `patch`/`write_file` (unless dry run)
- Verify: run targeted tests, linter/type check
- Summarize applied fixes + skipped findings

### Rules

- Max 3 reviewers (more = more conflicts, not better coverage)
- WHOLE diff to each reviewer (cross-file issues need full picture)
- Reviewers must provide `file:line → problem → fix` evidence
- Apply = cleanup of user's changes, not whole-module refactor
- Respect project conventions (AGENTS.md, CLAUDE.md, linter config)

---

## 6. Systematic Debugging

### Core Phases

1. **Reproduction** — Minimal input/env, reliable steps
2. **Isolation** — Binary search bisect, blame change window
3. **Inspection** — Logging/tracing, debuggers/watchpoints, stack traces
4. **Fix** — Verify root cause, regression guard

### Teaching Approach

- Require explanation before edits
- Practice one bisect each session
- Add one permanent test per bug

### Key References (in `references/systematic-debugging/`)

- `overview.md`, `the-iron-law.md`, `when-to-use.md`, `the-four-phases.md`
- `phase-1-root-cause-investigation.md` through `phase-4-implementation.md`
- `red-flags-stop-and-follow-process.md`
- `common-rationalizations.md`, `quick-reference.md`
- `hermes-agent-integration.md`, `real-world-impact.md`

---

## 7. Spike (Throwaway Feasibility Experiments)

### When to Use

User wants to "feel out an idea" before committing — validate feasibility, compare approaches, surface unknowns.

**NOT for**: Knowable from docs (research instead), production path (use `plan`), already validated.

### Core Loop

```
decompose → research → build → verdict
```

**1. Decompose** — 2-5 independent feasibility questions, ordered by risk (killer first)

| # | Spike | Validates (Given/When/Then) | Risk |
|---|-------|----------------------------|------|
| 001 | websocket-streaming | Given WS, when LLM streams, then chunks < 100ms | High |
| 002a | pdf-parse-pdfjs | Given PDF, when pdfjs, then structured text | Medium |
| 002b | pdf-parse-camelot | Given PDF, when camelot, then structured text | Medium |

Types: `standard` (one approach) or `comparison` (same question, different approaches — shared number, letter suffix).

**2. Align** — Present table, user confirms/adjusts

**3. Research** (per spike) — Brief, surface approaches, pick one, skip for pure logic

**4. Build** — One dir per spike, standalone, runnable

```
spikes/
├── 001-websocket-streaming/
│   ├── README.md
│   └── main.py
├── 002a-pdf-parse-pdfjs/
│   ├── README.md
│   └── parse.js
└── 002b-pdf-parse-camelot/
    ├── README.md
    └── parse.py
```

Bias toward interactive: CLI > HTML > web server > unit test. Hardcode everything.

**Parallel comparison spikes** — delegate:
```bash
delegate_task(tasks=[
  {"goal": "Build 002a-pdf-parse-pdfjs...", "toolsets": ["terminal", "file", "web"]},
  {"goal": "Build 002b-pdf-parse-camelot...", "toolsets": ["terminal", "file", "web"]},
])
```

**5. Verdict** — Each spike's `README.md` closes with:

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked - ...
### What didn't - ...
### Surprises - ...
### Recommendation for real build - ...
```

---

## Cross-Tool Workflows

| Goal | Tools |
|------|-------|
| Find bug → fix → verify | Dogfood (find) → Python Debugpy (fix/debug) → Systematic Debugging (validate) |
| Decompose feature → parallel impl | Kanban Orchestrator (decompose) → Kanban Workers (impl) → Simplify Code (cleanup) |
| Spike feasibility → build | Spike (validate) → if VALIDATED → Kanban/SIMPLIFY for production |
| Review PR → cleanup | Code review → Simplify Code (3-agent cleanup) |

---

## Common Pitfalls

1. **Dogfood**: Skipping `browser_console()`, not testing invalid inputs, no visual verification
2. **Kanban**: Inventing profile names, bundling independent lanes, over-linking, forgetting deps
3. **Python Debugpy**: Forgetting `pty=true` for remote, not checking Hermes-specific refs
4. **Simplify Code**: Splitting diff across reviewers, reviewers guessing without evidence, over-refactoring
5. **Systematic Debugging**: Editing before explaining, skipping bisect, no regression test
6. **Spike**: Too broad questions, no observable output, declaring "works" after happy path only

---

## Verification Checklist

- [ ] Dogfood: `browser_console()` checked after every interaction, evidence captured, report generated
- [ ] Kanban: Profiles discovered, tasks decomposed with correct deps, workers executing correctly
- [ ] Python Debugpy: Right recipe selected, breakpoint hits, issue isolated
- [ ] Simplify Code: 3 reviewers launched with full diff, findings aggregated, fixes applied & tested
- [ ] Systematic Debugging: Repro steps documented, bisect performed, fix validated, test added
- [ ] Spike: Questions ordered by risk, verdict documented with evidence, recommendation clear