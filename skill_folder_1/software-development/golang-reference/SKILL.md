---
name: golang-reference
description: Practical Go reference for writing, running, and checking Go programs on this system, with idioms, stdlib, project layout, modules, concurrency, testing, and safe editing rules. Serve as a strong assistant reference for any Go task.
---

# Go reference for this environment and general use

Facts for this system:
- Go 1.26.3
- GOPATH: /home/nova/go
- GOMODCACHE: /home/nova/go/pkg/mod
- Modules are enabled and modern Go workflow applies
- Use `go run`, `go build`, `go test`, `go vet`, `staticcheck` when available

Reference topics:
- project layout
- syntax and idioms
- stdlib modules
- tooling
- concurrency and error handling
- testing and benchmarks
- common pitfalls
- editing/running rules

# Project layout and modules
Common layout:
- cmd/<name>/main.go entrypoints
- internal/ private application code
- pkg/ public library code if needed
- api/, scripts/, configs/ as needed

Module setup:
  go mod init github.com/<user>/<project>
  go get, go mod tidy
  Keep go.sum clean; avoid replacing stdlib versions
  Use Go workspace (go.work) for multi-module repos when needed

# Syntax and style rules
- Format with `gofmt`; never reformat block style manually
- Naming:
  - packages: lowercase single word
  - exported: CamelCase
  - unexported: camelCase
  - error variables end with `Err` or `err`
- Comments:
  - package comments for main package doc
  - exported names must have doc comments
- Error handling:
  - check errors immediately, do not swallow
  - wrap with `fmt.Errorf("context: %w", err)`
  - do not panic in library code
- Avoid naked returns in long functions; named returns acceptable if short
- Use `defer` for cleanup in the same block where resource opens
- Use zero values explicitly when default struct initialization is required
- initialize maps and slices via `make` or literal
- do not copy mutexes, sync types by value
- avoid `init()` where constructor can do the same work more predictably

# Stdlib essentials by category
IO and filesystem:
  os, os/exec, path/filepath, io, io/fs, bufio, bytes, strings, strconv, fmt, log/slog

Data:
  encoding/json, encoding/xml, encoding/csv, encoding/base64, encoding/hex
  database/sql, errors, fmt, reflect, unsafe (avoid when possible)

Collections:
  slices, maps; container/* optional for linked list/ring/heap
  sort, search, maps (ordered map iteration in Go 1.21+)

Text and time:
  strings, strconv, text/scanner, unicode, time, time/tzdata

Networking:
  net, net/http, net/url, net/mail, crypto/tls

Context and cancellation:
  context.Context, context.WithTimeout, context.WithCancel, context.WithValue

Concurrency:
  sync, sync/atomic, runtime, time
  channels and select
  errgroup.Group, semaphore patterns via chan or golang.org/x/sync/semaphore

CLI:
  flag, os.Args, os/exec, bufio.Scanner

Logging and telemetry:
  log, log/slog, expvar, runtime/debug, runtime/metrics

Testing:
  testing, testing/quick, testing/fstest, testing/synctest, net/http/httptest, gomock or testify (optional)

# Idioms and safe patterns
- Return `error` as the last result
- Use `errors.Is` and `errors.As` for wrapping checks
- Use `fmt.Errorf("...: %w", err)` not `%v` for wrapping
- Write small functions; each returns a single responsibility
- Use interfaces for boundaries; keep them narrow
- Accept interfaces, return structs mostly
- Avoid global mutable state
- Prefer value semantics when possible; use pointers only when mutation required
- Do not defer error handlers inside loops; use named helper closures carefully

# Concurrency patterns
- Do not start goroutines without a cancellation strategy
- Use `errgroup.Group` under `context`:
  ```go
  g, ctx := errgroup.WithContext(ctx)
  g.Go(func() error { ... })
  if err := g.Wait(); err != nil { return err }
  ```
- Worker pools use buffered channels for semaphore:
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
- Prefer channels for handoff, mutexes for shared state
- Avoid time.Ticker when context.WithTimeout can express the same contract
- Recover from panics only at goroutine boundaries if needed

# HTTP and servers
- Use `net/http` stdlib for most servers
- Use `http.Handler`, `http.ServeMux`, or `chi`/`gin` only if stdlib is insufficient
- Always set `ReadTimeout`, `WriteTimeout`, `IdleTimeout`
- Use structured logging with `log/slog`
- Use `http.Error` for failures; keep response body concise
- For clients: set timeouts, reuse transport, use `defer resp.Body.Close()`

# Working with JSON and data
- Define struct tags explicitly when serializing
- Use anonymous structs for small payloads
- Prefer `json.Decoder` for streams instead of `json.Unmarshal`
- Use `omitempty` and `string` tags intentionally
- Validate date and enum-behaving fields explicitly after unmarshal

# Files and paths
- Use `filepath.Join`, never bare `/` in paths for portability
- Use temporary dirs with `os.MkdirTemp` and clean up with `defer`
- For huge files, use `os.Open` and `io.Copy`/`bufio.Scanner`
- Close files in the same function where they are opened

# Context, timeouts, and cancellation
- Pass `context.Context` as the first argument in APIs
- `context.Background()` only in `main()` and tests setup
- `context.TODO()` is acceptable only as temporary placeholder
- Never store context inside a struct; pass it through the call chain
- Use `context.WithoutCancel` when spawning detached work
- Respect deadlines and avoid leaking goroutines

# Testing and benchmarks
- Table-driven tests:
  - use `tests` slice with cases
  - exercise function and compare with `reflect.DeepEqual` or `cmp.Diff`
- Subtests with `t.Run`
- `t.Parallel()` when tests are independent
- Benchmark with `func BenchmarkX(b *testing.B)`
- Use `httptest` for HTTP tests
- For fuzz: `func FuzzX(f *testing.F)`
- Golden files: store expected outputs under `testdata/`

# Tools
- `go test ./...`
- `go vet ./...`
- `staticcheck ./...`
- `golint` deprecated in favor of `staticcheck`
- Use `delve` for debugging, `pprof` for profiling
- Use `go mod tidy` after dependency changes
- Use `go generate` with `//go:generate` for codegen

# Safe editing and running rules
- Read stdlib docs before copying StackOverflow into code
- Run `go vet` after edits
- Run `go test` after logic changes
- Do not run tests that depend on network unless isolated
- Validate `go.sum` after touching modules
- Use `context` to bound I/O operations
- Keep `main.go` thin; move logic to internal packages
- Use `errors.Is` and `errors.As` over panic for handlable problems

# Common pitfalls
- Forgetting to close `resp.Body`
- Using `time.Now()` inside loops and tests
- Mutating receiver pointer when value receiver is intended
- Copying sync types by value
- Leaking goroutines on canceled context
- Returning `nil` error and non-nil value
- Overusing global vars or package-level state
- Mishandling `omitempty` for zero-valued required fields
- Assuming map iteration order
- Blocking inside `init` or `Load` paths
