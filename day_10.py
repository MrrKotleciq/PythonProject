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
                                             (tesla_data["Zmienność"] > std_treshold), 0, np.nan)
                                    )
    

    tesla_data["Profit"] = np.where(tesla_data["Sygnał"].shift(1) == 1, tesla_data["Open"].squeeze() * -1, 
                                    np.where(tesla_data["Sygnał"].shift(1) == 0, tesla_data["Open"].squeeze(), np.nan)
                                    )


    tesla_data["Return"] = tesla_data["Zwrot"] * tesla_data["Sygnał"].shift(1)

    tesla_data["B_Cumulative"] = (1 + tesla_data["Zwrot"]).cumprod() * 100
    tesla_data["S_Cumulative"] = (1 + tesla_data["Return"]).cumprod() * 100

    plt.plot(tesla_data["B_Cumulative"], label="Hold")
    plt.plot(tesla_data["S_Cumulative"], marker='o', label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

    '''
    plt.plot(tesla_data["SMA5"], label="SMA5")
    plt.plot(tesla_data["SMA20"], label="SMA20")
    plt.plot(tesla_data["SMA100"], label="SMA100", color="#D81D1D")
    plt.plot(tesla_data["Close"], label="Close", color="#B6F19E")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()
    '''

    #plt.plot(tesla_data["Sygnał"], marker='o', linestyle='--')
    plt.plot(tesla_data["Profit"], marker = 'x')
    plt.show()


main()