---
name: quantum-hall-edge-states-microscopy
category: physics
description: Teach the first-ever high-resolution STM imaging of topological quantum Hall edge states in graphene (Princeton, Nature 2025). Covers quantum Hall effect basics, edge states as chiral 1D channels, the 30-year experimental gap, electrostatic edge definition vs physical edges, Luttinger liquid physics, interaction-driven channel restructuring, and implications for topological quantum computing.
tags:
  - quantum Hall effect
  - topological matter
  - STM spectroscopy
  - graphene
  - Luttinger liquid
  - electron-electron interactions
  - topological quantum computing
  - edge states
  - Ali Yazdani
  - Princeton
---

# Quantum Hall Edge States Microscopy: Teaching Skill

## Overview

This skill teaches the breakthrough **first-ever direct visualization of topological quantum Hall edge states** using scanning tunneling microscopy (STM) on electrostatically defined edges in monolayer graphene. Published in *Nature* (December 2025) by the Yazdani group at Princeton.

**Core teaching challenge:** For 30 years, quantum Hall edge states were only inferred from global transport measurements. Theory predicted smooth, non-interacting channels. Experiment reveals **narrow, spatially separated channels with 4× higher velocity** — direct proof that **electron-electron interactions fundamentally restructure topological edge channels**.

---

## Prerequisites

Learners should know:
- Basic quantum mechanics (wavefunctions, Landau levels)
- Condensed matter basics (Fermi level, band structure, 2D electron systems)
- Magnetic field quantization (cyclotron motion, magnetic length ℓ_B = √(ℏ/eB))
- Basic STM principle (tunneling current ∝ local density of states)

---

## Teaching Structure

### 1. The Quantum Hall Effect Refresher (15 min)
**Key concepts to establish:**
- 2D electron gas + strong B-field → quantized Landau levels
- Bulk = insulator (localized states), Edges = chiral conducting channels
- Quantized Hall conductance: σ_xy = ν·e²/h (ν = integer filling factor)
- Edge channels = 1D wires with perfect transmission (no backscattering)

**Visual aid:** Sketch Landau level fan diagram + edge state dispersion E(k) crossing Fermi level.

### 2. The 30-Year Gap: Why Couldn't We See Them? (10 min)
| Method | Limitation |
|--------|------------|
| Global transport (Hall bar) | Only measures net conductance — no spatial info |
| Early STM/AFM | Resolution ~100 nm >> magnetic length ℓ_B ~10 nm |
| Physical edges | Disorder, reconstruction, defects blur edge states |
| Theory (non-interacting) | Predicted smooth overlapping channels — untestable |

**Key insight:** Topology guarantees channel *existence* but says nothing about *microscopic structure*.

### 3. The Breakthrough: Two Experimental Innovations (20 min)

#### Innovation 1: Electrostatic Edge Definition
- **Instead of cutting graphene**, use local gate voltage to deplete carriers → create "gentle edge"
- Advantages: atomically smooth, tunable position, no reconstruction, defect-free
- Dual-gated hBN/graphene/hBN heterostructure enables this

#### Innovation 2: Millikelvin STM in High B-Field
- Dilution refrigerator base T ~10 mK
- Vector magnet up to 12 T
- dI/dV spectroscopy with sub-nm resolution (~0.5 nm)
- Simultaneous topography + spectroscopy

### 4. What They Saw: Interaction-Driven Restructuring (25 min)

#### Finding 1: Narrow, Separated Channels
- **Theory (non-interacting):** Channels width ~ℓ_B, overlapping
- **Experiment:** Channels 13-15 nm wide, **cleanly separated** with gaps
- **Implication:** Inter-channel repulsion pushes them apart

#### Finding 2: 4× Velocity Enhancement
- Measured group velocity v ≈ 4 × v₀ (single-particle prediction)
- **Direct evidence of Luttinger liquid behavior** in 1D interacting electrons
- v/v₀ = K (Luttinger parameter) → K ≈ 4 indicates strong repulsion

#### Finding 3: Channels "Talk to Each Other"
- Channel spacing depends on filling factor ν
- Arrangement minimizes interaction energy (commensurability)
- **Theory cannot predict this arrangement a priori** — it's an emergent interacting phenomenon

