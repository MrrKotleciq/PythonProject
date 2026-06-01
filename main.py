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
volatility_span = 20
stop_loss_level = 5 # [%]
take_profit_level = 30000 * stop_loss_level # [%]

BH = True; R = False

param_gtid = {
    "sma_fast" : [12],
    "sma_slow" : [25],
    "sma_trend" : [100],
    "target_vol" : [0.03]
}

combinations = list(itertools.product(
    param_gtid["sma_fast"],
    param_gtid["sma_slow"],
    param_gtid["sma_trend"],
    param_gtid["target_vol"]
))

# tickers = ["TSLA", "AAPL", "BTC-USD", "MSFT"]
# dates = [["2019-01-01", "2021-06-01"],["2021-07-01", "2023-03-01"],["2015-01-01", "2017-01-01"]]

tickers = ["AAPL"]
dates = [["2019-01-01", "2025-01-01"]]

wyniki = []
corr = pd.DataFrame()

i = 1

for ticker in tickers:

    k = 1

    for data in dates:

        j = 1
        
        data = load_data(f"{ticker}", data[0], data[1])

        for sma_fast, sma_slow, sma_trend, target_vol in combinations:
        
            print(f"Ticker: {i}/{len(tickers)}, date_span: {k}/{len(dates)} combinaiton: {j}/{len(combinations)}")
            j += 1

            if sma_fast >= sma_slow or sma_slow >= sma_trend:
                continue

            os.makedirs(f"files/{ticker}", exist_ok=True)


            sma_df = get_indicators(data, ATR_span, volatility_span, sma_fast, sma_slow, sma_trend)
            
            # print(sma_df["slope"].describe())
            # print(sma_df["volatility"].describe())
            
            sma_df = get_sma_signal(sma_df, stop_loss_level, take_profit_level)
            BH_df, r_df, wyniki = run_backtest(ticker, data, sma_df, wyniki, cost_per_trade, slippage_cost, ATR_span, stop_loss_level, take_profit_level, target_vol, BH, R)

            get_regime_stats(sma_df)
            get_regime_changes(sma_df)
            plt_draw(ticker, BH_df, r_df, sma_df, BH, R)

            corr[f"{ticker}"] = sma_df["Zwrot"]

        k += 1
    i += 1

# corr_matrix = corr.corr()

# print(corr_matrix)

wyniki_df = get_resaults_df(wyniki)

trade_df = pd.DataFrame(columns=("Ticker", "Bullish", "Sideways", "Bearish"))

for i in range(0, len(wyniki_df)-3, 3):

    trade_df.loc[i, "Ticker"] = wyniki_df.loc[wyniki_df.index[i], "Ticker"]
    trade_df.loc[i, "Bullish"] = wyniki_df.loc[wyniki_df.index[i], "Sharpe"]
    trade_df.loc[i, "Sideways"] = wyniki_df.loc[wyniki_df.index[i+2], "Sharpe"]
    trade_df.loc[i, "Bearish"] = wyniki_df.loc[wyniki_df.index[i+1], "Sharpe"]

print(trade_df)