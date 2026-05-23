import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
def main(ticker):    
    
######## ticker data - main dataframe

    data = yf.download(ticker, start="2020-12-01", end="2026-01-01")

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
    
    if os.path.exists("files\\pos.xlsx"):
        os.remove("files\\pos.xlsx")
         
    position_df.to_excel(r"files\\pos.xlsx")
    
########

######## trade_log DataFrame

    trade_log_df = create_trade_log("strategy_trade_log", position_df)

########

######## Strategy - data

    data["Return"] = data["Zwrot"] * data["position"].shift(1)
    data["S_Cumulative"] = (1 + data["Return"]).cumprod() * 100

    strategy_return = round(data["S_Cumulative"].iloc[-1], 2)
    strategy_max_drawdown = round(data["S_Cumulative"].min(), 2)
    strategy_peak = round(data["S_Cumulative"].max(), 2)
    strategy_exposure = round(data["position"].mean()*100, 2)
    strategy_trades = (data["signal"] > 0).sum()
    strategy_overtrading = round(strategy_trades / len(data), 2)
    Strategy_sharpe_ratio = round(data["Return"].mean()/data["Return"].std() * np.sqrt(252), 2)
    strategy_winrate = trade_log_df["Win/Loss"].sum() / len(trade_log_df)
    strategy_winrate = round(strategy_winrate,2)

########

######## Buy and Hold - data

    data["B_Cumulative"] = round((1 + data["Zwrot"]).cumprod() * 100, 2)
    BH_return = round(data["B_Cumulative"].iloc[-1], 2)
    BH_max_drawdown = round(data["B_Cumulative"].min(), 2)
    BH_peak = round(data["B_Cumulative"].max(), 2)
    BH_sharpe_ratio = round(data["Zwrot"].mean()/data["Zwrot"].std() * np.sqrt(252), 2)

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

    r_changes = data["Random_Position"] != data["Random_Position"].shift(1)
    r_position_df = data[r_changes].iloc[1:]
    
    r_position_df.drop(columns=["High","Low","Volume","SMA5","SMA20","SMA100","Zwrot","Zmienność"], inplace=True)

######## random_trade_log DataFrame

    r_trade_log_df = create_trade_log("r_s_trade_log", r_position_df)

########

    random_return = round(data["R_Cumulative"].iloc[-1], 2)
    random_max_drawdown = round(data["R_Cumulative"].min(), 2)
    random_peak = round(data["R_Cumulative"].max(), 2)
    random_exposure = round(data["Random_Position"].mean() * 100, 2)
    random_trades = ((data["Random_Signal"] > 0).sum())
    random_overtrading = round(random_trades / len(data), 2)
    random_sharpe_ratio = round(data["Random_Return"].mean()/data["Random_Return"].std() * np.sqrt(252), 2)
    random_winrate = r_trade_log_df["Win/Loss"].sum() / len(r_trade_log_df)
    random_winrate = round(random_winrate, 2)

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
        "Overtrading" : ["-", strategy_overtrading, random_overtrading],
        "Win rate" : [int(data["Open"].index[0] < data["Close"].index[-1]), strategy_winrate, random_winrate]
    }

    sheet = pd.DataFrame(wyniki)
    print(sheet)
    #print("Profitable strategy active trades: {:.2f}%".format(winrate))
    #print("Profitable random strategy active trades: {:.2f}%".format(random_winrate))
    
    os.makedirs(r"files", exist_ok=True)
    sheet.to_excel(r"files\wyniki.xlsx")

########

######## zapis danych do pliku
        
    if os.path.exists("files\\data.xlsx"):
        os.remove("files\\data.xlsx")
         
    data.to_excel(r"files\\data.xlsx")
    
########


######## wykresy

    #plt.plot(data["signal"], label="Signal")
    plt.plot(data["B_Cumulative"], label="Hold")
    plt.plot(data["S_Cumulative"], label="Strategy")
    plt.plot(data["R_Cumulative"], label="Random")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

#########




######## functions

def append_resaults():
    return()

def create_trade_log(name, df):
    
    tab = []
    
    for i in range(0, int(np.floor(len(df)-1)), 2):
        entry_price = df["Open"].iloc[i].values[0]
        exit_price = df["Close"].iloc[i+1].values[0]
        ret = round((exit_price-entry_price)/entry_price*100, 2)
        
        tab.append({
            "Entry Date": df.index[i],
            "Exit Date": df.index[i+1],
            "Entry Price": round(entry_price, 5),
            "Exit Price": round(exit_price, 5),
            "PnL [%]": ret,
            "Duration": df.index[i+1] - df.index[i],
            "Win/Loss" : int(ret > 0)
        })
    
    tab_df = pd.DataFrame(tab)
    
    summary = {
        "Entry Date": "-",
        "Exit Date": "-",
        "Entry Price": "-",
        "Exit Price": "-",
        "PnL [%]": tab_df["PnL [%]"].mean(),
        "Duration": tab_df["Duration"].sum(),
        "Win/Loss" : int(tab_df["PnL [%]"].mean() > 0)
    }
    
    tab_df = pd.concat([tab_df, pd.DataFrame([summary])], ignore_index=True)
    
    tab_df.to_excel(fr"files\{name}.xlsx")
    
    return tab_df

########




main("TSLA")