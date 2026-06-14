---
name: go-concurrency-patterns-teaching
description: Teach Go concurrency patterns with working examples, common pitfalls, and progressive difficulty. Covers goroutines, channels, select, worker pools, and context usage.
tags:
  - golang
  - concurrency
  - teaching
---

# Go Concurrency Patterns Teaching

## Purpose
Teach Go concurrency in a structured way from basic goroutines through production-ready patterns. Use this skill when explaining channels, select, worker pools, or designing concurrent Go code.

## Teaching Rules
- Emphasize goroutine ownership and completion
- Use `sync.WaitGroup` before introducing channels
- Introduce channels as communication, not just data passing
- Teach context and cancellation with every concurrent example
- Avoid `time.Sleep` in production examples
- Explain difference between concurrency and parallelism

## Level Progression

### Beginner
- Goroutines: `go func()`
- WaitGroups: `wg.Add`, `defer wg.Done()`, `wg.Wait()`
- Closure capture bug: loop variable capture

### Intermediate
- Channels: send, receive, close, `range`
- Buffered vs unbuffered
- Select with multiple channels
- Timeout patterns with `time.After` and context

### Advanced
- Worker pools with fixed goroutine counts
- Pipelines with owned stages and channel closing
- Errgroup for structured error propagation
- Fan-out/fan-in patterns
- Rate limiting and backpressure

## Common Beginner Mistakes
- Launching goroutines without completion signal
- Capturing loop variable instead of passing it
- Expecting `print` statements to serialize across goroutines
- Using `break` to exit outer loop inside select
- Assuming map iteration order under concurrency

## Common Intermediate Mistakes
- Closing channels from receiver side
- Unbuffered channels causing unexpected blocking
- Not handling closed channel panics
- Mixing context cancellation and select incorrectly
- Spawning goroutines without cancellation

## Teaching Templates
- Concept: `<title>`
- Example: `<snippet>`
- Exercise: `<task>`
- Mistake: `<buggy snippet>`
- Fix: `<corrected snippet>`

## Essential Patterns

### WaitGroup
```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    doWork()
}()
wg.Wait()
```

### Closure Capture Bug
Bug:
```go
for i := 0; i < 3; i++ {
    go func() { fmt.Println(i) }()
}
```
Fix:
```go
for i := 0; i < 3; i++ {
    i := i
    go func() { fmt.Println(i) }()
}
```

### Channel Directions
```go
func send(ch chan<- string)  { ch <- "data" }
func recv(ch <-chan string)  { <-ch }
```

### Select
```go
select {
case <-ctx.Done():
    return ctx.Err()
case v := <-ch:
    process(v)
case <-time.After(time.Second):
    return errors.New("timeout")
}
```

### Worker Pool
```go
sem := make(chan struct{}, n)
for _, item := range items {
    item := item
    g.Go(func() error {
        sem <- struct{}{}
        defer func() { <-sem }()
        return process(item)
    })
}
```

## Exercises
- Predict race condition in shared counter without mutex
- Convert spinning goroutine to WaitGroup
- Build producer/consumer with channel
- Add timeout to channel read
- Build worker pool with fixed goroutines
- Add context cancellation to pool

## Lesson Generation Rules
- Use shared variable state as a learning tool
- Start with a race, then show the safe version
- Use one hand-drawn style diagram in ASCII if possible
- Always include a runnable snippet
- Ask learner to name the bug before naming the concept

## Lesson Templates
Template: race-to-safe
- Show unsafe code
- Ask for output
- Show unsafe output
- Show fixed code
- Explain underlying concept

Template: analogy
- Concept: goroutine
- Analogy: runner on track
- Concept: channel
- Analogy: baton pass
- Concept: context
- Analogy: whistle for all runners
- Concept: select
- Analogy: first person to raise hand gets asked

## Example Lesson: Closure Capture
Introduction: What does this print?
```go
for i := 0; i < 3; i++ {
    go func() {
        fmt.Println(i)
    }()
}
time.Sleep(100 * time.Millisecond)
```
Expected wrong answers: 0 1 2
Reveal: 3 3 3
Fix: pass i explicitly
Why: loop variable reused across iterations

## Assessment Checklist
- Can explain goroutine lifecycle
- Can identify closure capture bug
- Can choose channel vs mutex correctly
- Can design worker pool with bounded concurrency
- Can use context for cancellation and timeouts
- Can read and reason about select behavior
