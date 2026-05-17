import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main():    
    std_treshold = 5

    data = yf.download("SABR", period="1y", interval="4h")

    data["SMA5"] = data["Close"].rolling(5).mean()
    data["SMA20"] = data["Close"].rolling(20).mean()
    data["SMA100"] = data["Close"].rolling(100).mean()
    data["return"] = data["Close"].pct_change()
    data["Zmienność"] = data["Close"].rolling(10).std()

    #print(data["Zmienność"])

    data["signal"] = np.where((data["SMA5"].shift(1) <= data["SMA20"].shift(1)) & 
                                    (data["SMA5"] > data["SMA20"]) & 
                                    (data["Close"].squeeze() > data["SMA100"]), 1, 
                                    np.where((data["SMA5"].shift(1) >= data["SMA20"].shift(1)) &
                                             (data["SMA5"] < data["SMA20"]), -1, 0)
                                    )
    
    data["position"] = data["signal"].replace({
        1: 1,
        -1: 0,
        0: np.nan
    })

    data["position"] = data["position"].ffill()
    data["position"] = data["position"].fillna(0)

    
    data["Return"] = data["return"] * data["position"].shift(1)

    data["B_Cumulative"] = (1 + data["return"]).cumprod() * 100
    data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

    #plt.plot(data["position"], label="position")

    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

main()