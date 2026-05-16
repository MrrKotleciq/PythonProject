import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main():    
    std_treshold = 5

    tesla_data = yf.download("SABR", period="1y", interval="4h")

    tesla_data["SMA5"] = tesla_data["Close"].rolling(5).mean()
    tesla_data["SMA20"] = tesla_data["Close"].rolling(20).mean()
    tesla_data["SMA100"] = tesla_data["Close"].rolling(100).mean()
    tesla_data["Zwrot"] = tesla_data["Close"].pct_change()
    tesla_data["Zmienność"] = tesla_data["Close"].rolling(10).std()

    #print(tesla_data["Zmienność"])

    tesla_data["Sygnał"] = np.where((tesla_data["SMA5"].shift(1) <= tesla_data["SMA20"].shift(1)) & 
                                    (tesla_data["SMA5"] > tesla_data["SMA20"]) & 
                                    (tesla_data["Close"].squeeze() > tesla_data["SMA100"]), 1, 
                                    np.where((tesla_data["SMA5"].shift(1) >= tesla_data["SMA20"].shift(1)) &
                                             (tesla_data["SMA5"] < tesla_data["SMA20"]), -1, 0)
                                    )
    
    tesla_data["Pozycja"] = tesla_data["Sygnał"].replace({
        1: 1,
        -1: 0,
        0: np.nan
    })

    tesla_data["Pozycja"] = tesla_data["Pozycja"].ffill()
    tesla_data["Pozycja"] = tesla_data["Pozycja"].fillna(0)

    
    tesla_data["Return"] = tesla_data["Zwrot"] * tesla_data["Pozycja"].shift(1)

    tesla_data["B_Cumulative"] = (1 + tesla_data["Zwrot"]).cumprod() * 100
    tesla_data["S_Cumulative"] = (1 + tesla_data["Return"]).cumprod() * 100

    #plt.plot(tesla_data["Pozycja"], label="Pozycja")

    plt.plot(tesla_data["B_Cumulative"], label="Hold")
    plt.plot(tesla_data["S_Cumulative"], label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

main()