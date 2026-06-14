---
name: go-performance-optimization
description: Teach Go performance optimization using profiling, benchmarks, memory analysis, and practical tuning techniques for production systems.
tags:
  - golang
  - performance
  - profiling
  - pprof
---

# Go Performance Optimization

## Purpose
Teach Go performance optimization as a measurement-driven process. Use this skill when profiling, benchmarking, tuning memory, or teaching how to make Go programs faster and more efficient.

## Core Philosophy
- Measure before optimizing
- Optimize hot paths, not everything
- Fewer allocations often beats algorithmic improvements in Go
- Understand stack vs heap and escape analysis
- Profile in production-like conditions

## Profiling Tools
- `net/http/pprof` endpoints
- `runtime/pprof` profiles: cpu, heap, goroutine, block, mutex
- `go tool pprof` for analysis
- `go tool trace` for latency and scheduling
- `runtime.MemStats` for metrics

## Benchmarking
- `go test -bench=.`
- `b.N` controlled iteration
- Avoid compiler inlining traps with side effects
- Use `b.ResetTimer` after setup
- Benchmark memory: `-benchmem`

## Memory Optimization
- Prefer value receivers for small types
- Preallocate slices with capacity when size is known
- Use `sync.Pool` for reuse of frequent temporary objects
- Reduce string concatenation with `strings.Builder`
- Use `bytes.Buffer` for streaming or large text
- Inspect with `pprof` heap to find leak sources

## Escape Analysis
- Use `go build -gcflags="-m -m"` to inspect escapes
- Keep short-lived objects on stack when possible
- Avoid returning pointers to local variables unnecessarily
- Pass large structs by pointer only when mutation or size justifies it

## Concurrency Tuning
- Use worker pools to bound concurrency
- Avoid goroutine leaks: contexts and cancellation
- Batch work to reduce per-item overhead
- Prefer channels for handoff; mutex for shared state

## Common Mistakes
- Premature optimization without profiling
- Ignoring `sync.Pool` reset before reuse
- Memory leaks from unclosed resources
- Benchmarking without disabling GC or accounting for noise
- Overusing pointers thinking they avoid copies

## Teaching Sequence
1. Benchmark baseline
2. Profile CPU and memory
3. Identify hotspot
4. Apply optimization with hypothesis
5. Re-measure
6. Discuss tradeoffs

## Exercises
- Profile and optimize string concatenation
- Reduce allocations in hot loop
- Fix goroutine leak with context
- Compare value vs pointer receiver benchmark

## Assessment Checklist
- Can profile CPU and heap with pprof
- Can interpret benchmark output
- Can use escape analysis flags
- Can explain when sync.Pool helps
- Can measure before and after changes
