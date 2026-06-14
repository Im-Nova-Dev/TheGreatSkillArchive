---
name: von-neumann-entropy-and-measurement
description: Teach von Neumann entropy, quantum measurement completeness, majorization, purification, and connections to classical Shannon entropy for advanced CS/math students.
---

# Von Neumann Entropy and Measurement Completeness

Use this skill to teach quantum-state uncertainty, how measurement restricts uncertainty, and the link between classical and quantum entropy.

## Scope
- Density matrices and von Neumann entropy
- Measurement postulates
- Information gain vs disturbance
- Concavity and majorization connections

## 1. Density Matrix and von Neumann Entropy
- Density matrix: ρ = Σ_i p_i |ψ_i⟩⟨ψ_i|
- Properties:
  - Hermitian, trace 1, positive semidefinite
  - Pure state iff ρ^2 = ρ
- von Neumann entropy: S(ρ) = -Tr(ρ log ρ)
- Connection to Shannon entropy: if ρ is diagonal in some basis, S(ρ) = H(eigenvalue distribution)

Teaching point: von Neumann entropy is the quantum generalization of Shannon entropy for statistical ensembles.

## 2. Measurement as a Channel
- Projective measurement {Π_k}
- Post-measurement state:
  - λ_k ρ_k = Π_k ρ Π_k
  - measurement probabilities: p(k) = Tr(Π_k ρ)
- Average post-measurement state:
  - ρ' = Σ_k Π_k ρ Π_k
- Measurement leaves uncertainty:
  - S(ρ') ≥ S(ρ) in general
- Special case: complete/projective measurement reduces entropy toward the Shannon entropy of the measurement distribution

Teaching point: measuring destroys coherence and can increase or decrease entropy depending on basis and state mixedness.

## 3. Majorization and Spectra
- λ(ρ) majorizes λ(ρ') under complete measurement
- Schur-Horn theorem relates diagonal elements to eigenvalues
- Unitary dynamics preserves spectrum and entropy
- Lindblad/Kraus operations generally do not

## 4. Purification
- Every mixed state ρ on A can be realized as a pure state |Ψ⟩ on A+B
- Purification is not unique; relates to Schmidt decomposition
- Entanglement and entropy link:
  - S(ρ) = entanglement entropy of purification

## 5. Classical-Quantum Bridge Exercise
1) Given ρ = 1/2|0⟩⟨0| + 1/2|+⟩⟨+|, compute S(ρ).
2) Show S(UρU†) = S(ρ).
3) Show S(ρ') ≥ S(ρ) for dephasing in the computational basis.
4) For a qubit with Bloch vector r, S(ρ) = h((1+|r|)/2), where h is binary entropy.

## Pitfalls
- Treating measurement as always reducing information
- Forgetting von Neumann entropy is basis-independent
- Confusing ensembles with density matrices

## Intuition Summary
- unitary => spectrum preserved => entropy preserved
- measurement => typically increases rank => increases entropy
- purification shows mixedness is relational