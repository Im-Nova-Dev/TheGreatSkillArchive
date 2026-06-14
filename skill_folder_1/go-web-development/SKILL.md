---
name: go-web-development
description: Teach Go web development including HTTP servers, middleware, routing, REST APIs, WebSockets, and production-ready web application patterns.
tags:
  - golang
  - web
  - http
  - api
---

# Go Web Development

## Purpose
Teach Go web development from basic HTTP handlers to production-ready APIs. Use this skill when building web services, explaining middleware, or discussing web architecture in Go.

## Core Philosophy
- Use stdlib `net/http` as the foundation
- Middleware should be composable and focused
- Separation of concerns: routing, handlers, business logic, data
- Graceful shutdown is mandatory
- Security is not optional

## Standard Library HTTP
- `http.Handler`, `http.HandlerFunc`
- `http.ServeMux` for routing
- `http.Server` for configuration and lifecycle
- `http.Request` and `http.ResponseWriter`
- Request parsing, headers, query parameters, body limits

## Routing
- Simple stdlib mux with `http.HandleFunc` or `http.ServeMux`
- Third-party routers: `chi`, `gorilla/mux`, `gin`
- Path parameters, wildcards, middleware chaining
- Grouping routes for versioning and modules

## Middleware Patterns
- Logging middleware
- Recovery from panics
- Authentication and authorization
- Rate limiting with token bucket or sliding window
- CORS handling
- Compression: gzip middleware
- Request validation and sanitization

Example:
```go
func Logging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

## REST API Design
- Resource-based URLs
- HTTP methods semantically correct
- Status codes: 200, 201, 204, 400, 401, 403, 404, 409, 500
- JSON request/response with `json.Decoder` and `json.Encoder`
- Content negotiation
- Pagination and filtering

## Request Validation
- Validate before processing
- Reject malformed input early
- Use struct tags and custom validators
- Bind query parameters, path params, and JSON body

## WebSockets
- `gorilla/websocket` for WebSocket support
- Upgrader pattern
- Handling concurrent connections
- Heartbeat and ping/pong
- Graceful disconnect handling

## Graceful Shutdown
- Listen for SIGINT and SIGTERM
- Close server with timeout
- Drain in-flight requests
- Cleanup resources

## TLS and HTTPS
- Automatic HTTPS with `autocert` for Let's Encrypt
- Manual certificate configuration
- TLS best practices: strong ciphers, HSTS

## Common Middleware Examples
```go
// CORS
func CORS(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        // ...
        next.ServeHTTP(w, r)
    })
}

// Rate limiter with token bucket
func RateLimit(next http.Handler) http.Handler {
    // implementation using sync.Mutex or atomic
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !allow() {
            http.Error(w, "rate limit exceeded", http.StatusTooManyRequests)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

## Testing Web Applications
- `httptest.NewRecorder` and `httptest.NewRequest`
- Table-driven tests for endpoints
- Integration tests with test server
- Mock external dependencies

## Common Mistakes
- Forgetting to set timeouts on server
- Reading unlimited request bodies
- Not closing response bodies from clients
- Using global state for handlers
- Blocking in middleware

## Teaching Sequence
1. Simple handler with stdlib
2. Add middleware decorator pattern
3. Build REST endpoints
4. Add validation and error handling
5. Add authentication
6. Add graceful shutdown
7. Discuss deployment and TLS

## Assessment Checklist
- Can build HTTP server with stdlib
- Can implement middleware pattern
- Can design REST API endpoints
- Can add graceful shutdown
- Can write integration tests for handlers
- Understands security basics: input validation, auth, rate limiting
