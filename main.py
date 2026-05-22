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
                                    (data["Close"].squeeze() > data["SMA100"]), 1, 
                                    np.where((data["SMA5"].shift(1) >= data["SMA20"].shift(1)) &
                                             (data["SMA5"] < data["SMA20"]), -1, 0))
    
    data["position"] = data["signal"].replace({
        1: 1,
        -1: 0,
        0: np.nan
    })

    data["position"] = data["position"].ffill()
    data["position"] = data["position"].fillna(0)

    
    data["Return"] = data["Zwrot"] * data["position"].shift(1)

    data["B_Cumulative"] = (1 + data["Zwrot"]).cumprod() * 100
    data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

    strategy_return = data["S_Cumulative"].iloc[-1]
    strategy_max_drawdown = data["S_Cumulative"].min()
    strategy_peak = data["S_Cumulative"].max()
    exposure = data["position"].mean()*100
    trades = (data["signal"] > 0).sum()
    Strategy_sharpe_ratio = data["Return"].mean()/data["Return"].std() * np.sqrt(252)
    #udawany winrate "Profitable active trades"
    winrate = (data["Return"] > 0).sum() / (data["position"] > 0).sum() * 100
    
    BH_return = data["B_Cumulative"].iloc[-1]
    BH_max_drawdown = data["B_Cumulative"].min()
    BH_peak = data["B_Cumulative"].max()
    BH_sharpe_ratio = data["Zwrot"].mean()/data["Zwrot"].std() * np.sqrt(252)

    ## random area 

    data["Random_Signal"] = np.random.randint(-1, 2, size=len(data))
    data["Random_Position"] = data["Random_Signal"].replace({
        1: 1,
        -1: 0,
        0: np.nan
    })
    data["Random_Position"] = data["Random_Position"].ffill()
    data["Random_Position"] = data["Random_Position"].fillna(0)
    data["Random_Return"] = data["Zwrot"] * data["Random_Position"].shift(1)

    data["R_Cumulative"] = (1 + data["Random_Return"]).cumprod() * 100

    random_return = data["R_Cumulative"].iloc[-1]
    random_max_drawdown = data["R_Cumulative"].min()
    random_peak = data["R_Cumulative"].max()
    random_exposure = data["Random_Position"].mean() * 100
    random_trades = (data["Random_Signal"] > 0).sum()
    random_sharpe_ratio = data["Random_Return"].mean()/data["Random_Return"].std() * np.sqrt(252)
    #udawany winrate
    random_winrate = (data["Random_Return"] > 0).sum() / (data["Random_Position"] > 0).sum() * 100

    ##

    wyniki = {
        "Strategia" : ["Buy and Hold", "SMA Strategy", "Random Strategy"],
        "Final return [%]" : [BH_return, strategy_return, random_return],
        "Sharpe" : [BH_sharpe_ratio, Strategy_sharpe_ratio, random_sharpe_ratio],
        "Max Drawdown [%]" : [BH_max_drawdown, strategy_max_drawdown, random_max_drawdown],
        "Peak [%]" : [BH_peak, strategy_peak, random_peak],
        "Exposure [%]" : [100, exposure, random_exposure],
        "Trades" : [1, trades, random_trades]
    }

    sheet = pd.DataFrame(wyniki)


    print(sheet)
    print("Profitable strategy active trades: {:.2f}%".format(winrate))
    print("Profitable random strategy active trades: {:.2f}%".format(random_winrate))

    #plt.plot(data["position"], label="position")

    #plt.plot(data["Random_Signal"], label="Signal")
    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], label="Strategy")
    plt.plot(data["R_Cumulative"], label="Random")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

main()