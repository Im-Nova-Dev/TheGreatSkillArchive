# Membership Inference Attack Benchmark Methodology

## Overview
Standardized protocol for evaluating MIA resistance in federated learning systems.

## Attack Taxonomy

### 1. Shadow Model Attacks (Shokri et al. 2017)
- **Assumption**: Attacker has auxiliary data from same distribution
- **Procedure**: Train N shadow models on disjoint auxiliary subsets, train attack classifier on shadow model outputs
- **Target**: Global model, client models, or intermediate updates

### 2. Metric-Based Attacks (Yeom et al. 2018)
- **Assumption**: No auxiliary data needed
- **Features**: Loss, confidence, entropy, prediction margin
- **Threshold**: Calibrate on held-out member/non-member data

### 3. Label-Only Attacks (Li & Zhang 2021)
- **Assumption**: Only hard labels accessible (no confidence scores)
- **Method**: Use prediction correctness + label frequency statistics

### 4. Blind Attacks (Sablayrolles et al. 2019)
- **Assumption**: No auxiliary data, only query access
- **Method**: Use memorization metrics (e.g., influence functions)

## FL-Specific Considerations

### Attack Surfaces
1. **Global model**: Standard MIA after aggregation
2. **Client models**: Local models before aggregation (if accessible)
3. **Intermediate updates**: Gradients/model deltas sent to server
4. **Secure aggregation output**: Aggregated result before noise addition

### Client Sampling Effects
- Partial participation reduces attack effectiveness (fewer exposed clients)
- But increases variance in attack success estimation
- Stratified sampling by data distribution matters

## Benchmark Protocol

### Dataset Splits
```
Member Set:      D_train (used in FL training)
Non-Member Set:  D_test (held-out, same distribution)
Auxiliary Set:   D_aux (for shadow training, can overlap with D_test)
```

### Shadow Training
- Train K shadow models on disjoint D_aux subsets
- Match FL architecture, local epochs, optimizer
- Record (output, label) for member/non-member queries

### Attack Classifier
- Input: Model output (logits/softmax) + true label
- Architecture: MLP or GBM (XGBoost/LightGBM)
- Training: Balanced member/non-member from shadow outputs
- Evaluation: AUC, Precision@Recall=0.5, TPR@FPR=0.01

### Metrics to Report
| Metric | Target | Notes |
|--------|--------|-------|
| AUC | ≤ 0.55 | Near random |
| Advantage | ≤ 0.1 | Over random guessing |
| TPR@1% FPR | ≤ 0.05 | Low false positive regime |
| Precision@50% Recall | ≤ 0.55 | Precision at moderate recall |

## FL Configuration Variations to Test

| Parameter | Values | Expected Effect |
|-----------|--------|-----------------|
| DP noise (σ) | 0, 0.5, 1.0, 2.0 | Higher σ → lower AUC |
| Clipping norm (C) | 0.1, 1.0, 5.0 | Lower C → lower AUC |
| Client fraction | 0.01, 0.1, 0.5, 1.0 | Lower fraction → lower AUC |
| Local epochs | 1, 5, 10, 20 | More epochs → higher AUC |
| DP location | Client vs Server | Client DP stronger |

## Baseline Comparison
Always compare against:
1. Centralized training with same DP (sanity check)
2. No-DP FL (upper bound on vulnerability)

## Automation Script
See `scripts/run_mia_benchmark.py` for automated execution.