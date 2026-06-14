---
name: quantum-oracle-tuner
description: "Tune oracle parameters for quantum algorithm benchmarking."
version: 0.2.0
category: technology
---

# Quantum Oracle Tuner

## Overview

This skill provides a systematic approach to tuning oracle parameters for quantum algorithm benchmarking, particularly for Grover's search, amplitude amplification, and other oracle-based quantum algorithms. It covers parameter selection, performance profiling, and optimization workflows using common quantum computing frameworks (Qiskit, Cirq, PennyLane).

## When To Use

- Benchmarking Grover's algorithm with different oracle implementations
- Optimizing oracle depth and qubit count for NISQ devices
- Comparing oracle constructions (phase vs. bit-flip oracles)
- Calibrating oracle parameters for variational quantum algorithms
- Profiling oracle performance on simulators vs. hardware

## Prerequisites

- Python 3.10+ with quantum framework (Qiskit, Cirq, or PennyLane)
- Access to quantum simulator (local) or hardware backend (IBM Quantum, IonQ, Rigetti)
- Familiarity with oracle-based quantum algorithms

## Workflow

### 1. Define Oracle Specification

```python
# Example: Grover oracle for 3-SAT problem
def create_3sat_oracle(num_vars, clauses):
    """Create phase oracle for 3-SAT instance."""
    qc = QuantumCircuit(num_vars + 1)  # +1 for ancilla
    # Encode clauses as multi-controlled Z gates
    for clause in clauses:
        # Apply X gates for negated literals
        # Apply multi-controlled Z
        # Uncompute X gates
    return qc.to_gate(label="3SAT Oracle")
```

### 2. Parameter Space Definition

Key tunable parameters:
- `oracle_depth`: Circuit depth of oracle implementation
- `ancilla_count`: Number of ancilla qubits required
- `decomposition_level`: Gate decomposition granularity (Toffoli → CNOT+T)
- `error_mitigation`: Whether to apply ZNE/PEC/VD error mitigation

### 3. Benchmarking Loop

```python
def benchmark_oracle(oracle_factory, param_grid, backend, shots=1024):
    results = []
    for params in param_grid:
        oracle = oracle_factory(**params)
        circuit = build_grover_circuit(oracle, num_iterations)
        job = backend.run(circuit, shots=shots)
        counts = job.result().get_counts()
        success_prob = counts.get(target_state, 0) / shots
        results.append({**params, "success_prob": success_prob})
    return pd.DataFrame(results)
```

### 4. Optimization Strategies

| Strategy | Use Case | Tools |
|----------|----------|-------|
| Grid search | Small discrete parameter spaces | `itertools.product` |
| Bayesian optimization | Continuous parameters, expensive evals | `scikit-optimize`, `optuna` |
| Gradient-free (CMA-ES) | Noisy hardware evaluations | `cma` package |
| Circuit compilation passes | Pre-execution transpilation | Qiskit `transpile`, `OptimizationLevel=3` |

### 5. Hardware-Aware Tuning

```python
# Account for device topology and error rates
from qiskit.transpiler import CouplingMap
from qiskit.providers.ibmq import IBMQBackend

coupling_map = CouplingMap(backend.configuration().coupling_map)
transpiled = transpile(circuit, backend=backend, optimization_level=3,
                       coupling_map=coupling_map, initial_layout=initial_layout)
```

## Common Oracle Types

1. **Phase Oracle**: Applies phase flip to marked states
2. **Bit-flip Oracle**: Flips ancilla qubit for marked states
3. **Phase Gradient Oracle**: For amplitude estimation
4. **Quantum Walk Oracle**: For walk-based search

## Verification Steps

1. Unit test oracle unitarity: `oracle @ oracle† ≈ I`
2. Verify marked state phase flip on simulator
3. Compare transpiled depth across parameter settings
4. Run on hardware with error mitigation, compare to ideal simulation

## Reference Notes

- Oracle synthesis: arXiv:1804.03719 (Qiskit Aqua)
- Grover optimal iterations: π/4 √(N/M)
- Qiskit `QuantumCircuit.mcx` for multi-controlled gates
- PennyLane `qml.ctrl` for controlled operations
- Auto-expanded on 2026-06-06 with benchmarking workflows
