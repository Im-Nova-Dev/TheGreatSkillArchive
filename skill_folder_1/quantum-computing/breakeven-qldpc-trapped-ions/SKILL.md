---
name: breakeven-qldpc-trapped-ions
description: Teach the first breakeven demonstration of quantum low-density parity-check (qLDPC) codes on trapped ions — 4 logical qubits in 18 physical qubits, 9× error rate improvement, OMG architecture for mid-circuit measurement without ion transport.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [quantum-computing, qldpc, trapped-ions, quantum-error-correction, fault-tolerance, breakeven]
    related_skills: [quantum-computing-fundamentals, surface-code-error-correction]
---

# Breakeven qLDPC Codes on Trapped Ions

## Overview

This skill teaches the breakthrough result from arXiv:2606.06455 (June 2026): the first demonstration of **breakeven quantum low-density parity-check (qLDPC) codes** on a trapped-ion quantum computer. The experiment achieved 4 logical qubits encoded in 18 physical qubits ([[18,4,4]] code) with a 9× improvement in logical error rate over prior superconducting demonstrations, and — critically — reached the **breakeven point** where logical qubit lifetimes equal or exceed physical qubit lifetimes.

The work also introduces the **OMG (Optical-Metastable-Ground) architecture** for mid-circuit measurement and reset without ion transport or dedicated coolant ions, eliminating two major overheads in trapped-ion systems.

## When to Use

- Teaching the mechanics and significance of qLDPC codes vs. surface codes
- Explaining why trapped ions have a connectivity advantage for high-rate codes
- Understanding the breakeven milestone in quantum error correction
- Learning the OMG architecture for mid-circuit operations
- Comparing trapped-ion vs. superconducting approaches to fault-tolerant quantum computing

## Core Concepts

### 1. qLDPC Codes — What and Why

**Low-density parity-check (LDPC)** codes are classical error-correcting codes where each parity check involves few bits, and each bit participates in few checks. The **quantum** version (qLDPC) generalizes this to stabilizer codes with sparse parity-check matrices.

| Property | Surface Code | qLDPC Codes |
|----------|-------------|-------------|
| Connectivity | Planar, nearest-neighbor | **Non-local, high-degree** |
| Encoding rate (k/n) | ~1/d² (very low) | **10-25% (high)** |
| Physical qubits per logical | ~2d² | ~10-20 for d=4 |
| Hardware challenge | Easy connectivity | **Requires long-range couplers** |
| Decoding complexity | Polynomial (MWPM) | More complex (belief propagation + ...) |

**Key insight:** High-rate qLDPC codes are *theoretically* superior (less overhead) but *practically* require all-to-all or long-range connectivity — which superconducting qubits lack naturally.

### 2. Trapped-Ion Connectivity Advantage

Trapped ions interact via **collective motional modes** (phonons) of the ion chain. Any pair of ions can be entangled by addressing them with lasers tuned to a shared motional mode.

- **All-to-all connectivity** is native — no hardware reconfiguration needed
- **No long-range couplers** required — the phonon bus *is* the long-range interaction
- This single device demonstrated **9 distinct QEC codes** across 3 families (qLDPC, topological, concatenated) with **zero hardware changes**

### 3. The [[18,4,4]] qLDPC Code — Breakeven Demonstration

**Code parameters:**
- n = 18 physical qubits
- k = 4 logical qubits  
- d = 4 (distance: corrects up to 1 error, detects 2)
- Rate = k/n = 4/18 ≈ **22.2%**

**Breakeven definition:** Logical qubit lifetime ≥ physical qubit lifetime.

**Result:** "Some instances achieving qubit lifetimes comparable to or slightly exceeding that of our trapped-ion qubits."

**9× improvement** over the previous best superconducting qLDPC demonstration (Google, Nature 2023).

### 4. OMG Architecture — Optical-Metastable-Ground

