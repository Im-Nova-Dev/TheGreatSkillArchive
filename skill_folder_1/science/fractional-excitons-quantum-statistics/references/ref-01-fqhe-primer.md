---
title: "Fractional Quantum Hall Effect — First-Principles Primer"
skill: fractional-excitons-quantum-statistics
---

# Fractional Quantum Hall Effect (FQHE) — From First Principles

## 1. The Classical Hall Effect (1879)
Place a current-carrying conductor in a perpendicular magnetic field **B**. Charges experience Lorentz force **F = q(v × B)**, accumulating on one side → transverse voltage **V_H**.
- Hall resistance: **R_H = V_H / I = B / (n e)** (n = carrier density)
- In classical regime: linear in B, proportional to 1/n

## 2. Integer Quantum Hall Effect (IQHE) — von Klitzing 1980
At **low T, high B, 2D electron gas** (2DEG): Hall resistance develops **exact plateaus** at quantized values.

**R_H = h / (ν e²)** where **ν = 1, 2, 3, 4...** (integer filling factor)

**Why?**
- In 2D + B-field, electron energies quantize into **Landau levels**: E_n = ħω_c (n + ½)
- Each Landau level has degeneracy **N_φ = B A / (h/e)** = number of flux quanta
- **Filling factor ν = N_e / N_φ** = electrons per flux quantum
- When ν = integer: all Landau levels completely filled or empty → **incompressible state**
- **Energy gap** to excitations = cyclotron energy ħω_c (or Zeeman for spin splitting)
- Edge states carry current; bulk is insulating → **exact quantization**

## 3. Fractional QHE — Tsui, Störmer, Gossard 1982
At **even higher B, lower T, cleaner samples**: new plateaus at **ν = 1/3, 2/5, 3/7, 2/3, 3/5...**

**This changed everything**: interactions *create* new states of matter.

### 3.1 Laughlin Wavefunction (ν = 1/m, odd m)
Ψ_1/m = ∏_{i<j} (z_i - z_j)^m exp(-∑|z_k|²/4ℓ_B²)
- **Jastrow factors** (z_i - z_j)^m → electrons avoid each other (correlation)
- m odd → antisymmetric (fermions)
- **Energy gap** from Coulomb interaction, not single-particle physics
- **Quasiparticles**: charge **±e/m** (e/3 for ν=1/3)

### 3.2 Jain's Composite Fermion Theory
Attach **2 flux quanta** to each electron → **composite fermions** (CFs)
- CFs see effective field: **B* = B - 2n h/e**
- CF filling factor: **ν* = ν / (1 - 2ν)**
- FQHE of electrons ⇔ IQHE of CFs
- Explains entire sequence: ν = p/(2p+1), ν = 1 - p/(2p+1), etc.

### 3.3 Moore-Read / Pfaffian States (ν = 5/2, 12/5...)
Paired states → **non-Abelian anyons**
- Quasiparticle exchange → unitary matrix (not just phase)
- Potential for **topological quantum computing**

## 4. Key Concepts for Fractional Excitons

### 4.1 Fractional Charge
- Quasiparticles carry **fraction of e** (e/3, e/5, e/7...)
- Measured via shot noise, tunneling, adiabatic transport
- **Charge = statistics** in 2D (spin-charge relation)

### 4.2 Anyon Statistics
- Exchange two identical particles in 2D: **wavefunction picks up phase e^{iθ}**
- Bosons: θ = 0 (any loop = no phase)
- Fermions: θ = π (odd permutation = -1)
- Anyons: **θ = fractional multiple of π** (e.g., π/3 for ν=1/3)
- **Braiding** = particle worldlines winding in (2+1)D spacetime

### 4.3 Incompressibility
- FQHE ground state: **unique, gapped, topologically ordered**
- Adding/removing one electron costs finite energy → **gap**
- Low-energy excitations = anyons (fractional charge, fractional statistics)

### 4.4 Edge-Bulk Correspondence
- Bulk topological order ↔ chiral edge modes
- Number of edge modes = number of quasiparticle types
- Thermal conductance quantized: **κ_xy = (π²k_B²T/3h) c** (c = central charge)

## 5. Band Diagrams: Landau Levels at ν = 1/3
```
Energy
  ↑
  |    ┌──────────────── LL 1 (empty)        ───
  |    │
  |    │    ← Cyclotron gap ħω_c
  |    │                                        Δ
  |    │                                       Δ
  |    │    ┌──────────────── LL 0  ◄─── 1/3 filled
  |    │    │  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
  |    │    │  e  e  e  ·  ·  ·  ·  ·  ·  ·  ← electron holes (quasiholes)
  |    │    └────────────────
  +----+----+----+----+----+----+----+----+----→ Position
       Spatial separation of electrons → correlations
```

## 6. Experimental Signatures of FQHE
| Technique | What It Measures | FQHE Signature |
|-----------|------------------|----------------|
| DC transport | R_xx, R_xy | R_xx → 0, R_xy = h/νe² plateaus |
| Shot noise | Current fluctuations | S = 2e*I → e* = fractional charge |
| Tunneling | I-V across barrier | Power-law: I ∝ V^{(1/ν)-1} |
| Capacitance | Compressibility dν/dμ | Incompressibility peaks at ν |
| Thermal transport | κ_xy | Quantized chiral central charge |
| NMR | Nuclear spin relaxation | Edge mode signatures |

## 7. Why FQHE Is the Right Playground for Fractional Excitons
1. **Well-defined fractional quasiparticles** (charge, statistics known)
2. **Tunable filling factors** via gate voltage → tunable quasiparticle density
3. **Clean 2D platform** (graphene/hBN: ultra-high mobility, ~10⁶ cm²/Vs)
4. **Valley/spin degeneracy** in graphene → richer phase diagram
5. **Direct optical access** to interlayer transitions (crucial for PL spectroscopy)

---

## Quick Reference: FQHE Filling Factor Sequences
| Sequence | Formula | Examples | Physics |
|----------|---------|----------|---------|
| Laughlin | 1/m (m odd) | 1/3, 1/5, 1/7 | Fundamental, simplest |
| Jain CF | p/(2p+1) | 2/5, 3/7, 4/9 | CF IQHE |
| Jain CF (hole) | 1 - p/(2p+1) | 2/3, 3/5, 4/7 | Particle-hole conjugate |
| Second LL | 2 + p/(2p+1) | 5/2, 7/3, 8/3 | Non-Abelian candidates |
| Graphene | 4(|n|+½) + ν_cf | 0, ±1, ±4... | 4-fold degeneracy |

---

*This primer covers the essential physics needed to understand fractional excitons. See `ref-02-exciton-physics.md` for exciton basics and `ref-03-theory-framework.md` for the specific theory of fractional composite bosons.*