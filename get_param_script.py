import os  
import itertools

from back_test import *

######## Constants    

cost_per_trade = 0.002      # working cost - just for testing
# cost_per_trade = 0.000      # (0.0%) on xtb for cash flow less then 100k euro per month
# cost_per_trade = 0.002      # (0.2%) on xtb for cash flow grater then 100k euro per month
# cost_per_trade = 0.001      # (0.1%) on binance

slippage_cost = 0.0002      # simplified slippage cost

ATR_span = 14
volality_span = 20
stop_loss_level = 5 # [%]
take_profit_level = 30000 * stop_loss_level # [%]

BH = True
R = False

param_gtid = {
    "sma_fast" : [5, 12, 20, 50],
    "sma_slow" : [25, 50, 100, 150],
    "sma_trend" : [100, 150, 250, 300],
    "target_vol" : [0.01, 0.02, 0.03, 0.04]
}

combinations = list(itertools.product(
    param_gtid["sma_fast"],
    param_gtid["sma_slow"],
    param_gtid["sma_trend"],
    param_gtid["target_vol"]
))

tickers = ["TSLA", "AAPL", "BTC-USD", "MSFT"]
wyniki = []

i = 1

for ticker in tickers:

    j = 1
    print(f"{i}/{len(tickers)}")
    i += 1
    
    data = load_data(f"{ticker}", "2015-01-01", "2026-01-01")

    for sma_fast, sma_slow, sma_trend, target_vol in combinations:
    
        print(f"{j}/{len(combinations)}")
        j += 1

        if sma_fast >= sma_slow or sma_slow >= sma_trend:
            continue

        os.makedirs(f"files/{ticker}", exist_ok=True)


        sma_df = get_indicators(data, ATR_span, volality_span, sma_fast, sma_slow, sma_trend)
        sma_df = get_sma_signal(sma_df, stop_loss_level, take_profit_level)
        BH_df, r_df, wyniki = run_backtest(ticker, data, sma_df, wyniki, cost_per_trade, slippage_cost, ATR_span, stop_loss_level, take_profit_level, target_vol, BH, R)

        # plt_draw(ticker, BH_df, r_df, sma_df, BH, R)

        wyniki.append({
            "fast" : sma_fast,
            "slow" : sma_slow,
            "trend": sma_trend,
            "target_vol" : target_vol
        })

wyniki_df = get_resaults_df(wyniki)