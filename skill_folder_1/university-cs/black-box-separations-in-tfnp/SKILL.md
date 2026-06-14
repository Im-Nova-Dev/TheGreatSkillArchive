---
name: black-box-separations-in-tfnp
description: |
  Teach randomized black-box separations in TFNP, covering TFNP subclasses
  (PPAD, PLS, PPP, CLS, EOPL, SOPL, NETS, etc.), the oracle separation
  framework, Merkle-tree and random-oracle techniques, and the implications
  of recent separations (e.g., Kiselev 2026) for structural complexity theory.
  Uses teaching exercises connecting to search-to-decision reductions.
---

# Black-Box Separations in TFNP

## What is TFNP?

- **TFNP** = Total Function NP: search problems where every instance has a
  provable witness, but no NP verification oracle is given directly.
- Represents structural richness beyond standard NP: there is always a
  solution, but finding it can require stronger tools than NP search.

## Important Subclasses

- **PLS** (Polynomial Local Search): provably terminates by descent in a
  polynomial neighborhood.
- **PPAD** (Polynomial Parity Argument on Directed graphs): existence proof
  from Sperner / handshake lemma / parity.
- **PPP** (Polynomial Pigeonhole Principle): from pigeonhole/noninjectivity.
- **CLS** = intersection of PPAD ∩ PLS; captures continuous local search +
  parity-constrained search.
- **EOPL**, **SOPL**, **NETS**: finer-grained subclasses isolating
  equilibrium-like vs. shortest-path-like vs. network-flow structures.

## Black-Box Separations

- **Goal**: prove there is no polynomial-time *black-box* algorithm for A
  given an oracle for B.
- **Oracle separation** ≠ non-existence of any algorithm; only rules out
  generic, representation-independent procedures.
- Central technique: construct oracles under which any proposed
  black-box solver for a class fails with noticeable probability; then
  average-case or randomized lower bounds follow.

## Merkle-Tree and Random-Oracle Technique

- Build a **Merkle tree** or layered hash function so that any small number
  of oracle queries cannot simultaneously satisfy both:
  - the structure encoding a counterexample,
  - the hash consistency checks.
- Used to separate randomized algorithms from deterministic ones for the
  *same* TFNP subclass, or to separate two subclasses.

## Recent Result To Study

- Fedor Kiselev, *Randomized separations in black-box TFNP*, arXiv:2606.04697
  (2026).
- Themes: prove randomized vs. deterministic black-box separations within
  TFNP subclasses; usually quantified through query complexity lower bounds.

## Pedagogical Exercises

1. Show that 3-SAT is not a natural complete problem for TFNP overall
   because TFNP is total. Contrast with NP-completeness.
2. Given a directed graph of degree 2, use the handshake lemma to show
   existence of an odd-degree vertex (PPAD-witness).
3. Design a Merkle-tree oracle that forces any k-query randomized black-box
   algorithm to succeed with probability ≤ 1/2^k.
4. Sketch why CLS ⊆ PPAD and CLS ⊆ PLS, and discuss why the inclusion
   proofs are *white-box* and do not settle black-box equality.
5. Convert a search problem whose witness is an *index* into a TFNP
   search problem and identify its minimal subclass.

## Connections

- Lower bounds for TFNP connect to **meta-complexity**, **oracle
  separations in BPP vs P**, and **proof complexity**.
- Embeds into **economics** via equilibrium computation (PPAD-complete
  problems arise from Nash equilibrium).
