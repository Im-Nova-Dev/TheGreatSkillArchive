---
name: go-error-handling-design
description: Teach Go error handling design patterns including error wrapping, sentinel errors, custom error types, and graceful error management strategies
tags:
  - golang
  - error-handling
  - teaching
---

# Go Error Handling Design

## Purpose
Teach Go error handling as a deliberate design activity. Use this skill when teaching error patterns, designing APIs, debugging error flow, or reviewing error-related code.

## Core Philosophy
- Errors are values
- Handle errors where they occur
- Add context at each layer
- Preserve error identity for inspection
- Distinguish expected vs unexpected errors

## Error Types

### Sentinel Errors
- Package-level variables for common failures
- Compare with `errors.Is`
- Use for stable known errors inside a package
- Avoid exporting sentinel errors from libraries

### Custom Error Types
- Implement `Error()` and optionally `Unwrap()`
- Use for structured error data
- Compare with `errors.As`

### Error Wrapping
- `%w` in `fmt.Errorf` for wrapping
- Unwrap with `errors.Unwrap` or chain with `errors.Is`/`errors.As`
- Use defer cleanup patterns with wrapped errors

### Abort Patterns
- Return early on error
- Guard clauses
- Reduce nesting with early returns

## Error Handling Strategies

### Return and Propagate
- Caller decides whether to handle, wrap, or abort

### Log and Return
- Log once at boundary
- Do not log and return same error

### Retry with Backoff
- Retry transient errors: network, temporary files
- Use exponential backoff
- Use context for cancellation

### Graceful Degradation
- Fallback on failure
- Partial results when possible
- Keep service running when non-critical path fails
