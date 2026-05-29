import os  

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
take_profit_level = 300 * stop_loss_level # [%]
target_volality = 0.02
S1 = 12
S2 = 25
S3 = 100


BH = True
R = False

tickers = ["TSLA", "AAPL", "BTC-USD"]
wyniki = []

for ticker in tickers:

    os.makedirs(f"files/{ticker}", exist_ok=True)

    data = load_data(f"{ticker}", "2020-12-01", "2026-01-01")

    sma_df = get_indicators(data, ATR_span, volality_span, S1, S2, S3)
    sma_df = get_sma_signal(sma_df, stop_loss_level, take_profit_level)
    BH_df, r_df, wyniki = run_backtest(ticker, data, sma_df, wyniki, cost_per_trade, slippage_cost, ATR_span, stop_loss_level, take_profit_level, target_volality, BH, R)

    plt_draw(ticker, BH_df, r_df, sma_df, BH, R)

wyniki_df = get_resaults_df(wyniki)