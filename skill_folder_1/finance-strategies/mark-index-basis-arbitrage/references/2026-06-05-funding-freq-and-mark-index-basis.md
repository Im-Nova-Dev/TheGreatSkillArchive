# 2026-06-05 Session Detail: Funding Frequency + Mark/Index Basis

## Item 1 of 2: Perpetual Futures Funding Frequency as Execution Edge
**Category:** Execution · Microstructure · Derivatives
**Source:** MetaMask Perps Research, 2026-05-14; SEI Blog, 2026; CryptoQuant annual volume data.

### Key Rules
- Standard 8-hour windows: 00:00 / 08:00 / 16:00 UTC.
- Sub-8-hour schedules (dYdX, Coinbase): 1-hour or 4-hour funding.
- Intersection rule: if funding window closes < 15 minutes after mark/index divergence threshold breach, close or reduce size to avoid adverse funding + mark-price spike coupling.
- CRITICAL: Funding applies only to positions held open at the checkpoint timestamp.

### Actionable Use Cases
- Funding-rate calendar spread: route entries/exits to avoid negative-window payments.
- Mark-price liquidation buffer: use index, not last trade, to size margin + cushion.
- Venue-selection heuristic: choose venue whose funding offset aligns with funding-flow forecast to reduce carry cost or increase receipt.

---

## Item 2 of 2: Mark/Index Basis Arbitrage and Liquidation Buffer Scheduling
**Category:** Execution · Liquidity · Derivatives
**Source:** SEI Blog "Perpetual Futures vs. Traditional Futures," 2026; Arthur Hayes BitMEX funding rate whitepaper; exchange mark-price methodology docs (Binance aggregator cross-venue index).

### Key Rules
- Mark price = index_price + funding_rate_time_value_adjusted + moving_average_basis + liquidation_buffer.
- Index price is a volume-weighted average across 8-11 spot exchanges; mark price can diverge 0.5%-2% from index during volatility without arbitrage.
- Manipulation playbook: spoof mark price above index to force liquidations, then revert. Detect by comparing index volatility to mark volatility; a 3x ratio is a spoofing fingerprint.
- Funding frequency compounds mark/index basis: 8-hour funding with 0.01% interest rate can push mark to 0.03% quarterly annualized under stress.
- Exchange liquidation cascade threshold is typically 4.5x maintenance margin; mark price breaks index first.

### Actionable Use Cases
- Liquidation buffer sizing: use index as fair value, mark as trigger; keep margin 20-25% above minimum to avoid cascade-triggered close.
- Basis arbitrage: short perpetual when mark > index + 1.5x normal spread; cover when mark/index reverts or funding payment collected; delta hedge with spot or cross-exchange perp.
- Mark-price spike trade: enter short at mark spike, cover within 30 minutes before normalization; target 0.5%-2% capture.
- Venue routing: exotics/DEX venues with thinner OI widen mark/index spread; route heavy directional flow to venues with tight index fencing.

### Execution Checklist
1. Compute rolling 20-bar mark/index spread and classify as normal (<0.5%), elevated (0.5%-1.5%), or spike (>1.5%).
2. When normalized funding exceeds 0.3% per 8-hour interval (ER), avoid holding through window; exit 15 minutes prior.
3. Set liquidation cushion: initial margin = maintenance margin * (1 + 0.25 + max(0, (mark_index_spread - 0.005) * 10)).
4. Monitor funding window + spread joint distribution: high funding + high spread = elevated squeeze risk.

---

## Search Parameters
- Queries used: ["optimal hedging frequency derivatives transaction costs", "delta hedging frequency transaction costs trade execution", "TCA fill rate slippage execution quality benchmarks 2025 2026", "perpetual futures funding frequency strategies execution 2026", "mark price index price perpetual futures arbitrage 2026", "liquidation buffer mark index basis crypto derivatives"]
- Broadened fallbacks: ["execution algorithms TWAP VWAP Almgren-Chriss", "MEV sandwich attacks crypto arbitrage 2025 2026", "DeFi lending protocols perp hedging 2026"]
- Source types: research papers, practitioner blogs, TCA provider methodology, exchange methodology docs
