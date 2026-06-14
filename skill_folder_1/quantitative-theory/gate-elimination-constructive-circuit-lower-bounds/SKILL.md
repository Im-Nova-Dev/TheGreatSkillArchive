---
name: gate-elimination-constructive-circuit-lower-bounds
title: Convergent Gate Elimination and Constructive Circuit Lower Bounds
description: >
  Teach gate elimination as the only known method for proving lower bounds on explicit functions
  against unrestricted Boolean circuits, and the 2026 convergent term-graph-rewriting formalization
  (arXiv:2602.17942 by Carmosino, Dang, Jackman). Covers classical Schnorr XOR lower bound,
  constructive vs non-constructive separations, refuter algorithms, convergence/confluence in
  simplification systems, and why DeMorgan/{∧,∨,⊕} admit convergent systems but U2/B2 do not.
  Use when studying circuit complexity, Boolean function lower bounds, term rewriting, or complexity-theoretic proof techniques.
---

# Gate Elimination and Constructive Circuit Lower Bounds

## 1. Why gate elimination matters
- It is the **only known method** for proving lower bounds on *explicit* functions against *unrestricted* Boolean circuits.
- Classic results it has produced:
  - Razborov (1985): superpolynomial monotone lower bounds for clique / perfect matching.
  - Iwama–Morizumi: 5n − o(n) DeMorgan lower bound for an explicit function.
  - Li–Yang (STOC 2022): 3.1n − o(n) for full basis B2.
- Historical barrier: lower bounds from gate elimination have been **non-constructive** and heavily case-based, making automation and verification difficult.

## 2. Classical lower bound via gate elimination: Schnorr’s XOR result
**Theorem (Schnorr, 1974).** The n-bit XOR function requires at least `3(n−1)` binary gates over the DeMorgan basis {∧, ∨, ¬}.

**Proof sketch.**
1. Start from any DeMorgan circuit computing XORn.
2. Repeatedly apply local replacements that *preserve semantics* but *reduce circuit size*:
   - absorb constants, eliminate double negations, fuse identical subtrees, use distributivity / absorption.
3. Count the number of elimination opportunities: an n-bit parity forces at least 3 "payments" per input variable, yielding the 3(n−1) term.
4. Stop when you reach a normal form with fewer than 3(n−1) gates → contradiction.

This is the archetype of gate elimination: every elimination step removes at least one gate while preserving the computed function.

## 3. Convergent term and term-graph rewriting systems
Core idea: formalize the informal simplifications above as a **rewrite system** that is:
- **Terminating**: every chain of rewrites is finite.
- **Confluent**: any two rewrite sequences from the same circuit can be continued to the same normal form.

### Boolean identities used
Key identities capturing simplification power (no commutativity rules, which destroy confluence):
- `0 ∨ g → g`, `1 ∧ g → g`, `¬¬g → g`
- `g ∧ ¬g → 0`, `g ∨ ¬g → 1`
- `g ∧ 0 → 0`, `g ∨ 1 → 1`

### Bases with convergent systems
- **DeMorgan** {∧, ∨, ¬}
- **{∧, ∨, ⊕}** (XOR basis)

### Bases without
- **U2** (NAND/NOR) and **B2** (all 16 binary gates) do **not** admit convergent simplification.
  Reason: superfluous negation gates force "push-up/push-down" rewrites that create non-isomorphic final circuits on different simplification paths.
  Consequence: proof automation for these bases requires explicit dependence on simplification order, breaking the clean normal-form reasoning.

## 4. From rewriting to constructive lower bounds
A lower bound `f ∉ C` of size s(n) has logical form:

∀ circuits C of size < s(n), ∃ x with C(x) ≠ f(x).

Non-constructive proofs do not give an efficient way to find x.

**Constructive lower bound:** there is an efficient **refuter** algorithm that, given any too-small circuit C, outputs a counterexample input x on which C errs.

**Why constructivity matters.** Chen, Jin, Santhanam, Williams (FOCS 2021) showed that most conjectured complexity separations (e.g., P ≠ NP, BPP ≠ NEXP) require constructive proofs. Non-constructive arguments are insufficient for major complexity-class separations.

### First constructive gate-elimination lower bound
Using the convergent rewriting system, Carmosino et al. gave a constructive refuter for XORn:

Refuter for XORn:
1. Input: a DeMorgan circuit C with < 3(n−1) gates claiming to compute XORn.
2. Run the convergent simplification system to normal form N.
3. Because no equivalent normal form exists below the gate threshold, step 2 must *detect* the deficiency (e.g., via a canonical normal-form signature).
4. Return an input that distinguishes N from XORn; lift back to distinguish C from XORn.

Result: **first known constructive lower bound proved via gate elimination**.

## 5. Teaching exercises

### Exercise 1. Normal forms
Using the rewrite rules `¬¬g → g` and `g ∨ 1 → 1`, reduce the circuit `¬(¬x1 ∨ 1)` to normal form. Show two different rewrite orders give the same final result.

### Exercise 2. Gate elimination for AND
Prove by hand that ANDn requires at least n−1 AND/OR/NOT gates. Hint: treat each input variable as a "resource" that must be introduced once, and show no gate can introduce two new useful variables simultaneously.

### Exercise 3. Convergence intuition
Give a circuit over DeMorgan that can be rewritten in two different ways to different subcircuits. Explain why convergence guarantees these can be further rewritten to an isomorphic final form.

### Exercise 4. Constructivity translation
For the function MAJORITYn, sketch what a refuter might do for a small DeMorgan circuit that claims to compute majority. Which normal-form features would reveal that the circuit cannot implement majority?

## 6. Connections and further reading
- Gate elimination + lifting: Göös, Pitassi, Watson (2015) lifting theorem connects query complexity to communication and monotone circuit size.
- Monotone circuit lower bounds: see de Rezende et al., STACS 2025 survey on monotone complexity and recent supercritical trade-offs.
- Smoothed analysis: Spielman–Teng style analyses of the simplex method often rely on complementary structure related to KKT conditions, analogous in flavor to dual-vs-primal reasoning in circuit lower bounds.

## 7. Precise statement summary
- **Schnorr (1974):** XORn needs ≥ 3(n−1) binary DeMorgan gates.
- **Carmosino–Dang–Jackman (2026):** First constructive proof of this via convergent rewriting; convergent simplification exists for DeMorgan and {∧,∨,⊕}, but not for U2 or B2.
