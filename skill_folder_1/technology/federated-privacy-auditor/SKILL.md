---
name: federated-privacy-auditor
description: "Audit federated learning systems for privacy leakage and membership inference."
version: 1.0.0
category: technology
tags: ["federated-learning", "privacy", "membership-inference", "differential-privacy", "security-audit"]
related_skills: ["mlops/evaluation", "technology/federated-learning-aggregator", "technology/cybersecurity-threat-cove"]
---

# Federated Privacy Auditor

## Overview

Comprehensive audit framework for evaluating privacy guarantees in federated learning systems. Covers membership inference attacks, model inversion, attribute inference, differential privacy validation, and secure aggregation verification.

## When To Use

- Auditing a federated learning deployment before production release
- Validating differential privacy (DP) parameter configurations (ε, δ)
- Testing for membership inference vulnerability in client models
- Verifying secure aggregation protocol implementations
- Compliance review for GDPR, HIPAA, or sector-specific regulations
- Red-teaming FL systems as part of a security assessment

## Core Threat Models

### Membership Inference Attacks (MIA)
- **Shadow model attacks**: Train shadow models on synthetic/auxiliary data to mimic target behavior
- **Metric-based attacks**: Use loss, confidence, or entropy thresholds to distinguish members
- **Label-only attacks**: Work with only predicted labels (hard labels), no confidence scores
- **Blind attacks**: Attacker has no auxiliary data, only query access to the global model

### Model Inversion & Attribute Inference
- **Model inversion**: Reconstruct training samples from model gradients/parameters
- **Attribute inference**: Infer sensitive attributes (demographics, health status) not in the target label
- **Gradient leakage**: Recover data from shared gradients (even with DP noise)

### Aggregation-Time Attacks
- **Poisoning for privacy amplification**: Malicious clients craft updates to amplify leakage
- **Secure aggregation bypass**: Exploit implementation flaws in SAA (Secure Aggregation Additive)
- **Dropout/partial participation**: Target clients that drop out to isolate their updates

## Audit Workflow

### Phase 1: System Mapping
1. **Inventory components**: Client selection, aggregation server, communication protocol, DP mechanism
2. **Document threat boundaries**: Trusted vs. untrusted parties, honest-but-curious vs. malicious
3. **Capture data flow**: Raw data → local training → gradient/update → aggregation → global model

### Phase 2: Configuration Review
1. **DP parameters**: Verify ε (privacy budget), δ (failure probability), noise scale (Gaussian/Laplace), clipping norm
2. **Secure aggregation**: Check threshold (t/n), dropout handling, replay protection
3. **Client sampling**: Fraction per round, replacement strategy, minimum cohort size
4. **Model architecture**: Overparameterization increases memorization risk

### Phase 3: Empirical Testing
1. **Membership inference benchmark**:
   - Train shadow models on public/auxiliary data matching distribution
   - Attack queries: global model, client models (if accessible), intermediate updates
   - Metrics: AUC, precision@recall, advantage over random guessing
   - Baseline: Compare against non-FL centralized training

2. **Model inversion benchmark**:
   - Gradient leakage: Use DLG, iDLG, or Geiping et al. attacks on shared gradients
   - Reconstruction quality: PSNR, SSIM, perceptual metrics for images; token accuracy for text
   - Test with varying DP noise levels and clipping thresholds

3. **Attribute inference benchmark**:
   - Train auxiliary classifiers on public data for sensitive attributes
   - Measure inference advantage on target model outputs

### Phase 4: Aggregation Security Testing
1. **Secure aggregation protocol review**: Verify SAA implementation against spec (Bell et al. 2020 / Bonawitz et al. 2017)
2. **Dropout attack simulation**: Remove subsets of clients, measure information leakage
3. **Replay/forge resistance**: Test if malformed updates can bypass verification

### Phase 5: Reporting & Remediation
1. **Privacy budget accounting**: RDP accountant or moments accountant for composition
2. **Attack success rates**: Per attack type, per DP configuration
3. **Recommendations**: Adjust ε, increase clipping, add local DP, modify sampling
4. **Retest after mitigation**: Verify fixes reduce attack success to acceptable threshold

## Tooling & Frameworks

| Category | Tools |
|----------|-------|
| FL Simulation | Flower, PySyft, TensorFlow Federated, FATE, OpenFL |
| DP Accounting | Opacus, TensorFlow Privacy, PyTorch DP, AutoDP |
| MIA Benchmarks | `mli` (Membership Inference Library), `privacy-meter`, custom shadow training |
| Gradient Inversion | `grad-leak` (Geiping et al.), `deep-leakage` (DLG/iDLG) |
| Secure Aggregation | `pysodium`/`lib sodium` for SAA, `MP-SPDZ` for MPC-based |

## Key References

- **Membership Inference**: Shokri et al. "Membership Inference Attacks Against Machine Learning Models" (S&P 2017)
- **FL Privacy**: Nasr et al. "Comprehensive Privacy Analysis of Deep Learning" (IEEE S&P 2019)
- **Gradient Leakage**: Zhu et al. "Deep Leakage from Gradients" (NeurIPS 2019); Geiping et al. "Inverting Gradients" (ICML 2020)
- **FL-Specific MIA**: Melis et al. "Exploiting Unintended Feature Leakage in Collaborative Learning" (USENIX 2019)
- **Secure Aggregation**: Bonawitz et al. "Practical Secure Aggregation for Privacy-Preserving ML" (CCS 2017)
- **DP in FL**: McMahan et al. "Learning Differentially Private Recurrent Language Models" (ICLR 2018)
- **RDP Accounting**: Mironov "Rényi Differential Privacy" (CSF 2017)

## Example Usage

```bash
# Quick MIA check on a Flower FL system
python -m privacy_meter.audit \
  --framework flower \
  --config federation_config.yaml \
  --attack membership_inference \
  --shadow_data public_dataset \
  --rounds 100 \
  --output mia_report.json

# Gradient inversion test on client update
python -m grad_leak.test \
  --global-model global.pt \
  --client-update client_3_update.pt \
  --dp-noise 1.0 \
  --clipping 1.0 \
  --architecture resnet18

# DP budget accounting for composition
python -m opacus.accountants.rdp \
  --noise-multiplier 1.3 \
  --sample-rate 0.01 \
  --steps 5000 \
  --delta 1e-5
```

## Verification Steps

After running audits, verify:
- [ ] MIA AUC ≤ 0.55 (near-random) for all attack variants tested
- [ ] Gradient inversion PSNR < 20dB (unrecognizable) with production DP settings
- [ ] Attribute inference advantage < 0.1 over random
- [ ] RDP accountant ε matches declared privacy budget after T rounds
- [ ] Secure aggregation threshold holds under simulated dropout (t-of-n)
- [ ] No client-side data persists in logs, checkpoints, or shared artifacts

## References

See `references/` directory for:
- `mia-benchmark-methodology.md` — Detailed MIA benchmark protocols
- `dp-accounting-guide.md` — RDP vs. moments accountant comparison
- `secure-aggregation-checklist.md` — Protocol verification checklist
- `attack-implementations/` — Reference attack scripts for testing