# Native MCP Troubleshooting

Use this reference when diagnosing MCP client/server wiring, tool discovery, transport, permissions, or startup issues for Hermes's built-in MCP support.

## Quick triage
1. Check which MCP server entries are actually loaded.
2. Verify transport, command, and environment for each enabled server.
3. Reproduce tool discovery and call manually.
4. Fix config and restart.

## Symptoms and fixes

### No MCP tools appear
- Cause: No servers are configured, or all servers are disabled.
- Fix: Add at least one MCP server entry in Hermes config; restart Hermes.
- Verify: Hermes logs show "MCP client initialized"; tools from the server are exposed.

### Server fails to start
- Cause: Wrong command path, missing dependency, bad environment, bad JSON args, permissions.
- Command-line check: Run the exact `command` + `args` from the config manually.
- Common fixes:
  - Use absolute paths.
  - Avoid login shells: prefix with `bash -lc` or `sh -lc` only when required.
  - Confirm Python/Node runtimes are installed.
  - For async servers, verify `stdio` transport is supported; stdio is the expected default.

### Timeout / never responds
- Cause: Server hung waiting for input, buffered stdout, wrong JSON lines framing.
- Fix: Ensure server reads line-delimited JSON-RPC from stdin and writes to stdout.
- Try increasing transport timeout if Hermes exposes one.
- Background servers: confirm foreground server process is used for stdio transport.

### Calls succeed but return empty / wrong schema
- Cause: Tool response does not match MCP tool call result schema.
- Required shape:
  ```
  { "content": [{ "type": "text", "text": "..." }] }
  ```
- Common mistake: returning raw strings or objects instead of a list under `content`.
- Fix: Wrap response in the expected `content` array structure.

### Permission denied / sandboxed file access failed
- Cause: Container or sandbox profile blocks filesystem or network access.
- Fix:
  - Add needed path bind mounts or `volumes` in container config.
  - Check Hermes container run arguments; do not drop NET_RAW or other needed capabilities unless required.
  - For Docker-in-Docker setups, ensure sibling container access via host networking or proper endpoint.

### TLS / HTTPS / proxy errors when using SSE/HTTP transport
- Cause: Certificate validation failure, DNS inside container, proxy env not propagated.
- Fix:
  - Verify `HTTPS_PROXY` / `NO_PROXY` are passed to the container env.
  - Test `curl` from the same runtime context.
  - Prefer mTLS trusted CA bundle mounted into the container.

## Validation steps
1. Server process logs: `stderr` from the server command should show protocol messages or errors.
2. Manual run: replicate exact command/args/env in a terminal and send JSON-RPC lines manually.
3. Inspect config: confirm entry is present, enabled, and uses expected transport type.
4. Restart flow: restart Hermes and confirm MCP init messages in logs.

## Reference command template
```bash
cat <<'EOF' | your-mcp-server
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
EOF
```

## Further reading
- Hermes Agent MCP docs: https://hermes-agent.nousresearch.com/docs
- MCP protocol spec: https://modelcontextprotocol.io/specification
