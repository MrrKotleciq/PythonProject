import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np    

from back_test import *

######## Constants    

cost_per_trade = 0.002      # working cost - just for testing
# cost_per_trade = 0.000      # (0.0%) on xtb for cash flow less then 100k euro per month
# cost_per_trade = 0.002      # (0.2%) on xtb for cash flow grater then 100k euro per month
# cost_per_trade = 0.001      # (0.1%) on binance

slippage_cost = 0.0002      # simplified slippage cost

ATR_span = 14
stop_loss_level = 5 # [%]
take_profit_level = 300 * stop_loss_level # [%]
target_volality = 0.02

os.makedirs(r"files", exist_ok=True)

data = load_data("TSLA", "2020-12-01", "2026-01-01")
wyniki = []
run_backtest(data, wyniki, cost_per_trade, slippage_cost, ATR_span, stop_loss_level, take_profit_level, target_volality, BH=True, R=False)