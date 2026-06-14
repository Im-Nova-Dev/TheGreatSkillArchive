---
name: ai-agent-runtime-debugger
description: "Debug agent bundles, hook failures, and spinoff toolchains."
version: 0.1.0
category: technology
---

# AI Agent Runtime Debugger

## Overview

Debug agent bundles, hook failures, and spinoff toolchains. This skill provides systematic approaches for debugging AI agent runtime issues including bundle loading failures, hook execution problems, toolchain spinoff errors, and runtime state inspection.

## When To Use

- When an agent fails to start or crashes during initialization
- When hooks (pre/post tool, pre/post message) fail silently or throw errors
- When spinoff toolchains (subagents, delegated tasks) don't execute correctly
- When you need to inspect runtime state, memory, or configuration at debug time
- When agent behavior diverges from expected contract/behavior

## Prerequisites

- Access to the agent runtime environment (local or remote)
- Ability to run diagnostic commands (hermes CLI, logs, process inspection)
- Basic familiarity with the agent architecture (bundles, hooks, toolchains)

## Workflow

### Phase 1: Information Gathering

1. **Collect runtime metadata**
   ```bash
   hermes status                    # Overall system status
   hermes config show              # Active configuration
   hermes tool list                # Available tools and their status
   hermes profile list             # Available profiles
   ```

2. **Capture recent logs**
   ```bash
   hermes logs --tail 100          # Recent runtime logs
   hermes logs --level error       # Error-level logs only
   journalctl -u hermes --since "1 hour ago"  # Systemd logs (if applicable)
   ```

3. **Identify the failing component**
   - Bundle name/version
   - Hook name and trigger point
   - Toolchain/spinoff identifier
   - Error message or symptom description

### Phase 2: Bundle Debugging

1. **Validate bundle integrity**
   ```bash
   hermes bundle verify <bundle-name>    # Check bundle structure
   hermes bundle inspect <bundle-name>   # Show bundle metadata
   ```

2. **Test bundle loading in isolation**
   ```bash
   hermes run --bundle <bundle-name> --dry-run  # Validate without execution
   hermes run --bundle <bundle-name> --verbose  # Verbose execution trace
   ```

3. **Check dependencies**
   ```bash
   hermes bundle deps <bundle-name>    # List declared dependencies
   pip list | grep -E "<dependency>"   # Verify Python deps
   npm list <dependency>               # Verify Node deps (if applicable)
   ```

### Phase 3: Hook Debugging

1. **List registered hooks**
   ```bash
   hermes hook list                    # All registered hooks
   hermes hook list --type pre_tool    # Filter by type
   ```

2. **Test hook execution manually**
   ```bash
   hermes hook test <hook-name> --input '{"tool": "example", "args": {}}'
   ```

3. **Enable hook tracing**
   ```bash
   HERMES_HOOK_TRACE=1 hermes run ...  # Trace hook entry/exit
   ```

4. **Common hook failure patterns**
   - **Timeout**: Hook exceeds execution budget → optimize or increase timeout
   - **Import error**: Missing dependency in hook environment → verify venv
   - **State corruption**: Hook mutates shared state incorrectly → use immutable patterns
   - **Schema mismatch**: Input/output doesn't match contract → validate schemas

### Phase 4: Toolchain/Spinoff Debugging

1. **Inspect spawning configuration**
   ```bash
   hermes config get delegation.max_concurrent_children
   hermes config get delegation.max_spawn_depth
   ```

2. **Test spinoff in isolation**
   ```bash
   hermes delegate --goal "test task" --toolsets '["terminal"]' --timeout 30
   ```

3. **Check child process logs**
   ```bash
   hermes logs --child <child-session-id>  # If supported
   # Or check child working directory for logs
   ```

4. **Common spinoff issues**
   - **Context loss**: Parent context not passed correctly → check `context` field
   - **Toolset inheritance**: Child missing required tools → verify toolsets config
   - **Transport failure**: ACP/stdio transport broken → test with simple echo
   - **Resource exhaustion**: Too many concurrent children → check limits

### Phase 5: Runtime State Inspection

1. **Memory/state dump**
   ```bash
   hermes debug state --session <id>     # Dump session state
   hermes debug memory --session <id>    # Memory usage snapshot
   ```

2. **Configuration validation**
   ```bash
   hermes config validate                # Check config syntax and schema
   hermes config diff                    # Show differences from defaults
   ```

3. **Tool execution tracing**
   ```bash
   HERMES_TOOL_TRACE=1 hermes run ...    # Trace all tool calls
   ```

## Example Usage

```bash
# Full debug session for a failing agent
hermes status
hermes logs --level error --tail 50
hermes bundle verify my-agent-bundle
hermes hook list --type pre_tool
HERMES_HOOK_TRACE=1 hermes run --bundle my-agent-bundle --goal "test"
hermes delegate --goal "isolated test" --toolsets '["terminal"]'
```

## Verification Steps

After applying fixes:
1. Run the original failing scenario again
2. Verify no error logs appear in `hermes logs --level error`
3. Confirm expected output/behavior matches contract
4. Run regression test suite if available

## Reference Notes

- Auto-generated on 2026-06-05
- Expanded with debugging workflows on 2026-06-06
- Key files: ~/.hermes/config.yaml, ~/.hermes/logs/, ~/.hermes/bundles/
- Related skills: agent-contract-validator, agent-tool-auditor, agent-swarm-runner
- For Hermes-specific debugging, see: https://hermes-agent.nousresearch.com/docs