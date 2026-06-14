---
name: ai-coding-agents
description: "AI coding agent orchestration: Claude Code, Codex, OpenCode, codebase inspection. Use for delegating coding tasks (features, PRs, refactoring, reviews), parallel worktrees, one-shot vs interactive modes, and codebase analysis."
version: 1.0.0
category: autonomous-ai-agents
tags: [coding-agent, claude-code, codex, opencode, codebase-inspection, delegation, worktree, pr-review]
---

# AI Coding Agents

Unified class-level skill for orchestrating external AI coding agents. Replaces 4 narrow skills: `claude-code`, `codex`, `codebase-inspection`, `opencode`.

## When to Use

- Delegating feature implementation, refactoring, PR reviews to external coding agents
- Parallel issue fixing via git worktrees
- Codebase inspection: metrics, structure, complexity hotspots, dependency mapping
- One-shot tasks (print mode) vs interactive sessions (tmux/pty)
- Batch PR reviews

---

## Decision Guide

| Need | Agent | Mode |
|------|-------|------|
| Feature/PR work, Anthropic models | **Claude Code** | Print (`-p`) or Interactive (tmux) |
| Feature/PR work, OpenAI models | **Codex** | `exec` (one-shot) or Background (pty) |
| Feature/PR work, provider-agnostic | **OpenCode** | `run` (one-shot) or Interactive TUI (pty) |
| Codebase metrics, architecture, hotspots | **Codebase Inspection** | Analysis only |
| PR review automation | **Claude Code** / **Codex** / **OpenCode** | Any |

---

## 1. Claude Code

### Prerequisites

- `claude` CLI installed
- Auth: `claude auth login` or `ANTHROPIC_API_KEY`
- Git repo for worktree mode

### Orchestration Modes

| Mode | Flag | Use Case | PTY |
|------|------|----------|-----|
| Print | `-p` | One-shot, CI, scripting | No |
| Interactive | (default) | Multi-turn, human-in-loop | Yes (tmux) |

### Key Flags

| Flag | Purpose |
|------|---------|
| `-p` | Print mode (non-interactive) |
| `-c` | Continue most recent session |
| `-r <id>` | Resume specific session |
| `--worktree [name]` | Isolated git worktree |
| `--model <alias>` | Model selection |
| `--max-turns <n>` | Limit agentic loops |
| `--dangerously-skip-permissions` | Auto-approve tool use |
| `--output-format <fmt>` | text/json/stream-json |
| `--json-schema <schema>` | Structured output |

### Core Patterns

**Print Mode (One-Shot):**
```bash
claude -p 'Add error handling to all API calls in src/' \
  --allowedTools 'Read,Edit' \
  --max-turns 10
```

**Interactive via tmux:**
```bash
tmux new-session -d -s claude-work
tmux send-keys -t claude-work 'cd /project && claude' Enter
tmux send-keys -t claude-work 'Refactor auth module' Enter
tmux capture-pane -t claude-work -p -S -50
tmux kill-session -t claude-work
```

### Reference Files

- `references/claude-code/setup-authentication.md`
- `references/claude-code/environment.md`
- `references/claude-code/interactive-session.md`
- `references/claude-code/mcp-integration.md`
- `references/claude-code/monitoring.md`
- `references/claude-code/pitfalls-and-performance.md`

---

## 2. Codex (OpenAI)

### Prerequisites

- `npm install -g @openai/codex`
- OpenAI auth: `OPENAI_API_KEY` or Codex OAuth (`~/.codex/auth.json`)
- **Must run inside a git repository**
- Use `pty=true` — Codex is an interactive terminal app

### One-Shot Tasks

```bash
# Simple task
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)

# Scratch work (needs git repo)
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

### Background Mode (Long Tasks)

```bash
# Start
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)

# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if prompted
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot, exits when done |
| `--full-auto` | Sandboxed, auto-approves file changes |
| `--yolo` | No sandbox, no approvals (fastest, dangerous) |
| `--sandbox danger-full-access` | No Codex sandbox (for gateway contexts) |

### Gateway Caveat

In Hermes gateway/service contexts, Codex sandboxing may fail (bubblewrap errors). Use:
```bash
codex exec --sandbox danger-full-access "<task>"
```
Use process boundaries as safety layer instead.

### PR Reviews

```bash
# Clone to temp for safe review
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

### Parallel Issue Fixing with Worktrees

```bash
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <desc>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <desc>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

### Batch PR Reviews

