---
name: go-software-design
description: Teach software design principles in Go including SOLID, clean architecture, package design, and modular patterns. Use this skill to design maintainable and testable Go systems.
tags:
  - golang
  - architecture
  - design-principles
  - teaching
---

# Go Software Design Principles

## Purpose
Teach applying software design principles in Go for maintainable, testable, and scalable systems. Use this skill when designing packages, structuring applications, or reviewing architecture.

## Core Principles

## Go and SOLID Principles

### Single Responsibility
- One package or type should have one reason to change
- Separation of concerns in Go: handlers, services, repositories

### Open for Extension, Closed for Modification
- Use interfaces to define extension points
- Avoid package internals; design abstractions

### Liskov Substitution
- Subtypes must be substitutable for base types
- Behavior preservation in interface implementations

### Interface Segregation
- Prefer small interfaces
- The Zen of Go: accept interfaces, return structs

### Dependency Inversion
- Higher-level modules should not depend on lower-level
- Depend on abstractions via interfaces

## Package Design Rules

### Naming
- Short, clear names
- Single responsibility package
- Avoid utility packages like `common` or `helpers`

### Visibility
- Unexported types by default
- Export only stable API
- `internal/` for private application code

### Dependencies
- Low-level packages should not import high-level
- Accept interfaces at boundaries
- Return concrete types from constructors

## Layered Architecture
Typical layers:
- `cmd/` - entrypoints
- `internal/api/` - HTTP handlers
- `internal/service/` - business logic
- `internal/repository/` - data access
- `pkg/` - public library code
- `configs/` - configuration structs

Dependency flow: handlers -> service -> repository -> driver

## Clean Architecture in Go

### Entities
- Core business logic
- No external dependencies
- Pure domain objects

### Use Cases
- Application-specific business rules
- Orchestrate data flow
- Define interfaces for external dependencies

### Interface Adapters
- Convert data between external and internal formats
- Controllers, presenters, gateways

### Frameworks and Drivers
- External tools: databases, web, UI
- Lowest-level detail layer

## Common Design Patterns

### Repository Pattern
```go
type UserRepository interface {
    Find(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, u *User) error
}
```

### Service Pattern
```go
type UserService struct {
    users  UserRepository
    mailer Mailer
}
```

### Middleware Pattern
```go
func Logging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

## Common Design Mistakes
- Anemic domain models
- God objects handling everything
- Circular package dependencies
- Overusing interfaces for no benefit
- Leaking framework details into business logic

## Teaching Sequence
1. Explain why design matters
2. Show bad example with obvious problems
3. Introduce principle
4. Refactor to good example
5. Discuss tradeoffs
6. Practice design exercises

## Design Exercises
- Design a URL shortener service
- Design a notification system
- Design a caching layer
- Refactor legacy monolith

## Assessment Checklist
- Can explain SOLID in Go idioms
- Can design package structure for new project
- Can identify circular dependencies
- Can use interfaces to decouple layers
- Can avoid premature abstraction
