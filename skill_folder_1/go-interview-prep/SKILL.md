---
name: go-interview-prep
description: Teach Go interview preparation covering algorithmic patterns, data structures, concurrency questions, and hands-on problem-solving strategies.
tags:
  - golang
  - interview
  - algorithms
  - teaching
---

# Go Interview Preparation

## Purpose
Prepare learners for Go-related technical interviews with structured problem-solving practice. Use this skill when practicing algorithms, data structures, Go-specific patterns, or behavioral prep.

## Teaching Rules
- Teach problem-solving process, not just answers
- Emphasize time/space complexity analysis
- Practice both writing and explaining solutions
- Build from standard patterns, not memorization
- Use real LeetCode/HackerRank-style problems with Go context

## Core Problem-Solving Framework
1. Clarify requirements and examples
2. State brute-force approach first
3. Optimize with standard patterns
4. Write idiomatic Go solution
5. Handle edge cases explicitly
6. Analyze complexity
7. Test the code verbally

## Essential Pattern Catalog
Teach these patterns in order:
- Two pointers
- Sliding window
- Depth-first search
- Breadth-first search
- Backtracking
- Dynamic programming
- Greedy algorithms
- Hash maps for lookup
- Union find
- Topological sort

## Go-Specific Interview Topics

### Language Mechanics
- Goroutines and channels
- Maps and slices internals
- Pointers vs values
- Interface implementation
- Method sets and receivers
- Error handling idiom
- nil vs empty values
- Mutex and sync primitives
- iota and constants
- JSON marshaling/unmarshaling

### Standard Library
- `sort` interface
- `container` packages
- `net/http`
- `encoding/json`
- `sync` vs `sync/atomic`
- `context.Context`
- `time` handling

## Practice Exercises

### Two Pointers
Problem: Two Sum (sorted input)
Teach: pointer movement logic, while loop conditions

### Sliding Window
Problem: Longest substring without repeating characters
Teach: window boundaries, rune handling in Go

### Hash Map
Problem: Valid anagram
Teach: `map[rune]int`, range over string, equality check

### Trees
Problem: Binary tree level order traversal
Teach: slice as queue, struct definition, recursion vs queue

### Concurrency Design
Problem: Design a rate limiter
Teach: token bucket with goroutines and channels, context cancellation

## Code Review Rubric
Go-specific items to teach:
- Correct package declaration
- Proper error handling (`if err != nil`)
- Idiomatic naming (`MixedCaps`)
- Correct use of slices vs arrays
- Map initialization before use
- Defer for cleanup
- Avoid global mutable state

## Mock Interview Template
1. Problem statement and examples
2. Assumptions question
3. Brute-force solution
4. Optimization discussion
5. Coding phase
6. Complexity analysis
7. Test cases
8. Follow-up variations

## Common Interview Traps
- Forgetting Go method receiver semantics
- Wrong nil check on interfaces
- Map iteration order assumption
- Copying mutex by value
- Integer overflow in arithmetic
- Slicing bounds off-by-one
- Closing over loop variables in goroutines during concurrency questions

## Teaching Sequence
1. Pattern recognition: name the pattern
2. Pseudocode first
3. Translate to idiomatic Go
4. Complexity analysis
5. Refactor for clarity
6. Practice until pattern is automatic
