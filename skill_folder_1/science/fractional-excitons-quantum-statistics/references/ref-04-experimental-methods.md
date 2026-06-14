---
title: "Experimental Methods — PL Spectroscopy, Transport, and Gating in 2D Heterostructures"
skill: fractional-excitons-quantum-statistics
---

# Experimental Methods for Fractional Exciton Detection

## 1. Device Fabrication: Graphene/hBN Heterostructures

### 1.1 Stack Assembly (Van der Waals Transfer)
```
1. Exfoliate graphene, hBN, graphite onto SiO₂/Si
2. Identify monolayers by optical contrast + Raman
3. Pick up sequence with PDMS/PC stamp:
   Graphite (back gate)
         ↓
   hBN (~20 nm, dielectric)
         ↓
   Graphene (bottom layer)
         ↓
   hBN (~5 nm, tunnel barrier)
         ↓
   Graphene (top layer)
         ↓
   hBN (~20 nm, top dielectric)
         ↓
   Graphite (top gate)
4. Release onto SiO₂/Si, clean in vacuum/anneal
5. E-beam lithography → define Hall bar geometry
6. 1D edge contacts (Cr/Au) to graphite gates + graphene
```

### 1.2 Key Parameters
| Parameter | Typical Value | Importance |
|-----------|--------------|------------|
| Graphene mobility | >500,000 cm²/Vs | Clean FQHE states |
| hBN thickness (barrier) | 3-10 nm | Tunneling rate, exciton lifetime |
| Alignment | <0.5° twist | Avoid moiré complications |
| Contact resistance | <1 kΩ·μm | Low-noise transport |

---

## 2. Measurement Setup

### 2.1 Cryogenic + High B-Field Environment
```
Dilution refrigerator (base T < 10 mK)
    ↓
Sample in superconducting magnet (B up to 35 T)
    ↓
Wiring:
  - DC: 4-terminal Hall bars (lock-in, 10-100 nA)
  - RF: low-temp amplifiers for shot noise
  - Optical: confocal microscopy with objective inside fridge
```

### 2.2 Dual-Gate Control
- **Top gate**: tunes top layer filling νₜ
- **Back gate**: tunes bottom layer filling ν_b
- **Independent control** → scan 2D filling factor space (ν_b, ν_t)
- **Displacement field D**: controls interlayer potential, exciton energy

---

## 3. Photoluminescence (PL) Spectroscopy

### 3.1 Why PL Works for Fractional Excitons
- Interlayer excitons have **large dipole moment** → strong oscillator strength
- **Spatially indirect**: e and h in different layers → long lifetime (μs)
- **Energy tunable** via displacement field D
- **Selection rules**: σ⁺/σ⁻ polarization → valley/spin physics

### 3.2 PL Setup
```
Laser (532 nm or 638 nm, <1 μW) → cryostat window
    ↓
Objectve (NA 0.7-0.8) → focuses to ~1 μm spot
    ↓
Sample at B ⊥ plane
    ↓
Collected PL → spectrometer (grating) → CCD/EMCCD
    ↓
Time-resolved: streak camera or TCSPC (<100 ps resolution)
```

### 3.3 Key PL Measurements
| Measurement | What It Reveals |
|-------------|-----------------|
| **Energy vs. ν** | Exciton peaks at fractional fillings (1/3, 2/5...) |
| **Linewidth vs. ν** | Coherence, disorder, many-body effects |
| **Intensity vs. ν** | Population, formation efficiency |
| **Polarization (σ⁺/σ⁻)** | Valley/spin configuration |
| **Time-resolved** | Lifetime, formation dynamics |
| **B-field dependence** | Diamagnetic shift → exciton radius |
| **D-field dependence** | Stark shift → dipole moment, layer separation |

### 3.4 PL Signatures of Fractional Excitons (Zhang et al. 2025)
```
ν = 1/3:
  Sharp PL peak at E_X(1/3)
  Linewidth ~few hundred μeV
  Intensity ∝ (ν - 1/3) near filling

ν = 2/5, 3/7...:
  Additional peaks tracking fractional hierarchy
  Energy spacing = FQHE quasiparticle gaps
```

---

## 4. Electrical Transport

### 4.1 Standard Hall Bar Geometry
```
      I_in
O────────────────O
│  ○  ○  ○  ○  │  Ohmic contacts at edges
│              │
│  ○  ○  ○  ○  │
O────────────────O
      I_out
```
- **4-terminal**: eliminates contact resistance
- **Lock-in**: ~10-100 nA, 1-10 Hz (avoid heating)

### 4.2 Measured Quantities
| Quantity | Formula | FQHE Signature |
|----------|---------|----------------|
| R_xx | V_xx / I | → 0 at filling factors |
| R_xy | V_xy / I | = h/νe² plateaus |
| σ_xx | L/W R_xx/(R_xx²+R_xy²) | Activated: ∝ exp(-Δ/k_BT) |
| σ_xy | L/W R_xy/(R_xx²+R_xy²) | Quantized: ν e²/h |

### 4.3 Simultaneous PL + Transport
- **Correlate** PL peak positions with R_xx minima
- **Confirm** both layers in FQHE state
- **Map** (ν_b, ν_t) phase diagram

---

## 5. Data Analysis Techniques

### 5.1 PL Peak Fitting
```
PL(ω) = ∑ A_i / (1 + 4(ω - ω_i)²/Γ_i²) + background
```
- Lorentzian or Voigt profiles
- Extract: peak energy ω_i, linewidth Γ_i, amplitude A_i

### 5.2 Activation Gap Extraction
```
σ_xx(T) = σ_0 exp(-Δ/2k_BT)
→ Plot ln(σ_xx) vs 1/T → slope = Δ/2k_B
```
- Δ = transport gap
- Compare to PL energy spacing

### 5.3 Diamagnetic Shift
```
E_X(B) = E_X(0) + σ B²  (σ = e²⟨r²⟩/8μ)
```
- ⟨r²⟩ → exciton radius
- In FQHE: modified by Landau level mixing

### 5.4 Exciton-Exciton Interactions
- **Density-dependent shift**: ΔE = g n_X
- g = interaction strength
- g < 0: attractive (condensation); g > 0: repulsive (crystal)

---

## 6. Challenges & Troubleshooting

| Issue | Symptom | Fix |
|-------|---------|-----|
| Laser heating | R_xx increases, PL broadens | Reduce power, increase spot size |
| Charge instability | Hysteresis in ν scans | Better hBN quality, lower T |
| Disorder broadening | Γ > few meV | Improve mobility, alignment |
| Background PL | Obscures weak exciton peaks | Spectral filtering, time-gating |
| Gate leakage | Unstable filling factors | Thicker hBN, better contacts |

---

## 7. Extensions & Future Directions

### 7.1 Resonant PL / Reflectance
- Probe **exciton resonance** without above-gap excitation
- Reduce heating, access dark excitons

### 7.2 Microwave Spectroscopy
- Drive **exciton Rydberg transitions**
- Access quantum state, coherence

### 7.3 Interferometry
- **Fabry-Perot** for fractional excitons
- **Mach-Zehnder** with gate-defined channels
- Direct test of statistics via AB oscillations

### 7.4 Thermometry
- Johnson-Nyquist noise → electron temperature
- Noise thermometry for μK precision

---

*These methods underpin the 2025 Nature discovery. For teaching: emphasize **PL + transport correlation** as the key experimental proof of fractional excitons.*