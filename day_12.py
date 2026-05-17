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

    strategy_return = data["S_Cumulative"].iloc[-1]
    BH_return = data["B_Cumulative"].iloc[-1]


    print("Final strategy return: {:.2f}% \nFinal buy and hold return: {:.2f}%".format(strategy_return, BH_return))
    
    strategy_max_drawdown = data["S_Cumulative"].min()
    strategy_peak = data["S_Cumulative"].max()
    
    BH_max_drawdown = data["B_Cumulative"].min()
    BH_peak = data["B_Cumulative"].max()

    print("Max strategy drawdown: {:.2f} Max strategy peak: {:.2f}".format(strategy_max_drawdown, strategy_peak))
    print("Max Buy and Hold drawdown: {:.2f} Max B&H peak: {:.2f}".format(BH_max_drawdown, BH_peak))

    exposure = data["position"].mean()*100
    print("Exposure: {:.2f}%".format(exposure))

    trades = (data["signal"] > 0).sum()
    print("Buy signals: {}".format(trades))

    #udawany winrate
    winrate = (data["return"] > 0).sum() / (data["position"] > 0).sum()
    print("Profitable active trades: {:.2f}%".format(winrate))

    #plt.plot(data["position"], label="position")

    #plt.plot(data["signal"], label="Signal")
    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], label="Strategy")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

main()