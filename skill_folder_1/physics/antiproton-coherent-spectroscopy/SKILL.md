---
name: antiproton-coherent-spectroscopy
title: Coherent Spectroscopy with a Single Antiproton Spin
description: Teach the 2025 Nature breakthrough by BASE Collaboration at CERN: first coherent Rabi oscillations on a single antiproton spin, enabling precision antimatter CPT symmetry tests. Covers Penning traps, two-particle protocol, quantum metrology with antimatter, and the path to 10 ppt precision.
category: physics
tags:
  - antimatter-physics
  - quantum-metrology
  - CPT-symmetry
  - Penning-trap
  - Rabi-oscillations
  - coherent-spectroscopy
  - BASE-CERN
  - single-particle-quantum-control
related_skills:
  - quantum-echoes-and-verifiable-quantum-advantage
  - trapped-ion-scaling-and-cryogenic-electronics
  - quantum-hall-edge-states-microscopy
author: hermes
last_updated: 2026-06-06
source_paper: Latacz et al., Nature 644, 64–68 (2025) doi:10.1038/s41586-025-09323-1
recognition: First coherent spectroscopy on antimatter; 16× narrower resonance than 2017 incoherent method
institution: CERN BASE Collaboration
lead_researcher: Stefan Ulmer
---

# Coherent Spectroscopy with a Single Antiproton Spin

Teach the 2025 Nature breakthrough: the BASE Collaboration at CERN achieved the first coherent quantum transition spectroscopy on an antiproton — observing Rabi oscillations in a single nuclear spin-½ antimatter particle. This enables dramatically improved precision for CPT symmetry tests and opens quantum metrology with antimatter.

---

## First-Principles Concept

**Coherent spectroscopy** means driving a quantum system with a phase-stable oscillating field and observing the resulting **Rabi oscillations** — the coherent swinging of population between two quantum states. In NMR/ESR, this is done with ~10²³ spins. Here, it's done with **one antiproton**.

**Why it matters**: The antiproton's spin precession frequency (Larmor frequency) depends on its g-factor. Comparing **proton vs. antiproton g-factors** tests **CPT symmetry** — the fundamental theorem that particles and antiparticles have identical masses, lifetimes, and magnetic moments (except for charge sign).

---

## The Core Challenge

| Problem | Context |
|---------|---------|
| **Incoherent method (2017)** | Spin flips induced by thermal noise; resonance ~3.2 Hz linewidth; no phase control |
| **Goal for CPT test** | Need ~10 parts-per-trillion (ppt) precision on g-factor → requires Hz mHz linewidth |
| **Breakthrough** | Coherent drive → **200 mHz linewidth (16× narrower)**; 50 s coherence time |

---

## Experimental Architecture

### Multi-Penning Trap System (housed in 1.945 T superconducting solenoid at 4 K)

| Trap | Function |
|------|----------|
| **Precision Trap (PT)** | Homogeneous B-field for spin manipulation |
| **Analysis Trap (AT)** | Spin state detection via continuous Stern–Gerlach effect |
| **Cooling Trap (CT)** | Cyclotron motion cooling |
| **Reservoir & Park Traps** | Antiproton storage & handling |

### Two-Particle Measurement Protocol (Key Innovation)

| Particle | Role |
|----------|------|
| **Larmor Particle** | Undergoes spin manipulation & state detection |
| **Cyclotron Particle** | Measures B-field via cyclotron frequency → sets drive frequency for spin flips |

**Why two particles?** The B-field drifts over time. By simultaneously measuring the cyclotron frequency of a second particle in the same field, they track B-field in real time and phase-lock the spin-drive microwave — eliminating decoherence from field noise.

---

## Performance Gain: Coherent vs. Incoherent

| Metric | Coherent (2025) | Incoherent (2017) | Improvement |
|--------|----------------|-------------------|-------------|
| Spin-flip probability | > 80% | Suppressed by decoherence | Major gain |
| Spin coherence time (T₂) | ~50 s | Limited by B-field drift | New capability |
| Resonance linewidth | **200 mHz** | ~3.2 Hz | **16× narrower** |
| Signal-to-noise ratio | > 1.5× higher | Baseline | 1.5× better |
| Projected g-factor precision | 25× improvement | — | Transformative |

---

## Plain-Language Summary

