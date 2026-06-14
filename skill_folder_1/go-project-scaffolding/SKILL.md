---
name: go-project-scaffolding
description: Scaffold Go projects using standard layout and module patterns. Use this skill to bootstrap CLI tools, libraries, HTTP services, tests, and multi-module workspaces.
tags:
  - golang
  - scaffolding
  - project-layout
---

# Go Project Scaffolding

## Purpose
Generate clean, idiomatic Go project structure and module setup for common project types. Use this skill to start new Go code with standard layout, build files, and test setup.

## Guiding Principles
- Use standard layout unless the project clearly deviates
- Keep main thin; move logic into internal or package logic
- Prefer modules; use workspaces for multi-module local development
- Include tests from the start
- Use absolute imports aligned with module path

## Project Types

### CLI Tool
Structure:
```
cmd/<name>/main.go
internal/app/<name>/service.go
internal/pkg/<name>/...
go.mod
README.md
```
Steps:
- `go mod init github.com/<user>/<name>`
- Create `cmd/<name>/main.go`
- Move business logic into `internal/app/...`
- Use `pflag` or `cobra` only if needed

### HTTP Service
Structure:
```
cmd/server/main.go
internal/api/<name>/handler.go
internal/pkg/<name>/...
go.mod
README.md
```
Steps:
- Use `net/http` stdlib unless another framework is justified
- Add `ReadTimeout`, `WriteTimeout`, `IdleTimeout`
- Use `log/slog` for structured logging
- Add `internal/api/...` for handlers and routing

### Library
Structure:
```
<name>/<name>.go
<name>/<name>_test.go
go.mod
README.md
```
Steps:
- `go mod init github.com/<user>/<name>`
- Package name matches directory name
- Export only stable API
- Include examples in tests/documentation

### Multi-Module Workspace
Structure:
```
go.work
service-a/go.mod
service-a/...
service-b/go.mod
service-b/...
shared/go.mod
shared/...
```
Steps:
- `go work init` or add modules
- Use workspace for local edits across modules
- Avoid `replace` directives inside workspace modules

## Boilerplate Files
- `go.mod` with module path and Go version
- `README.md` with install, run, and test commands
- `.gitignore` for build artifacts and IDE files
- `Makefile` or `Taskfile.yml` with common targets: `build`, `test`, `lint`

## Quality Gates
- `go vet ./...`
- `staticcheck ./...`
- `go test ./...`
- Prefer CI workflow that runs on every PR

## Naming Rules
- Module path: lowercase, no spaces
- Package name: lowercase single word
- Internal packages stay private
- Avoid underscores in package names

## Example: Quickstart Template
```bash
mkdir -p myapp/cmd/myapp
cd myapp
go mod init github.com/<user>/myapp
cat > cmd/myapp/main.go <<'EOF'
package main

import (
    "fmt"
    "log"
    "myapp/internal/app"
)

func main() {
    if err := app.Run(); err != nil {
        log.Fatal(err)
    }
    fmt.Println("ok")
}
EOF
mkdir -p internal/app
cat > internal/app/app.go <<'EOF'
package app

import "errors"

var ErrStart = errors.New("start error")

func Run() error {
    return ErrStart
}
EOF
```

## Verification
- Can build executable: `go build ./cmd/myapp`
- Can run tests: `go test ./...`
- Can lint: `go vet ./...`
- Imports are absolute and consistent
