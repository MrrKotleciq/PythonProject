import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = yf.download("TSLA", start="2020-12-01", end="2026-01-01")

print(data)

data.loc[data.index[0], "test_signal"] = 0
for i in range(0, len(data)-1):
    
    if data.index[i, "Close"] < data.index[i-1, "Close"]:
        data.index[i, "test_signal"] = 0
    else:        
        data.index[i, "test_signal"] = 1
        
print(data)