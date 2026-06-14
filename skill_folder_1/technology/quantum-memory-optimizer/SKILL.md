---
name: quantum-memory-optimizer
description: "Optimize quantum memory allocation and coherence time for NISQ devices."
version: 1.0.0
category: technology
---

# Quantum Memory Optimizer

## Overview

This skill provides practical workflows for optimizing quantum memory allocation and maximizing coherence times on NISQ (Noisy Intermediate-Scale Quantum) devices. Covers memory mapping strategies, dynamical decoupling sequences, error mitigation for memory-intensive circuits, and platform-specific tuning for superconducting qubits, trapped ions, and neutral atoms.

## When To Use

- Designing quantum algorithms requiring long-lived quantum memory (quantum repeaters, quantum error correction cycles, variational algorithms with deep circuits)
- Debugging unexpectedly short coherence times in experiments
- Preparing for quantum volume benchmarks or algorithmic benchmarking
- Cross-platform memory characterization and comparison

## Core Concepts

### Memory Hierarchy on NISQ Devices

1. **Physical Qubit Memory** - Raw T1/T2 relaxation times (typically 50-500 µs for superconducting, 1-10 s for trapped ions)
2. **Logical Qubit Memory** - Effective coherence after error correction/dynamical decoupling
3. **Quantum RAM (qRAM)** - Addressable superposition storage (bucket-brigade, fan-out architectures)
4. **Classical Control Memory** - Pulse waveform storage, feedback latency budgets

### Key Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| T1 (relaxation) | > 100 µs (SC), > 1 s (ions) | Inversion recovery |
| T2* (dephasing) | > 50 µs (SC), > 500 ms (ions) | Ramsey |
| T2 (echo) | > 2x T2* | Hahn echo / CPMG |
| Gate fidelity | > 99.9% (1q), > 99% (2q) | RB / GST |
| Memory lifetime / gate time | > 10^4 | Derived |

## Workflow

### 1. Characterize Baseline Memory Performance

```bash
# Run coherence characterization suite
python -m qiskit_experiments.library.characterization.T1 \
  --qubits 0,1,2 --backend ibm_sherbrooke
python -m qiskit_experiments.library.characterization.T2Hahn \
  --qubits 0,1,2 --backend ibm_sherbrooke
python -m qiskit_experiments.library.characterization.T2Ramsey \
  --qubits 0,1,2 --backend ibm_sherbrooke
```

**Output**: Per-qubit T1, T2_echo, T2_ramsey with confidence intervals.

### 2. Map Memory-Friendly Qubit Subsets

```python
from quantum_memory_optimizer import QubitMemoryMap

mapper = QubitMemoryMap(backend)
# Find clusters of qubits with high T1/T2 and low crosstalk
memory_clusters = mapper.find_coherent_clusters(
    min_t1_us=100,
    min_t2_us=50,
    max_crosstalk_hz=1000,
    cluster_size=4
)
print(f"Best 4-qubit memory register: {memory_clusters[0]}")
```

### 3. Apply Dynamical Decoupling (DD) Sequences

```python
from quantum_memory_optimizer import DDSequenceBuilder

# Choose sequence based on noise spectrum
dd = DDSequenceBuilder()
# For 1/f noise (typical superconducting)
cpseq = dd.build_cpmg(n_pulses=8, tau_us=2.5)
# For non-Markovian noise (trapped ions)
uddseq = dd.build_udd(n_pulses=16, total_time_us=200)

# Embed in circuit
from qiskit import QuantumCircuit
qc = QuantumCircuit(4)
qc.h(0)
qc.cx(0,1)
qc.cx(1,2)
qc.cx(2,3)
qc = dd.insert_dd(qc, cpseq, qubits=[0,1,2,3])
```

### 4. Optimize Memory Allocation for Algorithms

```python
from quantum_memory_optimizer import MemoryAllocator

allocator = MemoryAllocator(
    backend=backend,
    memory_map=memory_clusters[0],
    dd_sequence=cpseq
)

# For VQE: minimize memory footprint of ansatz
optimized_ansatz = allocator.compress_ansatz(vqe_ansatz, strategy="commute")

# For QEC: maximize logical memory lifetime
logical_t2 = allocator.estimate_logical_t2(
    code="surface_code",
    distance=3,
    physical_t1=memory_clusters[0].t1_median,
    physical_t2=memory_clusters[0].t2_median
)
```

### 5. Error Mitigation for Memory-Intensive Circuits

```python
from quantum_memory_optimizer import MemoryErrorMitigator

mitigator = MemoryErrorMitigator(backend)

# Zero-Noise Extrapolation with memory-aware noise scaling
zne_result = mitigator.zne_memory_aware(
    circuit=deep_circuit,
    memory_qubits=[0,1,2,3],
    scale_factors=[1.0, 1.5, 2.0, 2.5],
    extrapolation="richardson"
)

# Probabilistic Error Cancellation with memory channel model
pec_result = mitigator.pec_memory_channel(
    circuit=deep_circuit,
    memory_time_us=50,
    qubit_subset=[0,1,2,3]
)
```

## Platform-Specific Tuning

### Superconducting (IBM, Google, Rigetti, IQM)

- **DD**: CPMG/UDD with 16-64 pulses optimal for 1/f flux noise
- **Frequency allocation**: Avoid frequency collisions during memory idle
- **Echo scheduling**: Align echoes to gate boundaries to avoid crosstalk
- **Reset optimization**: Use selective reset for ancilla qubits

### Trapped Ions (Quantinuum, IonQ, AQT)

- **DD**: UDD or KDD sequences; magnetic field noise dominant
- **Transport-aware memory**: Minimize shuttling during memory hold
- **Sympathetic cooling**: Schedule cooling cycles between memory ops
- **State-selective detection**: Use metastable states for long-term storage

### Neutral Atoms (QuEra, Atom Computing, Pasqal)

- **DD**: Spin-echo with global pulses; Rydberg dressing for protection
- **Atom loss mitigation**: Redundant encoding across multiple atoms
- **Tweezer lifetime**: Optimize trap depth vs. heating trade-off
- **Parallel memory**: Exploit 2D array for distributed memory

## Verification Steps

```bash
# 1. Verify coherence improvement
python verify_memory.py --baseline baseline_t2.json --optimized optimized_t2.json

# 2. Run algorithmic benchmark
python -m qiskit_experiments.library.quantum_volume \
  --qubits 0,1,2,3 --backend optimized_backend

# 3. Compare memory lifetime vs gate ratio
python analyze_memory_ratio.py --circuit deep_circuit.qasm
```

**Success Criteria**:
- T2_echo improves by ≥ 2x with DD
- Logical memory lifetime > 10^4 × gate time
- Algorithmic fidelity improvement > 20% on memory-bound circuits

## Reference Notes

- Based on: "Quantum Memory for NISQ Devices" (PRX Quantum 2023), "Dynamical Decoupling for Superconducting Qubits" (PRL 2022), "Quantum Volume Benchmarking" (Nature 2019)
- Auto-elaborated from stub on 2026-06-07
- Extend with platform-specific calibration routines and hardware-specific pulse-level optimization