### 5. Theoretical Framework: Luttinger Liquids (15 min)
**Minimal model for 1D interacting fermions:**
- Tomonaga-Luttinger Hamiltonian: H = (v/2π) ∫ dx [K(∂_xθ)² + K⁻¹(∂_xφ)²]
- K = 1: non-interacting | K < 1: repulsive interactions
- Observables: power-law tunneling DOS, spin-charge separation
- **Connection to experiment:** K ≈ 1/4 → v = v_F/K ≈ 4v_F matches data!

### 6. Paradigm Shift Summary (10 min)

| Old Paradigm | New Reality |
|--------------|-------------|
| Edge channels = single-particle Landau wavefunctions | Edge channels = **collective Luttinger liquid modes** |
| Topology dictates everything | Topology guarantees *existence*; **interactions dictate *form*** |
| Theory predicts arrangement | **Experiment discovers arrangement** theory couldn't predict |
| Passive boundaries | **Active, tunable quantum waveguides** |

### 7. Applications & Future Directions (10 min)
- **Topological qubits:** Edge states as protected quantum wires
- **Fractional QH (ν = 5/2, 12/5):** Same platform → image non-Abelian anyons
- **Quantum Hall hydrodynamics:** Viscous electron flow in channels
- **Reconfigurable networks:** Electrostatic gates → on-demand circuit topology

---

## Teaching Exercises

### Exercise 1: Magnetic Length Calculation
```python
# Calculate magnetic length ℓ_B for B = 10 T
ℏ = 1.055e-34  # J·s
e = 1.602e-19  # C
B = 10  # T
ℓ_B = sqrt(ℏ / (e * B))  # ~8.1 nm
```
**Question:** Channel width 13-15 nm vs ℓ_B ~8 nm — what does this ratio tell you about interactions?

### Exercise 2: Luttinger Parameter from Velocity
Given v_measured = 4 × v_F, calculate K and interpret.
**Answer:** K = v_F/v = 0.25 → strong repulsive interactions.

### Exercise 3: Channel Counting at ν = 2, 6
- ν = 2: 2 counter-propagating channels (spin-resolved)
- ν = 6: 6 channels (ν = 2 spin × 3 orbital? — discuss)
**Question:** Why doesn't channel count simply equal ν?

---

## Common Pitfalls to Address

1. **"Topological protection means no interactions"** → Wrong. Topology protects *existence* and *chirality*; interactions reshape *internal structure*.
2. **"STM measures wavefunctions directly"** → STM measures **local density of states** (LDOS), not wavefunctions. dI/dV ∝ LDOS(E).
3. **"Electrostatic edge = physical edge"** → Electrostatic edge is **smooth, tunable, defect-free**; physical edges have atomic-scale roughness.
4. **"Fractional QH is just smaller filling factors"** → Fractional QH involves **electron fractionalization** into anyons with fractional charge/statistics — completely different physics.
5. **"Velocity enhancement = Fermi velocity change"** → It's **collective mode velocity** (plasmon-like), not single-particle v_F.

---

## Key References (for learners)

1. **Primary paper:** Yu et al., *Nature* **636**, 786–791 (2025) | DOI: 10.1038/s41586-025-09858-3
2. **Review:** Wen, *Quantum Field Theory of Many-Body Systems* (Ch. 6: Edge states)
3. **Luttinger liquid:** Giamarchi, *Quantum Physics in One Dimension* (Oxford, 2003)
4. **Quantum Hall basics:** Girvin, *The Quantum Hall Effect* (arXiv:cond-mat/9909006)
5. **Graphene QH:** Young & Kim, *Nature Physics* **5**, 222 (2009)

---

## Intel Source

Based on: `/home/nova/.hermes/intel/science/2026-06-09-princeton-quantum-hall-edge-states-imaging.md`
- Princeton University News (2026-06-09 cron capture)
- *Nature* publication: December 17, 2025
- Lead authors: Jiachen Yu (postdoc), Kristina Wolinski (grad), Ali Yazdani (senior)

---

## Version History
- v1.0 (2026-06-09): Initial creation from Princeton breakthrough intel