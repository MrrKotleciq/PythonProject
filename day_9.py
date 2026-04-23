import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

strategy_data = pd.DataFrame()

tesla_data = yf.download("TSLA", start="2022-12-01", end="2024-01-01")

tesla_data["SMA5"] = tesla_data["Close"].rolling(5).mean()
tesla_data["SMA20"] = tesla_data["Close"].rolling(20).mean()
tesla_data["Zwrot"] = tesla_data["Close"].pct_change()

tesla_data["Sygnał"] = np.where(tesla_data["SMA5"] > tesla_data["SMA20"], 1, 0)
tesla_data["Return"] = tesla_data["Zwrot"] * tesla_data["Sygnał"]

tesla_data["B_Cumulative"] = (1 + tesla_data["Zwrot"]).cumprod() * 100
tesla_data["S_Cumulative"] = (1 + tesla_data["Return"]).cumprod() * 100

# Test
'''
dane = {
    "Dzień" : [1,2,3,4,5],
    "Return" : [0.10,0.10,-0.10,-0.10,-0.10]
}

test_data = pd.DataFrame(dane)

test_data["Cumulative"] = (1 + test_data["Return"]).cumprod()
'''

plt.plot(tesla_data["B_Cumulative"], label="Hold")
plt.plot(tesla_data["S_Cumulative"], label="Strategy")

plt.ylabel("Wartość")
plt.xlabel("Dzień")
plt.legend()
plt.show()

plt.plot(tesla_data["SMA5"], label="SMA5")
plt.plot(tesla_data["SMA20"], label="SMA20")

plt.ylabel("Wartość")
plt.xlabel("Dzień")
plt.legend()
plt.show()

print(tesla_data)