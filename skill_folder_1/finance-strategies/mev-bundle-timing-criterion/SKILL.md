---
name: mev-bundle-timing-criterion
title: MEV Bundle Timing Criterion
description: >
  Use when constructing, debugging, or evaluating private MEV bundles on
  Ethereum L1/L2 or Solana: gas-regime gating, token approval sequencing,
  bundle sizing and atomicity, builder acceptance, timing windows, and
  earnings risk. Gated by measurable rules before submitting a bundle.
triggers:
  - MEV bundle timing
  - gas gating
  - builder acceptance
  - bundle atomicity
  - token approval sequencing
  - backrun timing
  - Jito bundle
  - Flashbots bundle
  - arb bundle
---

# MEV Bundle Timing Criterion — Ethereum/Solana Bundle Construction

## Purpose
This skill provides executable selection rules for bundle inclusion: when to submit, how to size, and when to abort. It is intended for searchers and trading-system builders who treat bundle construction as an execution decision, not a routing default.

## Core Gating Rules

### 1. Gas Regime Gating
- Compute trailing 200-block median gas price `g_200` and 10-block median `g_10`.
- Submit only when `g_10 <= 0.85 * g_200`.
- Rationale: In elevated gas markets, priority fee markup dominates arbitrage edge and can flip profit to loss after inclusion risk.

### 2. Token Approval Sequencing
- Never include a fresh `approve()` in the same bundle as the consuming swap; it is front-run by sandwich bots and REV is captured before backrun.
- Require >= 1 block confirmation for any approval used inside the bundle route.
- Pre-flight: cache approval nonce and `blockNumber` in a state map keyed by token+spender.

### 3. Bundle Sizing and Atomicity vs Legged Risk
- Atomic bundle: safer settlement, but increases mempool-profile similarity to sandwich targets.
- Legged two-leg execution with private backrun: prefer when expected MEV >= 0.25 gwei per gas unit per leg.
- Leg separation: route legs through different builders within the same slot to reduce ordering risk.

### 4. Submission Timing Window
- Submit bundles 0.5–1.5 seconds before expected block time.
- Set `maxBlockNumber` to next 3 blocks max to avoid stale bundle waste.
- Fallback to public mempool if not accepted via private channel.

### 5. Builder Acceptance Filter
- Track per-builder req/reject ratio over last 20 submissions.
- Reject bundles from builders with success rate < 70%.
- If `tx.gasLimit > 200k` or bundle contains >5 internal calls, default to public mempool to reduce censorship surface and leakage.

### 6. Arb Trigger Threshold
- Characterize DEX pair liquidity depth via reserve delta per block.
- Enter only when:
  - spread over mid > 15 bps after estimated fees, or
  - quoted AMM output minus half-tick delta exceeds minimum edge.
- Use gasless observation of reserve delta first; only bundle after threshold passes.

### 7. Solana-Specific Timing (Jito)
- Leader rotation latency decays bundle edge after ~400ms post-slot boundary.
- Cap Jito tip at <= 40% of expected arbitrage profit.
- If lead-time < 150ms, abort bundle and requeue next slot.

## Risk Controls
- Never reuse bundle transactions in next block without parameter refresh; miner-extractable secrets leak and cause reverts.
- Maintain emergency abort fallback `closeOnlyOnLast` to avoid stranded legs during gas spikes.
- Reject routes through CEX-affiliated or OFAC-sanctioned builders for risk-system compatibility.

## Verification
- Backtest bundle decisions against historical builder acceptance logs and gas price series.
- Force-run gating rules on shadow bundle feed without execution to estimate knock-down rate.
- Performance targets: submission success rate >= 80%, expected profit per accepted bundle >= 0.25 gwei/unit, gas spend <= 35% of captured MEV.
