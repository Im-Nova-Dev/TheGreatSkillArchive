---
name: condensed-matter-angular-momentum-umklapp-lattice-phonons
description: >
  Teach why and how angular momentum can reverse during transfer in a periodic
  crystal lattice. Covers Umklapp processes for lattice angular momentum,
  rotational symmetry constraints, terahertz-driven phonon control, and the
  boundary with spin phononics.
author: hermes
last_updated: 2026-06-05
source_experiment: Minakova et al., 2026, Nature Physics, observation of angular momentum transfer among crystal lattice modes
---

# Condensed Matter Angular Momentum: Umklapp and Reversal in Lattice Modes

## 1. What was observed and at what energy scale

Minakova et al. drove collective atomic rotations inside bismuth selenide with terahertz pulses and watched the coupled lattice oscillations unwind in the opposite direction after momentum exchange. This is not an artifact; it is a discrete-symmetry selection rule appearing at the level of measured polarization.

Use this skill when the learner asks: how can angular momentum flip in a solid without violating conservation laws?

## 2. Conservation, symmetry, and the phase winding of the wavefunction

### 2.1 Conservation law
Total angular momentum J = L_mech + S_spin + L_orbital must be conserved.

### 2.2 What "lattice angular momentum" means here
The experiment is best read as angular momentum carried by a circularly polarized Raman-active phonon: the displacement pattern itself has orbital angular momentum peaking at phonon quanta. This is a coarse-grained collective coordinate, not individual electron spin.

### 2.3 Symmetry selection, not magic
Crystal point groups can have improper rotations: a rotation by 2π/n plus inversion or mirror. Under such a symmetry, a state with phase winding +m can be symmetry-equivalent to a state with winding -m for a given irreducible representation, so two quanta of winding +1 can combine into a representation whose observable phase advance decreases, giving the reversal.

## 3. Textbook review: Umklapp and selection rules

### 3.1 Momentum Umklapp
In a periodic lattice, crystal momentum is conserved modulo a reciprocal lattice vector G. If two phonons with vectors q1 and q2 produce q_out = q1 + q2 − G instead of q1 + q2, the extra back-transfer of G appears as an effective sign flip in the lab-frame motion.

### 3.2 Angular-momentum Umklapp
The experiment extends this by transferring linear crystal momentum into orbital winding. When the representation mixes under symmetry, the lab-frame rotation can reverse while total angular momentum remains constant.

## 4. Terahertz excitation as coherent phonon pumping

Terahertz pulses in the THz–multithertz range couple to low-energy infrared/Raman phonons. By tuning the pulse carrier and envelope, researchers selectively excite circularly polarized phonon modes, then probe them on a subcycle timescale. The measured blue-line stroboscopic data track the instantaneous displacement phase and reveal that the coupled phonon population winds oppositely.

## 5. Why this is experimentally hard

- Thermal phonons destroy coherent rotation. Millikelvin or low-temperature conditions are needed for a clean coherent state.
- Detecting orbital angular momentum of phonons requires ultrafast polarization-sensitive probes with sub-10-fs resolution relative to THz period, plus careful calibration of residual birefringence.
- Bismuth selenide was chosen because it combines large spin-orbit coupling and a point-group structure that gives the relevant rotational symmetry.

## 6. Teaching scaffold

### Beginner
1. Explain conservation of angular momentum with a figure skater analogy.
2. Explain crystal symmetry by comparing wallpaper patterns and their rotational symmetries.
3. Distinguish the thesis from its implication: angular momentum reversed, but the total remained constant, so the lattice had to absorb the compensating angular momentum.

### Intermediate
1. Walk through the irreducible-representation selection using character tables for D3d or D4h-like lattices.
2. Show that linear momentum Umklapp implies "softening" of group-velocity predictions and solve a simpler 1D monatomic lattice example.
3. Link to spin phononics: how circular phonons couple to electron spins via spin-orbit coupling.

### Advanced
1. Formalize the selection rule: decompose Γ_total from Γ_i ⊗ Γ_j and read off whether the symmetry element contains a π rotation about the phonon polarization vector.
2. Relate to tensor properties of the third-rank nonlinear-phononic susceptibility and measure off-diagonal phonon Hall-like responses.
3. Map to a realization of an angular-momentum-transfer Umklapp term and connect to topological phonon models where winding governs valley filtering.

## 7. Boundary cases and common misconceptions

- Misconception: the atoms spin like tiny classical tops. Correction: the experimental signal is the collective center-of-mass trajectory of many atoms driven by a phonon displacement pattern, not single-atom spin.
- Misconception: angular momentum conservation failed. Correction: total J is conserved; the experimental observable is a subsystem projection that can appear reversed.
- Misconception: this is the same as a phonon Hall effect. Correction: the phonon Hall transverse shift is momentum-momentum coupling; here, the reversal is angular-momentum-angle coupling, enabled by symmetry identification.
- Boundary case: in a high-symmetry cubic Bravais lattice with inversion, the same excitation may not produce reversal, because π rotations equivalent states would absent necessary chirality.

## 8. Cross-links
- excitonic-floquet-engineering_in_semiconductors
- floquet_engineering_and_time_driven_exotic_quantum_matter
- magnetism_angular_momentum_and_spin_photonics
- topological_semimetals_and_quantum_criticality