```bash
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

### Rules

1. Always use `pty=true`
2. Git repo required — use `mktemp -d && git init` for scratch
3. Use `exec` for one-shots
4. `--full-auto` for building
5. Background + `process` for long tasks
6. Don't interfere — be patient with long-running tasks
7. Parallel is fine — run multiple Codex processes for batch work

---

## 3. OpenCode

### Prerequisites

- `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`
- Auth: `opencode auth login` or provider env vars (`OPENROUTER_API_KEY`, etc.)
- Verify: `opencode auth list` shows at least one provider
- Git repo recommended
- `pty=true` for interactive TUI sessions

### Binary Resolution

```bash
which -a opencode
opencode --version
# Pin if needed: $HOME/.opencode/bin/opencode
```

### One-Shot Tasks

```bash
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")

# Attach context files
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")

# Show thinking
terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")

# Force model
terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

### Interactive Sessions (Background)

```bash
# Start TUI in background
terminal(command="opencode", workdir="~/project", background=true, pty=true)

# Send prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Follow-up
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or: process(action="kill", session_id="<id>")
```

**Important:** Do NOT use `/exit` — opens agent selector. Use Ctrl+C (`\x03`) or `process(action="kill")`.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit (press twice if needed) |
| `Tab` | Switch agents (build/plan) |
| `Ctrl+P` | Command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit |

### Resuming Sessions

```bash
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # Continue last
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # Specific
```

### Common Flags

| Flag | Use |
|------|-----|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue last session |
| `--session <id>` / `-s` | Continue specific session |
| `--agent <name>` | Choose agent (build or plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output |
| `--file <path>` / `-f` | Attach file(s) |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort (high, max, minimal) |
| `--title <name>` | Name the session |

### PR Review Workflow

```bash
# Built-in PR command
terminal(command="opencode pr 42", workdir="~/project", pty=true)

# Isolated review in temp clone
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\\n' ' ')", pty=true)
```

### Parallel Work Pattern

```bash
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

### Session & Cost Management

```bash
# List past sessions
opencode session list

# Token usage and costs
opencode stats
opencode stats --days 7 --models anthropic/claude-sonnet-4
```

### Pitfalls

- Interactive TUI requires `pty=true`; `opencode run` does NOT
- `/exit` is NOT valid — use Ctrl+C
- PATH mismatch can select wrong binary
- If stuck, inspect logs before killing
- Avoid sharing workdir across parallel sessions
- Enter may need double-press to submit

### Rules

1. Prefer `opencode run` for one-shot — simpler, no pty needed
2. Interactive background only when iteration needed
3. Always scope sessions to single repo/workdir
4. Long tasks: provide progress updates from `process` logs
5. Report concrete outcomes (files changed, tests, risks)
6. Exit with Ctrl+C or kill, never `/exit`

---

## 4. Codebase Inspection

### Core Activities

1. **Metrics** — Lines of code, language/file distribution
2. **Structure** — Entry points, modules, dependency graph
3. **Quality Signals** — Complexity hotspots, test coverage

### Teaching Approach

- Inspect one repository end-to-end
- Identify one onboarding path
- Propose one refactor target

### Usage

Use for initial repo assessment before delegating to coding agents. Provides context for task decomposition.

---

## Cross-Agent Patterns

### Worktree Isolation (All Agents)

```bash
# Standard pattern
git worktree add -b fix/issue-N /tmp/issue-N main
# Launch agent in /tmp/issue-N
# After: push, create PR, git worktree remove /tmp/issue-N
```

### Parallel Fan-Out

```bash
# Launch N agents in parallel
delegate_task(tasks=[
  {"goal": "Fix issue #1", "toolsets": ["terminal", "file"], "workdir": "/tmp/issue-1"},
  {"goal": "Fix issue #2", "toolsets": ["terminal", "file"], "workdir": "/tmp/issue-2"},
  {"goal": "Fix issue #3", "toolsets": ["terminal", "file"], "workdir": "/tmp/issue-3"},
])
```

### Batch PR Review

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Parallel review
delegate_task(tasks=[
  {"goal": "Review PR #N. git diff origin/main...origin/pr/N", "toolsets": ["terminal", "file"], "workdir": "~/project"},
  ...
])

# Post comments
gh pr comment N --body '<review>'
```

---

## Verification Checklist

- [ ] Right agent selected per decision guide
- [ ] Auth configured for chosen agent
- [ ] Git repo exists at workdir
- [ ] Worktree created for isolation (if parallel)
- [ ] Mode matches task (print vs interactive)
- [ ] Progress monitored for long tasks
- [ ] Concrete outcomes reported (files, tests, risks)
- [ ] Clean exit (Ctrl+C/kill, not `/exit`)