import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main():    
    std_treshold = 5

    tesla_data = yf.download("TSLA", start="2022-12-01", end="2025-01-01")

    tesla_data["SMA5"] = tesla_data["Close"].rolling(5).mean()
    tesla_data["SMA20"] = tesla_data["Close"].rolling(20).mean()
    tesla_data["SMA100"] = tesla_data["Close"].rolling(100).mean()
    tesla_data["Zwrot"] = tesla_data["Close"].pct_change()
    tesla_data["Zmienność"] = tesla_data["Close"].rolling(10).std()

    #print(tesla_data["Zmienność"])

    tesla_data["Sygnał"] = np.where((tesla_data["SMA5"].shift(1) <= tesla_data["SMA20"].shift(1)) & 
                                    (tesla_data["SMA5"] > tesla_data["SMA20"]) & 
                                    (tesla_data["Close"].squeeze() > tesla_data["SMA100"]) & 
                                    (tesla_data["Zmienność"] > std_treshold), 1, 
                                    np.where((tesla_data["SMA5"].shift(1) >= tesla_data["SMA20"].shift(1)) &
                                             (tesla_data["SMA5"] < tesla_data["SMA20"]) &
                                             (tesla_data["Close"].squeeze() < tesla_data["SMA100"]) &
                                             (tesla_data["Zmienność"] > std_treshold), -1, 0)
                                    )
    akcje = tesla_data["Sygnał"].sum()
    
    tesla_data.iloc[-2, tesla_data.columns.get_loc("Sygnał")] = -1 
    

    tesla_data["Zmienność"] = np.where(tesla_data["Sygnał"].shift(1) == 1, tesla_data["Open"].squeeze() * -1, 
                                    np.where(tesla_data["Sygnał"].shift(1) == -1, tesla_data["Open"].squeeze(), 0)
                                    )

    tesla_data.iloc[-1, tesla_data.columns.get_loc("Zmienność")] *= akcje
  

    tesla_data["Profit"] = tesla_data["Zmienność"].cumsum()

    print(tesla_data["Profit"])

    tesla_data["Return"] = tesla_data["Zwrot"] * tesla_data["Sygnał"].shift(1)

    tesla_data["S_Cumulative"] = (1 + tesla_data["Return"]).cumprod() * 100

    tesla_data["Peak"] = tesla_data["S_Cumulative"].cummax()
    tesla_data["Drawdown"] = (tesla_data["S_Cumulative"] - tesla_data["Peak"]) / tesla_data["Peak"]

    fig, axs = plt.subplots(2)
    fig.suptitle('data')

    axs[0].plot(tesla_data["Close"], label="Hold")
    axs[0].plot(tesla_data["Profit"], label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()

    axs[1].plot(tesla_data["Sygnał"], linestyle='--')
    plt.show()

    print(tesla_data["Peak"])

main()