---
name: quantum-criticality-and-emergent-topology
title: Teach quantum criticality and emergent topology in strongly correlated materials
description: Explain how quantum criticality can generate topological behavior in strongly interacting electron systems, using the emergent topological semimetal as a concrete example. Covers Kondo physics, heavy fermions, renormalization-group fixed points, band inversion, symmetry-protected topology, and the design rules for new quantum materials.
---

# Quantum Criticality and Emergent Topology

## Core conceptual units

Teach in this order, as each layer depends on the previous one.

### 1. Quantum criticality without topology

**What it is.** In many materials, tuning pressure, doping, or field drives electrons between ordered phases (e.g., magnetically ordered vs. paramagnetic). At the quantum critical point, quantum fluctuations span all length scales, creating a scale-invariant state with no classical analog.

**Toy model.** A Kondo lattice where local moments are screened at low T. Near the quantum critical point, the effective mass of quasiparticles diverges:

```
m* / m_bare ∝ |T - Tc|^(-νz)
```

- `ν` is the correlation-length exponent
- `z` is the dynamical exponent

In heavy fermions, this leads to very large specific heat (because electrons act much heavier), huge magnetic susceptibility, and highly correlated Fermi surfaces.

### 2. Electronic topology in non-interacting systems

**What it is.** Band structure can be classified by topological invariants (Chern numbers, Z2 indices). A topological insulator has edge states protected by symmetry; a topological semimetal has band touchings at Fermi level with a topological charge (Berry curvature monopole).

**Toy model.** A 2D Dirac Hamiltonian:

```
H(k) = v_F (σ_x k_x + σ_y k_y)
```

Integrate over the Brillouin zone to get a Chern number; nonzero Chern => chiral edge mode. In 3D, you get Weyl nodes with definite chirality.

### 3. The reversal: topology from interactions

**Traditional view.** Strong interactions typically smear band structures, open Mott gaps, and destroy topological invariants.

**The 2026 finding.** In the emergent topological semimetal paper (Nature Physics, Jan. 14, 2026), theory and experiment together showed that quantum critical fluctuations can **induce** band inversions and topological structures in an otherwise ordinary band structure.

**Mechanism sketch (first principles).**
1. Start with a heavy-fermion Kondo lattice (e.g., local f-electrons hybridizing with conduction electrons).
2. Choose a quantum critical point where Kondo screening and RKKY interaction compete.
3. The renormalization group flow generates a **non-Fermi liquid fixed point**; the Landau quasiparticle peak collapses into a branch cut.
4. Because the system sits near a symmetry-protected phase boundary, the branch cut intersects the Fermi level in a structured way — effectively creating a topological semimetal from a topological insulator or semimetal side.

**Key insight from the paper.** The topological character here is not in the bare band structure; it is emergent because the RG flow reorganizes the low-energy degrees of freedom into a topological form.

### 4. Heavy fermion mechanism: Kondo screening and the single-impurity case

For intuition:

- A single magnetic impurity in a metal is screened at T < T_K, the Kondo temperature.
- The low-energy fixed point is a singlet: `|ψ> = (|↑_f, ↓_c> - |↓_f, ↑_c>) / sqrt(2)`.
- The effective Hamiltonian near this fixed point is a Fermi liquid with a renormalized `g* = 2/(2 n_f + 1)`, where `n_f` is the occupancy of the f-orbital.

In the lattice version, the critical competition between this high-T local moment and low-T Kondo screening drives the quantum criticality. It is this critical competition that reshapes the band structure enough to flip topology.

### 5. Symmetry and topology

The emergent topological semimetal in the experiment was identified in a non-centrosymmetric heavy fermion superconductor. Key points to explain:

- Time-reversal symmetry and crystal symmetry together protect specific band crossings.
- Weyl nodes come in pairs with opposite chirality; in this case, their positions in momentum space are set by the critical RG structure.
- Surface Fermi arcs are the smoking-gun signature: open curves connecting the projections of bulk Weyl nodes.

### 6. Design rules for next materials

Given the mechanism, the paper gives an actionable materials design recipe:

1. Identify materials with a quantum critical point; heavy fermion or flat-band systems are fertile because correlation strength is large.
2. Check band structure near the critical point for an inversion or crossing that is symmetry-allowed.
3. Ensure the topological candidate is protected by time-reversal or crystalline symmetry.
4. Look for a sharp upturn in residual resistivity or a field-induced quantum phase transition; both indicate a topological semimetal nearby.

**Why this matters for technology.** The resulting state combines the **high sensitivity** of quantum criticality (useful for sensing) with the **robustness** of topology (useful for quantum memory and computation).

## Teaching exercises

1. Explain why a diverging effective mass at a quantum critical point by itself does not guarantee topological behavior, and what additional condition is needed.
2. Draw the single-impurity Kondo RG flow and mark the unstable versus stable fixed points.
3. Given a heavy fermion compound, identify which experimental signature (specific heat, resistivity upturn, de Haas-van Alphen frequency anomaly) would most directly signal an emergent topological semimetal.
4. Compare the emergent topological semimetal from this work with the Kitaev-chain Majorana zero mode: which is topological by construction, and which is emergent from strong correlations?
5. Explain why finding Weyl nodes at a quantum critical point is more surprising than finding them in a non-interacting tight-binding model.

## Misconceptions to address

- **Misconception:** Topology requires non-interacting electrons or weak correlations.
  **Correction:** The emergent topological semimetal shows that strong interactions, via a quantum critical fixed point, can reorganize the low-energy excitations into a topologically non-trivial form.
- **Misconception:** A long parity lifetime or large effective mass automatically implies topological protection.
  **Correction:** The topological character requires a protected band crossing or invariant. Long lifetimes without that structure are simply correlated metals.
- **Misconception:** Quantum criticality only destroys order.
  **Correction:** At a quantum critical point, fluctuations can select a topological form; the competition between Kondo screening and RKKY interaction is a concrete example.

## Related skills

- Topological quantum computing and Majorana zero modes for the Majorana hardware side
- Floquet engineering and driven quantum matter for driven topological phases
- Macroscopic quantum tunnelling and Josephson junction physics for macroscopic quantum coherence examples

## Key references

- Chen, L. et al. "Emergent topological semimetal from quantum criticality." Nature Physics 22, 218–224 (2026). https://doi.org/10.1038/s41567-025-03135-w
- Si, Q. & Paschen, S. "Quantum-criticality and topological semimetals." (associated theoretical work and review references)
- Coleman, P. "Introduction to Many-Body Physics." Cambridge University Press — for Kondo and heavy fermion fixed-points.
- Kitaev, A. Y. "Unpaired Majorana fermions in quantum wires." Physics-Uspekhi (2001) — for the non-interacting topological toy model contrast.
