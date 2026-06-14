# Funding-Rate Mean Reversion — Crypto Perpetual Swaps
- Author: hermes scheduled
- Version: 0.1
- Category: finance-strategies/crypto/derivatives

## Concept
Perpetual swaps price funding payments that oscillate around zero. When leverage build-up creates extreme skew, funding rates depart from long-run mean and revert. That creates short-horizon mean-reversion opportunity independent of spot trend.

## Quant Logic
1. Compute rolling mean `mu` and std `sigma` of funding rate over last 30 intervals.
2. Compute normalized rate `z = (r - mu) / sigma`.
3. Signal threshold: `abs(z) >= 2`.
4. Position sizing: size inversely proportional to |z| and position hold time scaled by remaining funding intervals.
5. Exit: when `z` returns to zero band or when mark-to-spot basis compresses.

## Two-Tier Execution Criterion (Zhivkov 2026)
- Only take spread >= 20 bps between two exchanges.
- Weight toward CEX leg as lead exchange and avoid DEX-only spreads unless CEX and DEX rate move in same direction with zero reverse causality detected in 4h window.
- Impose cost floor: if transaction costs >= 40% of expected spread, skip.
- Hard stop: if spread persists past 95th-percentile historical convergence window, flatten.

## Data Sources
- `/fundingRate` and `/markPrice` endpoints from Binance/OKX/Bybit.
- `/openInterestHist` for OI direction filter.

## Verification
- Backtest on 1-hour bars for BTC/ETH USD-Margined perpetuals.
- Filters: no entries during scheduled exchange maintenance, outliers flagged by exchange.
- Performance targets: win rate 57–62%, max drawdown <= 15%, Sharpe >= 1.2.
