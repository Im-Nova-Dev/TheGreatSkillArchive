---
name: go-databases-and-orm
description: Teach database access in Go using database/sql, connection pools, transactions, migrations, and ORM tradeoffs
tags:
  - golang
  - database
  - sql
  - orm
---

# Go Databases and ORM

## Purpose
Teach database interaction in Go covering stdlib, drivers, connection management, transactions, and ORM choices. Use this skill when accessing SQL/NoSQL data stores or teaching persistence layers.

## Core Principles
- Prefer `database/sql` for explicit control
- Connections are finite resources; use pools and limits
- Transactions must be bounded by scope and time
- Handle errors before checking rows
- Use parameterized queries everywhere

## database/sql
- `sql.Open`, `DB.Ping`, connection state vs actual connection
- Connection pooling configuration
- `QueryRow`, `Query`, `Exec`
- `sql.ErrNoRows` checking pattern

## Prepared Statements
- `db.Prepare` for repeated queries
- Prepared statements via placeholders
- Close statements when done

## Transactions
- `db.Begin`, `tx.Commit`, `tx.Rollback`
- Use named return with defer rollback
- Nested transactions via savepoints if needed

## Drivers
- PostgreSQL: `lib/pq`, `pgx`
- MySQL: `go-sql-driver/mysql`
- SQLite: `modernc.org/sqlite`
- Use connection strings with env config

## ORM Options
- `gorm.io/gorm` when ORM is justified
- Compare ORM vs raw SQL tradeoffs
- Avoid magic if team doesn't know the code path

## Test Data
- `sqlmock` for unit testing
- Testcontainers for integration tests
- Migrations with `golang-migrate`

## Common Mistakes
- Treating `sql.Open` as a live connection check
- Missing `defer rows.Close()`
- SQL injection via string concatenation
- Not handling `tx.Rollback` errors
- Long-lived transactions blocking writers

## Teaching Sequence
1. `database/sql` basics
2. Prepared statements and queries
3. Connection pools
4. Transactions and rollbacks
5. Migrations
6. ORM overview and justification
7. Test data strategies

## Exercises
- Build repository pattern for `User`
- Add transaction for account transfer
- Write migration for new table
- Test repository with sqlmock
