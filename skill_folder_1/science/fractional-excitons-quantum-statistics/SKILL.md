---
name: fractional-excitons-quantum-statistics
description: "Teach fractional excitons — a new class of quantum particles with hybrid statistics beyond bosons/fermions/anyons, discovered in the fractional quantum Hall effect (Nature 2025)."
version: 1.0.0
category: science
---

# Fractional Excitons & Quantum Statistics

## Overview

First-principles teaching pack for **fractional excitons** — neutral composite particles formed by pairing fractionally charged quasiparticles in the fractional quantum Hall regime. This 2025 breakthrough (Brown University, *Nature*) reveals a new class of quantum statistics that defies the standard boson/fermion/anyon trichotomy, opening a new dimension for quantum matter exploration and topological quantum computing.

**Primary Source**: Zhang, N.J., Nguyen, R., Batra, N. et al. *Excitons in the fractional quantum Hall effect*. **Nature 637**, 334–339 (2025). DOI: 10.1038/s41586-024-08274-3

## When To Use

- Teaching quantum statistics beyond the standard three classes
- Explaining the fractional quantum Hall effect (FQHE) and its new excitonic physics
- Introducing topological quantum matter and hybrid quantum statistics
- Connecting condensed matter breakthroughs to quantum computing applications

## Core Topics

### 1. Quantum Statistics Refresher
- **Bosons**: symmetric wavefunctions, no Pauli exclusion, unlimited state sharing (photons, phonons, Cooper pairs)
- **Fermions**: antisymmetric wavefunctions, strict Pauli exclusion (electrons, protons, quarks)
- **Anyons**: 2D-only intermediate braiding statistics (FQHE quasiparticles with charge e/3, e/5...)
- **Why 2D matters**: particle exchange = path winding; topological protection of statistics

### 2. What Are Fractional Excitons?
| Property | Conventional Exciton | Fractional Exciton |
|----------|---------------------|-------------------|
| Composition | electron + hole (integer charges) | fractional quasiparticle + fractional quasihole |
| Net charge | 0 | 0 |
| Constituent charges | -e, +e | -e/3, +e/3 (or e/5, e/7...) |
| Quantum statistics | Bose-Einstein (boson-like) | **Hybrid — neither boson, fermion, nor anyon** |
| Stability regime | Weak/no magnetic field, integer QHE | **Strong B-field, fractional QHE regime** |

### 3. The Experimental Platform
```
┌─────────────────────────────────────────────┐
│  Top gate                                   │
│  ────────────────────────────────────────   │
│  Monolayer graphene (hole Landau level)    │
│  ────────────────────────────────────────   │
│  Hexagonal boron nitride (hBN, ~5 nm)      │
│  ────────────────────────────────────────   │
│  Monolayer graphene (electron Landau level)│
│  ────────────────────────────────────────   │
│  hBN substrate / SiO₂ back gate            │
└─────────────────────────────────────────────┘
```
- **Magnetic field**: >20 T (millions × Earth's field)
- **Temperature**: <100 mK (millikelvin)
- **Control**: dual gates independently tune filling factors νₑ, νₕ
- **Detection**: photoluminescence spectroscopy + electrical transport

### 4. Key Experimental Signatures
1. **PL peaks at fractional filling** (ν = 1/3, 2/5, 3/7...) — excitons exist *inside* FQHE states
2. **Transport confirms FQHE** in both layers simultaneously
3. **Energy vs. filling factor** tracks predicted fractional quasiparticle gaps
4. **Linewidth/coherence** suggests non-trivial statistics

### 5. Why Hybrid Statistics?
- Fractional excitons are **bound pairs of anyons** (fractional charge = fractional statistics)
- Pairing two anyons with statistics θ₁, θ₂ gives total θ = θ₁ + θ₂ + ... (braiding phases add)
- But these are **neutral composite particles** — they don't "see" the Aharonov-Bohm phase like charged anyons
- Result: **statistics ≠ simple anyon sum** — unique behavior showing boson-like AND fermion-like tendencies
- Theoretical framework still developing (see ref-03-theory-framework.md)

### 6. Implications for Quantum Computing
- **Topological protection**: neutral particles immune to charge noise
- **Non-Abelian potential**: if statistics are non-Abelian → fault-tolerant qubits
- **New qubit platform**: fractional exciton condensates as quantum memories
- **Measurement**: interferometry of neutral particles (no Coulomb screening)

### 7. Open Questions (Active Research)
1. **Interactions**: fractional exciton-exciton interactions — attractive/repulsive?
2. **Condensation**: can they form Bose-Einstein-like condensates?
3. **Tunability**: continuous statistics control via gate voltage?
4. **Lifetime**: coherence times for quantum information processing?
5. **Generalization**: TMDs, twisted bilayer graphene, other 2D platforms?

## References

- `references/ref-01-fqhe-primer.md` — Fractional quantum Hall effect from first principles
- `references/ref-02-exciton-physics.md` — Exciton formation, binding, and spectroscopy
- `references/ref-03-theory-framework.md` — Theoretical models for fractional exciton statistics
- `references/ref-04-experimental-methods.md` — PL spectroscopy, transport, gating in 2D heterostructures
- `references/ref-05-quantum-computing-applications.md` — Topological qubits, interferometry, roadmaps

## Templates

- `templates/quantum-statistics-comparison.md` — Fill-in table for boson/fermion/anyon/fractional-exciton comparison
- `templates/fqhe-device-diagram.md` — LaTeX/TikZ template for graphene/hBN device cross-sections
- `templates/fractional-exciton-energy-diagram.md` — Band diagram template for exciton formation at fractional fillings

## Notes

- This skill teaches the *mechanism*, not just the result — focus on *why* fractional charges → fractional statistics → hybrid statistics
- Use the intel report at `/home/nova/.hermes/intel/science/2025-01-08-brown-fractional-excitons-breakthrough.md` for latest details
- Prerequisite: solid grasp of quantum Hall effect (integer + fractional) and basic exciton physics
- Best paired with: `science/quantum-error-correction-practical`, `physics/topological-quantum-computing-and-majorana-zero-modes`