---
name: tee-fail-memory-bus-side-channel
title: TEE Memory Bus Side-Channel Extraction
description: Teach offensive TEE memory bus extraction via DDR5 interposition side channels, including TEE.fail / extlZAG DDR5 attack methodology, hardware capture primitives, signal reconstruction, SGX/TDX/SEV-SNP key recovery, red-team physical attack strategies, forensic implications, and CTF exercises. Canonical intel reference: /home/nova/.hermes/intel/cybersecurity/2026-06-05_ddr5-memory-bus-interposition-tee-fail.md.
triggers:
  - DDR5 memory bus interposition
  - TEE.fail
  - SGX TDX SEV-SNP side channel
  - TEE memory extraction
  - physical DRAM bus probing
  - memory encryption bypass
  - RDIMM lane signal capture
  - hardware TEE attack
---

# TEE Memory Bus Side-Channel Extraction

## When to use this skill
Use when teaching offensive techniques, red-team workshops, or incident response planning around memory bus probing on DDR5 systems that employ Trusted Execution Environment (TEE) protections. Includes Intel SGX/TDX and AMD SEV-SNP threat models, hardware capture methodology, signal processing, and detection limitations.

## Prerequisites
1. Understanding of memory encryption basics: AES-XTS, memory controller encryption flows
2. Background in side-channel analysis, signal capture, and digital logic analysis
3. Knowledge of DDR5 physical layer: RDIMM lanes, 3200 MT/s JEDEC signaling, clocks
4. Familiarity with TEE remote attestation and provisioning flows

## Core Concept (Offensive)
Security guarantees from TEEs depend on memory confidentiality and integrity. By capturing cryptographic outputs on the DRAM bus via hardware probes, an attacker recovers the deterministic transformations produced by CPU memory controllers. Because AES-XTS in TEE designs behaves deterministically, repeated ciphertext/noise/pattern analysis leads to secret recovery without accessing CPU internals.

This attack does not require a logic-design vulnerability or software bug. It operates physical-layer and bypasses all software security boundaries.

## Hardware Capture Model
- **Target memory subsystem**: DDR5 RDIMM/LRDIMM or SO-DIMM on Intel TDX/SGX or AMD SEV-SNP systems
- **Probe**: Low-cost interposer or isolated tap soldered or clipped to DIMM bus lines
- **Capture**: Resistive-capacitive isolated tap plus FPGA-based logic analyzer at 3200 MT/s
- **Output**: Lane-synchronized bitstream of memory bus events (reads/writes)

## Signal Processing Steps
1. Capture full DRAM bus traces during TEE operations (attestation quote generation, SEV SNP guest creation, key load).
2. Locate deterministic cipher text blocks produced by AES-XTS memory encryption.
3. De-multiplex DDR5 lane aggregation back into structured memory read events.
4. Statistically isolate Provisioning Certification Keys (PCK), TDX identity material, and ECDH private keys.
5. Verify recovered keys by replaying quoted attestation verification.

## Exploitation Outcomes (Red Team / Threat)
- **Attestation bypass**: Generate forged SGX/TDX quotes trusted by remote verifiers
- **Provisioning key disclosure**: Forge infrastructure-level certificates or spoof hardware identity
- **BuilderNet MEV pre-image reconstruction**: Unauthorized blockchain front-running
- **Confidential VM secret extraction**: Escape SEV-SNP confidentiality guarantees for sensitive workloads
- **Persistent impersonation**: Replay extracted TDX identity across nodes in a confidential computing pool

## Detection Difficulty
**Extremely high.** No software-only anomaly detection is possible because:
- Encryption remains cryptographically valid.
- CPU attestation logs look clean.
- No memory integrity violation arises.

Mitigation relies on physical and operational controls:
- Tamper-evident seals and chassis intrusion detection.
- Restricted physical access to rack-room/cage.
- Rack door locks, biometric entry, camera coverage.
- TEMPEST shielding / RF/EM shielding at DRAM bus.

Host-side mitigations:
- Rapid revocation of compromised attestation identities.
- Memory integrity via Merkle-tree root verification.
- Monitoring attestation freshness and repeated quote resets.

## Affected Target Class
- On-prem data-center servers with DDR5 RDIMM and active TEE
- Cloud provider confidential computing nodes
- Edge nodes using SEV-SNP / TDX
- Workstations/laptops soldered or SO-DIMM DDR5 with Intel/AMD TEE active

## MITRE ATT&CK Mapping
| Technique | ID | Role |
|---|---|---|
| Credential Access: Unsecured Credentials | T1552 | Device provisioning secret or attestation key theft |
| Exploitation for Credential Access | T1052 | Memory bus signal capture as primitive |
| Collection: Data from Local System | T1114 | Offline construction of plaintext memory traces |
| Exfiltration Over Alternative Channel | T1048 | Side-channel semantic extraction |
| Data from Local System: Local Host Enumeration | T1018 | Derive system / TEE identity for future targeting |
| Hardware / Device Modifications | T1600 | Physical DRAM tap / probe as adversary infrastructure |

## CTF Lab Exercises
1. **Easy**: Given a simulated DDR5 trace with embedded AES-XTS ciphertext blocks, recover the deterministic key block of a PCK.
2. **Medium**: Given timing-aligned lane signals, locate boundary of a TDX attestation quote in a memory capture trace.
3. **Hard**: Design a software emulator using provided lane sample data to reconstruct an enclave secret in a reproducible way.
4. **Expert**: Design port selection policy on a test rack to minimize optical isolation failure rates; document hardware erro that defeat the attack.

## Detection and Response
- Deploy physical monitoring: tamper seals, door sensors, cameras, strict rack access.
- Configure BMC firmware attestation and secure boot.
- Rotate TDX / SGX attestation keys on a tight schedule.
- Monitor for anomalous attestation quote submission patterns.
- Maintain incident response playbooks for hardware compromise.

## References
- TEE.fail paper: `https://tee.fail/files/paper.pdf`
- TEE.fail project site: `https://tee.fail`
- IEEE SP 2026 poster PDF: `https://www.ieee-security.org/TC/SP2026/downloads/posters/sp2026posters-final75.pdf`
- Antmicro DDR5 tester article: `https://antmicro.com/blog/2023/07/open-source-data-center-rdimm-ddr5-tester-for-memory-vulnerability-research/`
