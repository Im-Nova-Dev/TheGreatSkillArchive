# Science Intel Index

**Purpose:** Ever-growing index mapping hard-science breakthrough topics to teaching skills.  
**Updated:** Each cron tick when new intel is saved.

---

## Topic → Skill Mapping

| Date | Topic | Intel File | Teaching Skill | Category |
|------|-------|------------|----------------|----------|
| 2026-01-14 | Quantum criticality generates topological behavior (heavy fermion hybrid state) | 2026-06-07_quantum-criticality-topology-hybrid-state.md | quantum-criticality-topology-hybrid-state | Condensed Matter / Quantum Materials |
| 2026-03-11 | Ambient-pressure superconductivity record: 151 K via pressure quenching (UH/TcSUH) | — | ambient-pressure-high-temperature-superconductivity | Superconductivity / Materials Science |
| 2026 | Fermi-gas pair correlation imaging — direct view of BCS pairing dynamics | — | fermi-gas-pair-dance-bcs-gap | Ultracold Atoms / Superconductivity |
| 2025 | Fractional excitons — new quantum statistics beyond bosons/fermions/anyons | — | fractional-excitons-quantum-statistics | Quantum Hall / Topological Matter |
| 2025 | Macroscopic quantum tunneling in Josephson junctions (Nobel Physics) | — | macroscopic-quantum-tunneling-josephson-quantum-2025-nobel | Quantum Circuits / Superconductivity |
| 2026 | Fluorescent protein spin qubits — quantum coherence in living cells | — | fluorescent-protein-spin-qubits | Quantum Biology / Quantum Information |
| 2026 | Excitonic Floquet engineering — internal periodic drives without extreme lasers | — | excitonic-floquet-engineering | Floquet Engineering / Semiconductors |
| 2026 | Nonlinear Hall effect in Bi₂Te₃ — battery-free EM energy harvesting | — | nonlinear-hall-effect-nlhe-battery-free-electronics | Topological Materials / Energy Harvesting |
| 2026 | KPZ universal growth law confirmed in 2D polaritons | — | kpz-universal-growth-law | Statistical Physics / Non-equilibrium |
| 2026 | Hollow-core optical fiber record loss — antiresonant guidance | — | hollow-core-optical-fibre-basics | Photonics / Optical Materials |
| 2026 | Quantum spin photonics at room temperature — structured light + spin coupling | — | quantum-spin-photonics-room-temperature | Quantum Photonics / Quantum Communication |
| 2025 | Topological superconductivity & Majorana experimental signatures (replication) | — | topological-superconductivity-majorana-experimental-signatures | Topological Quantum Computing |
| — | Muon g-2 magnetic moment physics | — | muon-g-2-and-magnetic-moment-physics | Particle Physics / Precision Measurement |
| — | Quantum teleportation & speed of light (no-communication theorem) | — | quantum-teleportation-speed-of-light | Quantum Foundations |
| — | CISS chiral spin selectivity | — | ciss-chiral-spin-selectivity | Spintronics / Chiral Materials |
| — | Perovskite-silicon tandem photovoltaics | — | perovskite-silicon-tandem-photovoltaics | Photovoltaics / Energy |
| — | Quantum error correction practical | — | quantum-error-correction-practical | Quantum Computing / Error Correction |

---

## Categories Tracked

- **Condensed Matter / Quantum Materials**: topological phases, heavy fermions, quantum criticality, superconductivity
- **Superconductivity / Materials Science**: high-Tc records, pressure quenching, hydrides, nickelates
- **Ultracold Atoms / Superconductivity**: Fermi gases, BCS-BEC crossover, pairing correlations
- **Quantum Hall / Topological Matter**: fractional statistics, anyons, topological order
- **Quantum Circuits / Superconductivity**: Josephson junctions, qubits, macroscopic quantum phenomena
- **Quantum Biology / Quantum Information**: bio-quantum interfaces, room-temperature coherence
- **Floquet Engineering / Semiconductors**: time-periodic drives, light-matter interaction
- **Topological Materials / Energy Harvesting**: nonlinear transport, thermoelectrics, ambient energy
- **Statistical Physics / Non-equilibrium**: KPZ, growth laws, universal scaling
- **Photonics / Optical Materials**: hollow-core fibers, antiresonant guidance
- **Quantum Photonics / Quantum Communication**: spin-photon interfaces, room-temperature quantum
- **Topological Quantum Computing**: Majorana modes, topological protection, braiding
- **Particle Physics / Precision Measurement**: g-2, fundamental constants, BSM searches
- **Quantum Foundations**: teleportation, no-communication, entanglement vs. signaling
- **Spintronics / Chiral Materials**: chiral-induced spin selectivity, molecular spin filters
- **Photovoltaics / Energy**: tandem cells, perovskites, solar conversion
- **Quantum Computing / Error Correction**: QEC codes, fault tolerance, logical qubits

---

## Cron Job Protocol

Each tick:
1. Find one substantive hard-science breakthrough (physics, biotech, materials, chemistry, cosmology, energy, robotics hardware, quantum hardware, experimental methods)
2. Save intel to `/home/nova/.hermes/intel/science/YYYY-MM-DD_topic.md`
3. Create or enhance a teaching skill in `/home/nova/.hermes/skills/science/<topic>/SKILL.md`
4. Append entry to this INDEX.md

Priority order:
1. First-principles physics results (Nature, Science, PRL, PNAS, PRX)
2. Materials science / chemistry discoveries with mechanistic insight
3. Cosmology / astrophysics findings with fundamental implications
4. Energy technology breakthroughs with demonstrated performance
5. Robotics / quantum hardware advances with experimental validation
6. Fallback: engineering breakthroughs or neuroscience results with hard-science basis