---
name: go-generics-teaching
description: Teach Go generics with progressive exercises and common pitfalls. Covers type parameters, constraints, type inference, and real-world usage.
tags:
  - golang
  - teaching
  - generics
---

# Go Generics Teaching

## Purpose
Teach Go generics systematically, from basics to constraints and real-world usage. Use this skill when explaining type parameters, constraints, or helping learners adopt generics idiomatically.

## Level Progression

### Beginner
Objective: Understand why generics exist and read basic syntax.
- Concept: eliminate duplicated type-specific code
- Vocabulary: type parameter, type argument, constraint, instantiation, type set
- Syntax: `[T any]`, `func Foo[T any](x T) T`

### Intermediate
Objective: Write constraints and design generic functions/types.
- Union types: `int | float64`
- Type sets with `~`: `~int` means int and any type with underlying int
- `comparable` for map keys and equality checks
- Inference: omit type args when possible

### Advanced
Objective: Evaluate when generics help vs hurt.
- Use generics for collections, algorithms, and reusable utilities
- Avoid overgeneralizing one-off types
- Recognize when interfaces suffice

## Common Beginner Mistakes
- Overusing `any` instead of meaningful constraints
- Expecting runtime type assertions inside generic bodies
- Creating generic types with no behavior difference between instantiations
- Forgetting type args are compile-time only

## Common Intermediate Mistakes
- Misunderstanding `comparable` vs `any`
- Using type parameters where simple interfaces work
- Writing generic functions with impossible operations on all constraint members
- Ignoring inference rules and repeating explicit type args unnecessarily

## Teaching Templates
Concept: `<title>`
Live example: `<snippet>`
Exercise: `<task>`
Explanation: `<text>`
Common mistake: `<snippet + fix>`

## Exercises

### Verification
- Ask: does the generic actually generalize? If every instantiation behaves the same, prefer an interface.
- Prefer `comparable` for equality before `any` with runtime checks.
- Write one instantiation with each base type in the constraint’s type set.

### Exercise 1: Hello Generics
Write a generic `Print[T any](x T)` that prints any value.
```go
func Print[T any](x T) {
    fmt.Printf("%v\n", x)
}
```
Ask learner to predict behavior with int, string, and slice.

### Exercise 2: Constraints
Write a generic `Sum[T int64 | float64](nums []T) T` that sums a slice.
Discuss why `any` alone won't support `+`.

### Exercise 3: Type Sets with `comparable`
Write a generic `KeyExists[K comparable, V any](m map[K]V, k K) bool`.
Discuss why `K` must be comparable.

### Exercise 4: Type Inference
Given:
```go
func Index[T comparable](s []T, x T) int
```
Have learner call `Index` without explicit type args.
Then make it fail and explain why.

### Exercise 5: Generic Types
Design `Stack[T any]` with `Push`, `Pop`, and `Len`.
Discuss when to use pointer receiver for generic types.

### Exercise 6: Constraints in Practice
Discuss `constraints.Ordered`:
```go
type Ordered interface {
    Integer | Float | ~string
}
```
Have learner implement a generic `Min[T Ordered](x, y T) T`.
Explain why `~string` exists.

### Exercise 7: Method Set vs Type Set
Explain how method-based interfaces and type-set interfaces serve different roles for generics.
Show how `fmt.Stringer` works as a constraint.

## Evaluation Checklist
- Can explain difference between type parameter and regular parameter
- Can read and write generic functions
- Can create constraints with union types and `comparable`
- Can explain when type args can be omitted
- Can design a simple generic type
