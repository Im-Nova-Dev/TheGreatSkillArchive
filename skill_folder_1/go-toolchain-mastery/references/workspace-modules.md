# Workspace and Modules

- `go.work` for multi-module repos
- `replace` only for local development
- Avoid module proxy bypasses in production
- Build tags: `//go:build linux`, `//go:build cgo`
- Cross-compile with `GOOS`, `GOARCH`, `CGO_ENABLED=0`
