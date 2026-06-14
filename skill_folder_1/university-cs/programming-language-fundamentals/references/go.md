# Go

Teaching priorities: concurrency model, error handling style, modules, then standard library.

- Memory: GC-managed; no manual free, but avoid pointer proliferation.
- Error model: explicit `error` return value, no exceptions; wrap with `fmt.Errorf("...: %w", err)`.
- Concurrency: goroutines and channels are cheap; use `select` for multiplexing; prefer channels when ownership is shared.
- Toolchain: module-aware (`go.mod`), built-in `go test -race`, `go vet`, fast builds.
- Idioms: small interfaces, returning concrete types when possible, `defer` for cleanup.