---
name: topological-quantum-computing-and-majorana-zero-modes
title: Teach topological quantum computing and Majorana zero modes
description: Explain Majorana zero modes, topological protection, and why the Microsoft Majorana 2 claim matters — with first-principles physics and verification criteria.
triggers:
  - topological quantum computing
  - Majorana zero mode
  - Majorana fermion
  - non-abelian anyon
  - topological qubit
  - Majorana 2
  - Majorana 1
  - parity lifetime
  - topological protection
  - Kitaev chain
  - parafermion
---

# Topological Quantum Computing and Majorana Zero Modes

Use this skill whenever the topic is topological quantum computing, Majorana zero modes (MZMs), or the experimental claims behind Microsoft's Majorana chips. Start with the condensed-matter physics, then connect to the hardware claim.

## The Core Physical Picture

### 1. What a Majorana zero mode is
In a topological superconductor, an exotic quasiparticle can appear at a boundary or defect whose wavefunction is its own antiparticle. Concretely:
- A **Majorana operator** γ satisfies γ = γ†, so it is its own Hermitian conjugate.
- A single MZM cannot deliver a complex fermionic wavefunction alone; two MZMs combine into one ordinary fermionic mode: c = (γ₁ + iγ₂)/2.
- If the two MZMs are spatially separated, the fermion parity of the pair becomes a topological degree of freedom: locally perturbing either endpoint cannot easily flip the parity because that would require moving the MZMs together first.

### 2. Why that is interesting for quantum computing
A qubit encoded non-locally across two well-separated MZMs inherits **topological protection**: local noise couples to either endpoint individually, but cannot change the joint even/odd parity (the logical |0⟩ vs |1⟩) unless it acts collectively across the whole wire. This is the central appeal of topological quantum computing: the hardware-level error rate should be intrinsically smaller than in superconducting transmons or trapped ions.

### 3. Minimal model: the Kitaev chain
The 1D Kitaev chain is the cleanest toy model. In momentum space, the Bogoliubov–de Gennes Hamiltonian has particle-hole symmetry. When the system is tuned to the topological phase, a zero-energy solution localizes at each end of the wire. Those end states are the MZMs.

Real experimental platforms use proximitized semiconductor nanowires (often InAs or InSb with an Al superconducting shell), rather than atomic-scale p-wave superconductors.

## Experimental Evidence Criteria

A convincing Majorana-based qubit report must show **more than** a long parity lifetime:

1. **Zero-bias conductance peak** consistent with MZMs, after ruling out alternatives (Andreev bound states, disorder, poor contacts).
2. **Quantized** conductance near 2e²/h in a Coulomb-blockaded island with emergent Majorana pairs.
3. **Non-Abelian statistics** or **fusion-rule evidence** — swapping two MZMs and observing the resulting unitary transformation on the degenerate ground-state manifold.
4. **Direct qubit control and readout**: initialize, manipulate, and measure a logical qubit encoded in separated MZMs.
5. **Independent replication** by multiple groups.

## Explaining the Majorana 2 Claim in Plain Terms

For the 2026 Microsoft Majorana 2 preprint:
- **What was reported:** >20 s parity lifetime in a micrometre-scale H-shaped device, ~1,000× longer than Majorana 1.
- **What the critics say:** Parity lifetime alone is not qubit lifetime; no fusion-rule or braiding evidence has been presented; prior peer-reviewed claims lacked proof of MZMs.
- **How to assess it:** Ask how the experiment moves beyond a static parity measurement to actual qubit operations and independent validation.

## Common Misconceptions
- MZMs are not "magic" because they are individual particles — they are emergent collective boundary modes in a many-body superconducting condensate.
- Topological protection does not make a device immune to all noise; quasiparticle poisoning, thermal excitations, and measurement back-action still matter.
- A long parity lifetime is necessary but not sufficient for a topological qubit.

## Teaching Exercises
1. Derive the Kitaev chain spectrum and show the zero-mode localization at the boundary.
2. Plot a schematic zero-bias peak and discuss how Andreev bound states can mimic it.
3. Explain, with words and simple diagrams, why two MZMs separated by L have an energy splitting ~e^(-L/ξ).
4. Debate whether the Majorana 2 preprint satisfies each of the five experimental criteria above.

## Further Reading
- Kitaev, A. Y. (2001). *Unpaired Majorana fermions in quantum wires.* Physics-Uspekhi.
- Nayak, C. et al. (2008). *Non-Abelian anyons and topological quantum computation.* Reviews of Modern Physics.
- Aghaee, M. et al. (2026). Preprint at arXiv:2606.03884 (Majorana 2).
