---
name: native-mcp
description: Teach native MCP client and server usage including protocol concepts, tool exposure, resource URIs, transport options, server configuration, security, debugging, and integration patterns with teaching exercises.
---

# Native MCP

## Core concepts
- Client/server model
- Tool and resource surfacing
- JSON-RPC over stdio
- `initialize`, `tools/list`, `tools/call`

## Implementation
- Transport choices: `stdio`, SSE/HTTP
- Server capabilities
- Config entry shape, absolute paths, env forwarding

## Teaching approach
- Inspect one native MCP setup.
- Add one simple tool.
- Test client interaction end to end.

## Troubleshooting
See `references/troubleshooting.md` for triage steps, common failure modes, and exact call templates.

## Related files
- `references/troubleshooting.md`
