---
name: agent-swarm-runner
description: "Run and manage agent swarms with governor controls and budgets."
version: 0.2.0
category: technology
---

# Agent Swarm Runner

## Overview

Run and manage agent swarms using Hermes delegation features. This skill covers spawning multiple subagents (Codex, Claude Code, OpenCode) in parallel, coordinating their work, and aggregating results with budget controls.

## When To Use

- Running multiple independent coding tasks in parallel (features, PRs, reviews)
- Distributing work across different agent CLIs for comparison or redundancy
- Managing compute budgets and time limits for agent pools
- Orchestrating multi-agent workflows with dependencies

## Prerequisites

- Hermes Agent with delegation enabled (`delegation.enabled: true` in config.yaml)
- At least one ACP-compatible CLI installed (Codex, Claude Code, or OpenCode)
- `delegation.max_concurrent_children` set appropriately (default: 3)

## Workflow

### 1. Single Task Delegation

```yaml
# Delegate a single feature to Codex
delegate_task:
  goal: "Implement user authentication API endpoints"
  context: |
    Repo: github.com/org/repo
    Stack: FastAPI + PostgreSQL + JWT
    Files: app/api/auth.py, app/models/user.py, tests/test_auth.py
  toolsets: ["terminal", "file", "search"]
```

### 2. Parallel Batch Delegation

```yaml
# Run multiple tasks concurrently
delegate_task:
  tasks:
    - goal: "Write unit tests for payment module"
      context: "Module: app/payments/, use pytest + pytest-mock"
      toolsets: ["terminal", "file"]
    - goal: "Refactor notification service"
      context: "File: app/services/notifications.py, add async support"
      toolsets: ["terminal", "file"]
    - goal: "Update API documentation"
      context: "OpenAPI spec in docs/api.yaml, add new endpoints"
      toolsets: ["file", "search"]
```

### 3. With Budget Controls

```yaml
delegate_task:
  goal: "Research and implement caching layer"
  context: "Evaluate Redis vs in-memory for session cache"
  toolsets: ["terminal", "file", "web"]
  # Implicit budget via max_concurrent_children and timeout
```

### 4. Orchestrator Pattern (for complex workflows)

```yaml
delegate_task:
  goal: "Coordinate full feature: design → implement → test → document"
  toolsets: ["terminal", "file", "web"]
  role: "orchestrator"  # Can spawn own workers
  # Note: Requires delegation.max_spawn_depth >= 1
```

## Key Configuration

```yaml
# ~/.hermes/config.yaml
delegation:
  enabled: true
  max_concurrent_children: 3
  max_spawn_depth: 0  # Set to 1 to enable orchestrator role
  default_toolsets: ["terminal", "file", "search", "web"]
```

## Agent CLI Options

| CLI | ACP Command | Best For |
|-----|-------------|----------|
| Codex | `copilot --acp --stdio` | OpenAI-powered, good for features/PRs |
| Claude Code | `claude --acp` | Anthropic, strong reasoning |
| OpenCode | `opencode --acp` | Local-first, good for refactoring |

Set via `acp_command` in delegate_task or default in config.

## Result Handling

Subagents return summaries. Always verify external side-effects:

```python
# Example verification pattern
result = delegate_task(...)
for task_result in result:
  if task_result.claims_file_created:
    verify_with_read_file(task_result.path)
  if task_result.claims_http_post:
    verify_with_web_extract(task_result.url)
```

## Common Pitfalls

- **No user interaction**: Subagents cannot use `clarify` — pass all context upfront
- **No execute_code**: Leaf agents can't run Python tool scripts
- **Silent cancellation**: Parent interruption cancels children; use cronjob for durable work
- **Memory isolation**: Subagents don't inherit parent memory — pass via `context`
- **Language drift**: Specify language in context if non-English output needed

## Verification Steps

1. Check delegation config: `hermes config get delegation`
2. Test single delegation: `delegate_task` with simple goal
3. Test batch: 2-3 parallel tasks with different toolsets
4. Verify results: read files, check URLs, run tests

## Reference Notes

- Based on Hermes delegation system (max_concurrent_children=3 for this user)
- Nesting disabled by default (max_spawn_depth=1 for this user)
- Update this skill when new agent CLIs or delegation features are added
- Auto-expanded on 2026-06-06 from skeleton template