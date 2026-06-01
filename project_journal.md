# AI Hedge Fund Roadmap – Project Journal

## Current Status
Completed: Days 1–17

---

## Days 1–7: Foundations
- Python fundamentals
- NumPy
- Pandas
- Data manipulation
- Visualization
- Financial returns basics

---

## Days 8–11: First Strategy
Built:
- SMA crossover strategy
- Buy/Hold benchmark
- Position tracking
- Proper use of `shift(1)`
- Long-only framework

Key lesson:
- Position and signal are different concepts.

---

## Days 12–15: Research Layer
Added:
- Sharpe ratio
- Exposure
- Trade statistics
- Transaction costs
- Slippage
- Stop loss
- Take profit
- Position sizing experiments

Findings:
- TP often reduced performance.
- Stop loss improved robustness.
- Random strategy behaved as expected.

---

## Day 16: Refactor
Created modular pipeline:
- load_data()
- calculate_indicators()
- generate_signals()
- run_backtest()
- calculate_metrics()
- plot_results()

Key lesson:
- Strategy != System

---

## Day 17: Multi-Asset Validation

Assets tested:
- TSLA
- AAPL
- MSFT
- BTC-USD

Findings:
- SMA strategy generally underperformed Buy & Hold.
- BTC showed the strongest Sharpe.
- Correlation:
  - BTC vs equities: low (~0.17)
  - MSFT vs AAPL: high (~0.66)

### Regime Analysis

Observed:
- Bullish regimes generally positive.
- Bearish regimes sometimes positive.
- Sideways regimes consistently weak.

Conclusion:
- Strategy appears regime-dependent.
- Sideways markets are the main weakness.

---

## Next Focus (Day 18+)

### Automatic Regime Classifier
Using:
- SMA100 slope
- Volatility
- Price relative to SMA100

Regimes:
- Bullish
- Sideways
- Bearish

Goals:
1. Validate classifier visually.
2. Compare performance by regime.
3. Test filtering sideways markets.
4. Determine whether edge exists only in specific regimes.

---

## Long-Term Roadmap

Upcoming topics:
- Regime filters
- Walk-forward validation
- Parameter search
- Portfolio construction
- Multi-asset backtesting
- Factor research
- ML-based signals (later)
- Quant research infrastructure