Traditional trapped-ion mid-circuit measurement requires:
1. **Ion transport** (shuttling) to physically separate measurement zone from computation zone — slow (ms), adds decoherence
2. **Coolant ions** (different species) for sympathetic cooling during reconfiguration — consumes ~30-50% of ion budget

**OMG innovation:** Uses **metastable electronic states** as a "shelving" mechanism.

```
Ground state (computation) ↔ Metastable state (storage) ↔ Optical state (measurement)
```

- **Addressable measurement:** Drive specific ions to optical state → fluoresce → detect photons → other ions undisturbed (in metastable/ground)
- **Mid-circuit reset:** Optical pump measured ions back to ground state
- **No ion transport** — all ions stay in place
- **No coolant ions** — sympathetic cooling unnecessary

### 5. Syndrome Extraction for qLDPC

qLDPC codes have **weight-w parity checks** (each check involves w qubits). Syndrome extraction requires measuring multi-qubit stabilizers.

Key circuit elements:
- **Ancilla qubits** for each stabilizer generator
- **Multi-qubit gates** (or sequences of 2-qubit gates) to couple data to ancilla
- **Mid-circuit measurement** of ancillas → syndrome bits
- **Classical decoding** (belief propagation, tensor networks, etc.) → error estimate

The all-to-all connectivity makes the multi-qubit coupling natural — no SWAP networks needed.

## Reference Files

| File | When to Open | Why It Matters |
|------|-------------|----------------|
| `references/qldpc-vs-surface-code.md` | Deep-dive on overhead scaling | Quantifies when qLDPC wins |
| `references/omg-architecture-details.md` | Teaching OMG metastable states | Energy level diagrams, timing |
| `references/breakeven-criterion.md` | Understanding the milestone | Formal definition, implications |
| `references/trapped-ion-phonon-bus.md` | Native connectivity mechanism | Mølmer-Sørenson gates, motional modes |

## Common Pitfalls

1. **Confusing qLDPC with surface code:** They are both stabilizer codes, but qLDPC has *non-local* checks and *high rate*. Surface code is a *topological* code with *local* checks and *low rate*.

2. **Thinking breakeven means "error-free":** Breakeven means logical lifetime ≥ physical lifetime. Errors still occur — the code *extends* lifetime, doesn't eliminate errors. Below threshold, concatenation gives exponential suppression.

3. **Assuming all trapped ions have OMG:** This is a *specific architecture* demonstrated in this work. Most trapped-ion systems still use transport + coolant ions.

4. **Overlooking the decoding challenge:** qLDPC decoding is harder than surface code (MWPM). Real-time decoding latency matters for fault tolerance.

5. **Ignoring the 9-code demonstration:** The [[18,4,4]] result is the highlight, but showing 9 codes on *fixed hardware* proves the architectural flexibility — a systems-level win.

## Verification Checklist

- [ ] Can explain qLDPC parity-check matrix structure (H_x, H_z sparse)
- [ ] Can contrast surface code vs qLDPC overhead scaling (k/n vs distance)
- [ ] Can explain why trapped ions have native all-to-all connectivity (phonon bus)
- [ ] Can define breakeven: T₁_logical ≥ T₁_physical
- [ ] Can describe OMG energy level diagram (ground, metastable, optical)
- [ ] Can explain why ion transport + coolant ions are overheads
- [ ] Can describe syndrome extraction circuit for weight-w stabilizer
- [ ] Knows the key numbers: [[18,4,4]], 9× improvement, 22.2% rate

## Intel Source

Primary intel: `/home/nova/.hermes/intel/science/2026-06-06-qldpc-breakeven-trapped-ions-breakthrough.md`

Paper: arXiv:2606.06455 — "Breakeven demonstration of quantum low-density parity-check codes" (Tham et al., June 2026)

---

*Skill created: 2026-06-06 | Part of the Science Intelligence cron job tracking hard-science breakthroughs*