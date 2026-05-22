# 13.0.0

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main():    
    
######## ticker data - main dataframe

    data = yf.download("TSLA", start="2022-12-01", end="2025-01-01")

    data["SMA5"] = data["Close"].rolling(5).mean()
    data["SMA20"] = data["Close"].rolling(20).mean()
    data["SMA100"] = data["Close"].rolling(100).mean()
    data["Zwrot"] = data["Close"].pct_change()
    data["Zmienność"] = data["Close"].rolling(10).std()

########

######## position - data

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
    
    changes = data["position"] != data["position"].shift(1)
    position_df = data[changes].iloc[1:]
    
    position_df.drop(columns=["High","Low","Volume","SMA5","SMA20","SMA100","Zwrot","Zmienność"], inplace=True)
    
    #print(position_df)
    
    if os.path.exists("files\pos.xlsx"):
        os.remove("files\pos.xlsx")
         
    position_df.to_excel(r"files\pos.xlsx")
    
########

######## trade_log DataFrame

    trades_table = []
    
    for i in range(0, int(np.floor(len(position_df)-1)), 2):
        entry_price = position_df["Open"].iloc[i].values[0]
        exit_price = position_df["Close"].iloc[i+1].values[0]
        ret = round((exit_price-entry_price)/entry_price*100, 2)
        
        trades_table.append({
            "Entry Date": position_df.index[i],
            "Exit Date": position_df.index[i+1],
            "Entry Price": round(entry_price, 5),
            "Exit Price": round(exit_price, 5),
            "Return": f"{ret}%",
            "Duration": position_df.index[i+1] - position_df.index[i],
            "Win/Loss" : int(ret > 0)
        })
    
    trade_log_df = pd.DataFrame(trades_table)
    trade_log_df.to_excel(r"files\trade_logs.xlsx")
    print(trade_log_df)

########

######## Strategy - data

    data["Return"] = data["Zwrot"] * data["position"].shift(1)
    data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

    strategy_return = data["S_Cumulative"].iloc[-1]
    strategy_max_drawdown = data["S_Cumulative"].min()
    strategy_peak = data["S_Cumulative"].max()
    strategy_exposure = data["position"].mean()*100
    strategy_trades = (data["signal"] > 0).sum()
    strategy_overtrading = strategy_trades / len(data)
    Strategy_sharpe_ratio = data["Return"].mean()/data["Return"].std() * np.sqrt(252)
    
    winrate = (data["Return"] > 0).sum() / (data["position"] > 0).sum() * 100 # udawany winrate - "Profitable active trades"

########

######## Buy and Hold - data

    data["B_Cumulative"] = (1 + data["Zwrot"]).cumprod() * 100
    BH_return = data["B_Cumulative"].iloc[-1]
    BH_max_drawdown = data["B_Cumulative"].min()
    BH_peak = data["B_Cumulative"].max()
    BH_sharpe_ratio = data["Zwrot"].mean()/data["Zwrot"].std() * np.sqrt(252)

########

######## random strategy data 

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
    random_overtrading = random_trades / len(data)
    random_sharpe_ratio = data["Random_Return"].mean()/data["Random_Return"].std() * np.sqrt(252)
    #udawany winrate
    random_winrate = (data["Random_Return"] > 0).sum() / (data["Random_Position"] > 0).sum() * 100

########

######## wyniki

    wyniki = {
        "Strategia" : ["Buy and Hold", "SMA Strategy", "Random Strategy"],
        "Final return [%]" : [BH_return, strategy_return, random_return],
        "Sharpe" : [BH_sharpe_ratio, Strategy_sharpe_ratio, random_sharpe_ratio],
        "Max Drawdown [%]" : [BH_max_drawdown, strategy_max_drawdown, random_max_drawdown],
        "Peak [%]" : [BH_peak, strategy_peak, random_peak],
        "Exposure [%]" : [100, strategy_exposure, random_exposure],
        "Trades" : [1, strategy_trades, random_trades],
        "Overtrading" : ["-", strategy_overtrading, random_overtrading]
    }

    sheet = pd.DataFrame(wyniki)
    print(sheet)
    print("Profitable strategy active trades: {:.2f}%".format(winrate))
    print("Profitable random strategy active trades: {:.2f}%".format(random_winrate))
    
    os.makedirs(r"files", exist_ok=True)
    sheet.to_excel(r"files\wyniki.xlsx")

########

######## zapis danych do pliku
        
    if os.path.exists("files\data.xlsx"):
        os.remove("files\data.xlsx")
         
    data.to_excel(r"files\data.xlsx")
    
########


######## wykresy

    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], label="Strategy")
    plt.plot(data["R_Cumulative"], label="Random")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

#########

main()