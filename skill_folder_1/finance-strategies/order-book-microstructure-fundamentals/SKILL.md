# Order Book Microstructure Fundamentals

Practical toolkit for teaching and implementing CLOB-style execution: OBI, VAMP, quote stuffing, and sequencing.

## Topics
- Filtered OBI / OBI(T)
- Volume-weighted adjusted mid price (VAMP)
- Quote stuffing detection and layout cost
- Lamport logical clocks for deterministic ordering across restarts
- Execution micro-skills with order book resilience

## Sequencing Note
Use deterministic ordering (Lamport logical clocks) to reconstruct audit trails and dissipated order flow.