> Imagine holding a single antiproton — the antimatter counterpart of a proton — in a magnetic bottle for months. You spin it like a quantum top with microwaves and watch it flip back and forth in perfect rhythm (Rabi oscillations). This coherent control reveals its magnetic moment with 16× better precision than before. Now you can compare proton vs. antiproton at the **10 parts-per-trillion** level — the most stringent test yet whether matter and antimatter obey the same physics (CPT symmetry).

---

## Teaching Order: First Principles → Mechanism → Metrology

1. **What is CPT symmetry and why test it?**
   - Lorentz-invariant QFT → CPT theorem
   - Any violation = new physics beyond Standard Model
   - Baryon sector test: proton/antiproton g-factor comparison

2. **Penning trap basics**
   - Static B-field + quadrupolar E-field → 3 oscillation modes (axial, cyclotron, magnetron)
   - Single-particle detection via image currents on trap electrodes
   - Continuous Stern–Gerlach: spin state shifts axial frequency

3. **Incoherent to coherent: the paradigm shift**
   - Old way: wait for rare thermal spin flips → measure rate vs. frequency
   - New way: drive spin coherently with phase-locked microwave → watch Rabi oscillations
   - Analogy: listening for random coin flips vs. conducting a metronome

4. **The two-particle protocol**
   - B-field stability is the killer → two particles, same B, one measures, one performs
   - Real-time feedback → phase-stable drive → long T₂ → narrow linewidth

5. **From linewidth to CPT limit**
   - Linewidth → frequency precision → g-factor precision → CPT limit
   - 200 mHz linewidth → 25× statistical precision gain → 10 ppt target

---

## Common Misconceptions to Address

- **"Antimatter falls up"** → CPT says it falls down; this experiment tests magnetic moment, not gravity
- **"One particle isn't statistics"** → Single-particle *quantum control* enables precision spectroscopy; statistics come from repeated measurements
- **"Coherent drive requires many particles"** → NMR uses ensembles for signal; here single-particle detection via Stern-Gerlach makes coherent spectroscopy possible with one particle
- **"Antiprotons annihilate instantly"** → In ultrahigh vacuum Penning traps, storage times > 1 year are routine

---

## Verification Questions for Learners

1. Why does coherent spectroscopy give narrower linewidths than incoherent methods?
2. What is the role of the *cyclotron particle* in the two-particle protocol?
3. How does the continuous Stern–Gerlach effect detect a single spin flip?
4. If the resonance linewidth is 200 mHz and the Larmor frequency is ~120 MHz, what is the relative precision on g-factor?
5. What systematic effects could still limit a 10 ppt CPT test?

---

## Key Terms

- **CPT symmetry**: Charge-Parity-Time reversal symmetry; fundamental QFT prediction
- **Penning trap**: Static magnetic + electric field confinement for charged particles
- **Continuous Stern–Gerlach**: Spin-dependent axial frequency shift for single-spin readout
- **Rabi oscillations**: Coherent population cycling between two quantum states
- **Larmor frequency**: Spin precession frequency ∝ g-factor × B-field
- **g-factor**: Dimensionless magnetic moment ratio (μ / μ_N)
- **BASE**: Baryon Antibaryon Symmetry Experiment at CERN AD/ELENA

---

## References

- Latacz et al. (2025). *Coherent spectroscopy with a single antiproton spin*. **Nature 644, 64–68**. DOI: 10.1038/s41586-025-09323-1
- Smorra et al. (2017). *A parts-per-billion measurement of the antiproton magnetic moment*. **Nature 550, 371–374**
- Ulmer et al. (2024). *Letter of Intent: BASE experiment upgrade at CERN SPS*. **CERN-SPSC-I-266**
- Intel file: `.hermes/intel/science/2025-antiproton-coherent-spectroscopy.md`

---

## Teaching Tips

- **Start with the analogy**: "NMR with one atom instead of a mole of them"
- **Emphasize the constraint**: B-field drift kills coherence → two-particle protocol is the hero
- **Connect to the big question**: "Does antimatter have the same magnetic moment as matter?" → CPT
- **Mention BASE-STEP**: Transportable trap = moving antimatter to quieter labs = next generation of precision
- **Timeline context**: 2017 (incoherent ppb) → 2025 (coherent) → next target 10 ppt