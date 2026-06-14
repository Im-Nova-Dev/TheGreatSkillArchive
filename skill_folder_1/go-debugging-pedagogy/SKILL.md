---
name: go-debugging-pedagogy
description: Teach Go debugging as both a mindset and a tool workflow. Covers systematic debugging, Delve, runtime inspection, and translating errors into fixes.
tags:
  - golang
  - debugging
  - teaching
---

# Go Debugging Pedagogy

## Purpose
Teach debugging in Go through investigation, not just answers. Use this skill when a learner has a bug, an unclear error, or needs to build debugging habits.

## Teaching Mindset
- Treat debugging as investigation, not punishment
- Require a theory before running fixes
- Ask: what did you expect, what happened, where is the mismatch?
- Normalize error messages; they are data, not failures
- Use rubber ducking as a first step

## Systematic Steps
1. Reproduce minimally
2. Read the full error and stack
3. Isolate the smallest failing case
4. Form a hypothesis
5. Test one change
6. Verify the fix and check side effects

## Go-Specific Habits
- Run `go vet ./...` before debugging
- Read stack traces bottom-up
- Check nil errors before values
- Use `%w` so errors can be unwrapped and traced
- Inspect goroutine state for leaks or unexpected activity

## Tool Tools
- `delve`:
  - `dlv debug`
  - breakpoints: `break`, `continue`, `next`, `step`
  - inspect vars: `print`, `locals`
  - goroutines: `goroutines`, `goroutine <id>`
- `pprof`: CPU, memory, goroutine profiles
- `runtime/pprof` and net/http/pprof

## Common Beginner Debugging Targets
- Missing error checks
- Nil pointer dereference
- Loop variable capture in closures/goroutines
- Misuse of `break` in `for/select`
- Range variable reuse in loops

## Teaching Templates
Template: predict
- Present buggy behavior
- Ask learner to predict output
- Reveal output
- Explain only what changed

Template: fix
- Present bug
- Ask learner to identify cause
- Reveal one fix
- Explain root cause

## Common Intermediate Targets
- Escaping pointers causing unexpected heap allocation
- Mutex value copy
- Misclosed channels or sender closes twice
- JSON unmarshal zero-value enums
- Context deadline exceeded vs canceled

## Classroom Patterns
- Show broken code first; ask learner to predict failure
- Rewrite the error message into a question
- Use print debugging only as a temporary scaffold
- Transition to Delve after 2 failed print attempts

## Example: Debugging Loop Capture
Bug:
```go
for i := 0; i < 3; i++ {
    go func() {
        fmt.Println(i)
    }()
}
```
Ask: What range of outputs do you expect? What actually prints?
Fix:
```go
for i := 0; i < 3; i++ {
    i := i
    go func() {
        fmt.Println(i)
    }()
}
```

## Example: Error Wrapping Debugging
Bug:
```go
return fmt.Errorf("failed: %v", err)
```
Problem: loses error identity
Fix:
```go
return fmt.Errorf("failed: %w", err)
```
Then: `errors.Is` and `errors.As` work correctly

## Assessment
- Learner writes a hypothesis before running
- Learner can read a stack trace and find the file
- Learner prefers Delve after practice
- Learner checks first whether error was ignored
