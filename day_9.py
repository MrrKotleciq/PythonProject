import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

strategy_data = pd.DataFrame()

data = yf.download("TSLA", start="2022-12-01", end="2024-01-01")

data["SMA5"] = data["Close"].rolling(5).mean()
data["SMA20"] = data["Close"].rolling(20).mean()
data["return"] = data["Close"].pct_change()

data["signal"] = np.where(data["SMA5"] > data["SMA20"], 1, 0)
data["Return"] = data["return"] * data["signal"]

data["B_Cumulative"] = (1 + data["return"]).cumprod() * 100
data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

# Test
'''
dane = {
    "Dzień" : [1,2,3,4,5],
    "Return" : [0.10,0.10,-0.10,-0.10,-0.10]
}

test_data = pd.DataFrame(dane)

test_data["Cumulative"] = (1 + test_data["Return"]).cumprod()
'''

plt.plot(data["B_Cumulative"], label="Hold")
plt.plot(data["S_Cumulative"], label="Strategy")

plt.ylabel("Wartość")
plt.xlabel("Dzień")
plt.legend()
plt.show()

plt.plot(data["SMA5"], label="SMA5")
plt.plot(data["SMA20"], label="SMA20")

plt.ylabel("Wartość")
plt.xlabel("Dzień")
plt.legend()
plt.show()

print(data)