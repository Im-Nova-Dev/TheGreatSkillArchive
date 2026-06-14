---
name: go-system-programming
description: Teach Go system programming including Linux syscalls, file descriptors, processes, signals, and low-level OS interaction.
tags:
  - golang
  - system-programming
  - linux
---

# Go System Programming

## Purpose
Teach Go system programming for learners interested in OS interaction, tools, and low-level programming. Use this skill when teaching file descriptors, processes, syscalls, signals, and Linux-specific Go code.

## Teaching Rules
- Treat OS calls as fallible resources; always handle errors
- Use absolute timeouts and cancellation on every syscall wrapper
- Focus on stdlib first; use `golang.org/x/sys/unix` when needed
- Explain file descriptor semantics, limits, and leaks

## Core Topics

### File Descriptors and I/O
- `os.Open`, `os.Create`, `os.OpenFile`
- `os.File` methods and `io.Reader`/`io.Writer`
- `io.Copy`, `io.CopyBuffer`, `io.ReadAll`
- `filepath` vs `path`

### Processes and Commands
- `os/exec.Command`, `CombinedOutput`, `Output`
- Forwarding stdin/stdout/stderr with `Stdio`
- Exit status and error wrapping from `exec.ExitError`

### Signals
- `os/signal.Notify`, `signal.Stop`
- Graceful shutdown pattern with `signal.Context`
- Cleanup in deferred handlers

### Users, Groups, and Permissions
- `os/user`, `os.Chown`, `os.Chmod`
- `os.Getuid`, `os.Getgid`
- Caveats in containers and CI

### Timers and Time
- `time.After`, `time.NewTimer`, `time.Ticker`
- `time.Sleep` only in tests or examples
- Monotonic clock behavior

### Networking at the OS Level
- `net.TCPListener`, `net.File` for inherited sockets
- Ephemeral ports and reuse
- `SO_REUSEADDR` analogs by `net` package semantics

### Advanced syscall usage
- Prefer `golang.org/x/sys/unix` over `syscall`
- Build tags for platform-specific files
- Avoid raw syscalls unless necessary

## Common Mistakes
- Forgetting to close files and leaking descriptors
- Ignoring `exec.ExitError` and treating non-zero as unknown failure
- Using `signal.Notify` without clearing on shutdown
- Assuming signals are queued
- Using `time.Now()` in hot loops

## Teaching Sequence
1. File descriptors as integers
2. Open, read, write, close lifecycle in Go
3. Process execution basics
4. Signal handling and graceful shutdown
5. When stdlib is insufficient and `unix` is needed
6. Observability: file limits with `ulimit`

## Example: Graceful Shutdown
```go
ctx, stop := signal.NotifyContext(context.Background(),
    syscall.SIGINT, syscall.SIGTERM)
defer stop()

srv := &http.Server{Addr: ":8080", Handler: handler}
go srv.ListenAndServe()

<-ctx.Done()
shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
srv.Shutdown(shutdownCtx)
```

## Exercises
- Build a minimal `cat` clone
- Implement process supervisor with restart and backoff
- Add signal-safe cleanup for temp dirs
- Implement `sof` like lite view using `/proc`

## Assessment Checklist
- Can explain file descriptor lifecycle and closing contracts
- Can run external processes and interpret exit status
- Can add signal-based graceful shutdown
- Can choose stdlib vs `golang.org/x/sys/unix` appropriately
