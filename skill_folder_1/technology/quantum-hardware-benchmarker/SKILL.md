---
name: quantum-hardware-benchmarker
description: "Benchmark quantum hardware with fidelity and gate latency metrics."
version: 0.2.0
category: technology
---

# Quantum Hardware Benchmarker

Comprehensive framework for benchmarking quantum processors across superconducting, trapped-ion, photonic, and neutral-atom platforms.

## When To Use

- Evaluating new quantum hardware for algorithm deployment
- Comparing cloud quantum providers (IBM, IonQ, Rigetti, AWS Braket, Azure Quantum)
- Validating quantum error correction codes against physical error rates
- Tracking device drift over time for calibration scheduling
- Research publications requiring standardized benchmark reporting

## Key Metrics

### Gate Fidelity
- Single-qubit RB: Randomized benchmarking for 1Q gates (Clifford group)
- Two-qubit RB: Simultaneous RB for parallel 2Q gates
- Interleaved RB: Specific gate fidelity (CZ, iSWAP, sqrt(iSWAP), CNOT)
- Leakage RB: Population leakage to non-computational states

### Coherence Times
- T1 (Energy relaxation): Inversion recovery / population decay
- T2 (Dephasing): Hahn echo / CPMG sequences
- T2* (Ramsey): Free-induction decay

### Readout
- Assignment fidelity: |0> vs |1> discrimination
- Readout crosstalk: Multi-qubit measurement correlation
- Active reset fidelity: Ground-state preparation after measurement

### Latency & Throughput
- Gate times: Physical duration of native gates
- Circuit latency: End-to-end execution including compilation
- Repetition rate: Shots/second for NISQ variational algorithms
- Queue time: Cloud access wait (provider-specific)

## Standard Benchmark Suites

| Suite | Focus | Platforms | Output |
|-------|-------|-----------|--------|
| QED-C | Industry standard | All | JSON/CSV |
| SupermarQ | Application-oriented | Superconducting, ion | HST, MIR |
| QV (Quantum Volume) | Holistic (width x depth) | All | Single integer |
| XEB (Cross-Entropy) | NISQ supremacy | Google, others | XEB fidelity |
| Mirror RB | Scalable fidelity | All | Process fidelity |

## Workflow

### 1. Hardware Characterization


### 2. Run Benchmark Circuits


### 3. Process & Report


## Cloud Provider APIs

| Provider | SDK | Auth | Notes |
|----------|-----|------|-------|
| IBM Quantum | qiskit-ibm-runtime | API token | Sessions, primitives |
| IonQ | ionq-client | API key | JSON circuits |
| Rigetti | pyquil + quilc | QCS auth | Parametric compilation |
| AWS Braket | amazon-braket-sdk | AWS creds | Hybrid jobs |
| Azure Quantum | azure-quantum | Azure AD | QIR, multiple targets |

## Automation Tips

- Scheduled calibration tracking: Cron job polling backend.properties() daily
- Drift detection: CUSUM on T1/T2/fidelity time series
- Multi-provider comparison: Normalize to QED-C schema, plot radar charts
- CI gate: Fail PR if new device calibration drops below threshold

## Verification Steps

1. Run RB on simulator with known noise model -> recover input params
2. Compare cloud-reported calibration vs. measured RB (should match ~10%)
3. Cross-validate XEB vs. RB on same qubit pairs
4. Verify JSON schema compliance with QED-C validator

## Reference Notes

- QED-C Benchmarking Standards v1.0 (2023)
- SupermarQ: https://github.com/SupermarQ/SupermarQ
- Qiskit Experiments: https://qiskit.org/ecosystem/experiments/
- Quantum Volume: arXiv:1811.12926
- XEB: Nature 574, 505-510 (2019)
