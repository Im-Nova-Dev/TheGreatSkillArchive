# Reference: Chiral-Induced Spin Selectivity (CISS) — Molecular Spin Polarization without Ferromagnets

**Related intel:** `2026-06-02-CISS-chiral-spin-selectivity-confirmed-prl.md` (in `/home/nova/.hermes/intel/science/`)

## Connection to Fluorescent-Protein Spin Qubits
Both discoveries demonstrate **room-temperature quantum spin phenomena in molecular systems**, challenging the assumption that spin qubits require cryogenics.

| Aspect | Fluorescent-Protein Spin Qubit | CISS (Heptahelicene) |
|--------|-------------------------------|---------------------|
| **Spin source** | Photoexcited chromophore radical (EYFP) | Chiral molecular helix ([7]H) |
| **Spin control** | Optical + microwave (Rabi driving) | Molecular helicity + current direction |
| **Readout** | Fluorescence (optical) | dI/dV spectroscopy (STM) |
| **Environment** | Living cells, aqueous, 300 K | Superconductor surface, 5 K (but B=0 signal persists) |
| **Key advantage** | Genetically encodable, self-assembling | No ferromagnetic contacts needed; Onsager-Casimir compliant |

## Why CISS Matters for Quantum Biology / Molecular Spintronics
1. **Mechanism clarity:** CISS resolves the long-standing Onsager-Casimir objection by using YSR states in a superconducting tip (fixed B-field, no magnetization reversal) — the spin polarization is a property of the *chiral molecule + probe*, not an intrinsic non-reciprocal effect.
2. **Platform transferability:** Heptahelicene self-assembles on superconductors; similar chiral molecules (DNA, peptides) could be integrated with superconducting qubits for chiral spin-photon interfaces.
3. **Quantum biology link:** CISS is invoked in avian magnetoreception and electron transport in proteins — the same chiral structures that appear in biology.

## Experimental Design Lesson (for teaching)
The Meyer et al. 2026 PRL paper is a masterclass in **clean experimental design to isolate a contested effect**:
- **Eliminate artifact A (work function):** Vary tip distance → spectra invariant
- **Eliminate artifact B (magnetic impurities):** Multiple independent Mn tips → reproducible
- **Eliminate artifact C (reciprocity violation):** Fixed B-field + superconducting YSR probe + linear regime → no magnetization reversal needed
- **Single-molecule resolution:** STM submolecular imaging identifies enantiomer by LUMO site

## Key References
- Meyer, Néel, Kröger. *Single-Enantiomer Spin Polarizers in Superconducting Junctions*. **PRL 136, 226201 (2026)**. DOI: 10.1103/pgs4-4nds
- APS Physics Magazine: "Confirming the Polarizing Effect of Chiral Molecules" (2 June 2026)
- Intelfile: `/home/nova/.hermes/intel/science/2026-06-02-CISS-chiral-spin-selectivity-confirmed-prl.md`

## Teaching Integration
When explaining fluorescent-protein spin qubits, mention CISS as a **parallel molecular spin phenomenon**: both use molecular structure (chromophore pocket / chiral helix) to protect or polarize electron spin at elevated temperatures. The protein qubit *initializes/controls/reads* a spin; CISS *filters* spin by molecular handedness. Together they suggest a future toolkit of **molecular spin elements** (sources, polarizers, detectors) all operating without dilution refrigerators.