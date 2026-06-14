# Common Mistakes

Beginner:
- omitting `return`
- not checking errors
- nil dereference
- using goroutines without cancellation
- misindented braces

Intermediate:
- wrapping errors with `%v` instead of `%w`
- forgetting `defer resp.Body.Close()`
- overusing types and interfaces
- missing `go vet` and `staticcheck`
- misusing `init()`
