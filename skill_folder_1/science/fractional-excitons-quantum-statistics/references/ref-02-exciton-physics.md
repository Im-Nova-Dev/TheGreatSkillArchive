---
title: "Exciton Physics — Formation, Binding, and Spectroscopy"
skill: fractional-excitons-quantum-statistics
---

# Exciton Physics — From First Principles

## 1. What Is an Exciton?
A **bound state of an electron and a hole** (absence of an electron in a filled valence band), held together by Coulomb attraction. The prototypical quasiparticle of semiconductor optics.

**Charge**: 0 (neutral)
**Spin**: singlet (S=0) or triplet (S=1) depending on electron/hole spin alignment
**Binding energy**: E_b = μ e⁴ / (2 ħ² ε²) (hydrogenic model)
  - μ = reduced mass = mₑ*mₕ/(mₑ+mₕ)
  - ε = dielectric constant

## 2. Types of Excitons

### 2.1 By Dimensionality
| Dimension | System | Binding Energy | Radius |
|-----------|--------|----------------|--------|
| **3D (bulk)** | GaAs, Si | ~meV (4-10) | ~10-50 nm (Wannier) |
| **2D (quantum well)** | MoS₂, GaAs QW | ~100-500 meV | ~1-5 nm |
| **1D (nanotube)** | CNTs | ~100-400 meV | ~1-10 nm |
| **0D (quantum dot)** | CdSe, PbS QDs | ~tens-hundreds meV | confined by dot |

### 2.2 Wannier-Mott vs. Frenkel
| Feature | Wannier-Mott (delocalized) | Frenkel (localized) |
|---------|---------------------------|---------------------|
| Radius | ≫ lattice constant | ~lattice constant |
| Binding | weak (meV) | strong (eV) |
| Materials | inorganic semiconductors | molecular crystals, organics |
| WF overlap | large | small |
| Binding formula | Rydberg-like: E_b = Ry*/n² | molecular orbital theory |

### 2.3 Special Types
- **Direct/indirect**: same/different k-space valley
- **Intralayer/interlayer**: e & h in same layer vs. separate layers
- **Dark/bright**: spin-forbidden/allowed optical transitions
- **Charged excitons (trions)**: X⁻ (2e+1h), X⁺ (1e+2h)
- **Biexcitons**: 2e+2h bound complexes

## 3. Exciton Dynamics

### 3.1 Formation
1. **Optical excitation**: photon creates e-h pair above gap
2. **Thermalization**: carriers lose energy via phonon emission
3. **Capture**: Coulomb attraction binds e+h → exciton
   - Timescale: ~ps in 2D, ~ns in bulk

### 3.2 Recombination
- **Radiative**: exciton → photon (bright excitons)
  - Rate ∝ |⟨Ψ(0)|² (WF at zero e-h separation)
  - Lifetime: ~ns (Wannier) to ps (Frenkel)
- **Non-radiative**: Auger, defect trapping, phonon-assisted

### 3.3 Transport
- Neutral → no net current from E-field
- **Diffusion**: D = k_BT τ / m_X
- **Drift**: can be driven by temperature/strain gradients
- **Dissociation**: high E-field ionizes exciton (Mott transition)

## 4. Spectroscopy of Excitons — Key for Fractional Excitons

### 4.1 Photoluminescence (PL) — The Primary Tool
**Process**: excite above gap → e-h pairs form → thermalize → emit photon at E_X
- **Peak energy** = E_gap - E_b + E_conf + E_Zeeman + ...
- **Linewidth** = homogeneous (lifetime) + inhomogeneous (disorder)
- **Polarization** reveals valley/spin selection rules
- **Temperature dependence**: thermal broadening, dissociation

### 4.2 Reflectance/Transmission/Absorption
- Probe **exciton resonance** without carrier injection
- Reveal oscillator strength, binding energy directly

### 4.3 Pump-Probe / Transient Absorption
- Sub-ps dynamics: formation, cooling, dissociation
- Track populations, coherences

### 4.4 Magneto-PL (Critical for FQHE Excitons)
- B-field quantizes LLs → discrete exciton lines
- **Zeeman splitting**: spin/valley physics
- **Diamagnetic shift**: ⟨r²⟩ → exciton radius
- **Fractional filling**: new peaks at ν = 1/3, 2/5...

## 5. Excitons in Magnetic Fields

### 5.1 Integer QHE Regime
- LLs fully filled/empty → well-defined e and h states
- Inter-LL transitions: **exciton = e in LL_n + h in LL_m**
- Spectroscopy reveals **magnetoexciton dispersion** E_X(q)

### 5.2 Fractional QHE Regime — NEW PHYSICS
**Conventional wisdom**: FQHE too correlated for excitons
- Adding e+h disrupts topological order
- But: **Zhang et al. 2025 found excitons *exist* in FQHE!**

**Mechanism**:
```
Lowest Landau level (ν = 1/3)
         ↓
Electron quasiparticle: charge -e/3 (anyonic)
         ↓
Hole quasiparticle: charge +e/3 (anyonic)
         ↓
Bound pair: charge 0, statistics = ?
```

## 6. Interlayer Excitons in Bilayer Systems
- Electron in one layer, hole in another
- **Tunneling barrier** (hBN) controls overlap
- **Permanent dipole moment** p = e d (d = layer separation)
- **Stark shift**: E = -p·E_field → voltage-tunable energy
- **Long lifetime** (μs-ms): spatial separation suppresses recombination
- **Condensation**: dipolar repulsion → crystallize/spatial separation

**This is exactly the Brown U. platform**: graphene/hBN/graphene

## 7. Why Fractional Excitons Are Different

| Property | Conventional Interlayer Exciton | Fractional Exciton |
|----------|--------------------------------|-------------------|
| Constituents | free e & h (integer charge) | FQHE quasiparticles (fractional charge) |
| Binding energy | Coulomb e-h attraction | Coulomb + correlation energy |
| Statistics | boson-like (tends to condense) | **hybrid / exotic** |
| Stability | weak B-field OK | **requires FQHE gap** |
| Tunability | gate, B-field, E-field | gate (filling factor), B-field |
| Theoretical framework | well-established | **actively developing** |

## 8. Binding Mechanism in FQHE
Not simple Coulomb! The FQHE gap itself mediates binding:
- Creating free fractional e+h costs FQHE gap energy
- Binding them recovers some correlation energy
- **Net binding** = correlation gain - Coulomb cost

**Analogy**: Cooper pairs in BCS — binding mediated by phonons, not bare Coulomb

---

## Key Equations Summary

| Quantity | Formula | Notes |
|----------|---------|-------|
| 2D exciton Rydberg | Ry* = μ e⁴ / (2 ħ² ε²) | ε = 2D dielectric function |
| 2D Bohr radius | a* = ħ² ε / (μ e²) | ~1-5 nm in TMDs, ~10 nm in graphene/hBN |
| Binding energies 2D | E_n = -Ry* / (n - ½)² | Non-hydrogenic due to Keldysh potential |
| PL peak shift | ΔE = E_Z + E_dia + E_stark + ... | Zeeman + diamagnetic + electric field |
| Exciton dispersion | E_X(q) = E_X(0) + ħ²q²/2m_X + ... | m_X ≈ m_e + m_h |

---

*This reference provides the exciton physics foundation. See `ref-01-fqhe-primer.md` for the FQHE side and `ref-03-theory-framework.md` for how they combine.*