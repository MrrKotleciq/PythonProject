import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main():    
    std_treshold = 5

    data = yf.download("TSLA", start="2022-12-01", end="2025-01-01")

    data["SMA5"] = data["Close"].rolling(5).mean()
    data["SMA20"] = data["Close"].rolling(20).mean()
    data["SMA100"] = data["Close"].rolling(100).mean()
    data["Zwrot"] = data["Close"].pct_change()
    data["Zmienność"] = data["Close"].rolling(10).std()

    #print(data["Zmienność"])

    data["signal"] = np.where((data["SMA5"].shift(1) <= data["SMA20"].shift(1)) & 
                                    (data["SMA5"] > data["SMA20"]) & 
                                    (data["Close"].squeeze() > data["SMA100"]) & 
                                    (data["Zmienność"] > std_treshold), 1, 
                                    np.where((data["SMA5"].shift(1) >= data["SMA20"].shift(1)) &
                                             (data["SMA5"] < data["SMA20"]) &
                                             (data["Close"].squeeze() < data["SMA100"]) &
                                             (data["Zmienność"] > std_treshold), 0, np.nan)
                                    )
    

    data["Profit"] = np.where(data["signal"].shift(1) == 1, data["Open"].squeeze() * -1, 
                                    np.where(data["signal"].shift(1) == 0, data["Open"].squeeze(), np.nan)
                                    )


    data["Return"] = data["Zwrot"] * data["signal"].shift(1)

    data["B_Cumulative"] = (1 + data["Zwrot"]).cumprod() * 100
    data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], marker='o', label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

    '''
    plt.plot(data["SMA5"], label="SMA5")
    plt.plot(data["SMA20"], label="SMA20")
    plt.plot(data["SMA100"], label="SMA100", color="#D81D1D")
    plt.plot(data["Close"], label="Close", color="#B6F19E")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()
    '''

    #plt.plot(data["signal"], marker='o', linestyle='--')
    plt.plot(data["Profit"], marker = 'x')
    plt.show()


main()