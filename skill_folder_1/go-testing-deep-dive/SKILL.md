---
name: go-testing-deep-dive
description: Teach Go testing beyond basics including table-driven tests, subtests, benchmarks, fuzz tests, httptest, and test organization
tags:
  - golang
  - testing
  - tdd
---

# Go Testing Deep Dive

## Purpose
Teach Go testing with progressive depth. Use this skill when writing tests, explaining stdlib testing, benchmarks, fuzz, or promoting test-first habits.

## Core Philosophy
- Test behavior, not implementation
- Prefer small focused tests
- Use table-driven tests for multiple cases
- Avoid test logic duplication
- Run tests often; make them fast

## Table-Driven Tests
Pattern:
```go
tests := []struct {
    name    string
    input   int
    want    int
}{
    {"positive", 2, 4},
    {"negative", -1, -1},
    {"zero", 0, 0},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got := Double(tt.input)
        if got != tt.want {
            t.Errorf("got %d, want %d", got, tt.want)
        }
    })
}
```

## Subtests and Parallelism
- Use `t.Run` for named subtests
- Use `t.Parallel()` for independent tests
- Combine both for large tables

## Testing Output
- Use `t.Log`, `t.Logf` for verbose output
- Use `t.Helper()` for test helpers
- Use `t.Fatalf` when continuing is meaningless

## Benchmarking
- Signature: `func BenchmarkX(b *testing.B)`
- Use `b.N` for iterations
- Reset timer after setup: `b.ResetTimer()`
- Use `-bench`, `-benchmem`, `-run` flags

## Fuzz Testing
- Signature: `func FuzzX(f *testing.F)`
- Add seed corpus with `f.Add`
- Run with `-fuzz`
- Use for parsing, encoding, untrusted input

## HTTP Testing
- Use `net/http/httptest`
- `httptest.NewRecorder` for response capture
- `httptest.NewServer` for server testing
- Test handlers, middleware, routing

## Test Organization
- Keep tests close to code: `foo_test.go` next to `foo.go`
- Use `testdata/` for golden files and fixtures
- Use `internal` to limit test surface

## Common Beginner Mistakes
- Comparing slices with `==`
- Not using subtests for tables
- Sharing state between parallel tests
- Testing private functions directly
- Using `time.Now()` causing flaky tests

## Common Intermediate Mistakes
- Over-mocking; testing implementation details
- Large one-test functions covering many behaviors
- Missing error path checks
- Not cleaning up temp files or servers
- Assuming map key order in assertions

## Teaching Sequence
1. Write a function, then write a failing test
2. Make it pass; refactor
3. Introduce table-driven tests for multiple inputs
4. Introduce benchmarks and fuzz
5. Show httptest for API testing
6. Discuss test philosophy: Red-Green-Refactor

## Example: httptest Handler
```go
func TestHealthz(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(healthz)
    handler.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("status: got %d, want %d", rr.Code, http.StatusOK)
    }
}
```

## Assessment Checklist
- Can write a table-driven test
- Can add subtests and run in parallel
- Can write a benchmark
- Can write a basic fuzz test
- Can test an HTTP handler with httptest
- Can explain why not to test implementation details
