import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
    
signal = {
    "SELL"  : -1,
    "BUY"   : 1
}  

print(signal["SELL"])
print(signal["BUY"])


def main(ticker):      

######## Constants    

    cost_per_trade = 0.002      # working cost - just for testing
#    cost_per_trade = 0.000      # (0.0%) on xtb for cash flow less then 100k euro per month
#    cost_per_trade = 0.002      # (0.2%) on xtb for cash flow grater then 100k euro per month
#    cost_per_trade = 0.001      # (0.1%) on binance

    slippage_cost = 0.0002      # simplified slippage cost

    ATR_span = 14
    stop_loss_level = 5 # [%]
    
########
    
######## ticker data - main dataframe

    data = yf.download(ticker, start="2020-12-01", end="2026-01-01")

    data["SMA5"] = data["Close"].rolling(12).mean()
    data["SMA20"] = data["Close"].rolling(25).mean()
    data["SMA100"] = data["Close"].rolling(100).mean()
    data["Zwrot"] = data["Close"].pct_change()
    data["ATR"] = (data["Close"] - data["Close"].shift(1)).abs().rolling(ATR_span).mean()
    data["volality"] = data["Close"].rolling(20).std()

########

######## Buy and Hold - data

    BH_df = pd.DataFrame()
    BH_df["Close"] = data["Close"]
    BH_df["Open"] = data["Open"]
    BH_df["Zwrot"] = data["Zwrot"]
    BH_df["signal"] = np.where(BH_df.index == BH_df.index[0], 1, 
                                np.where(BH_df.index == BH_df.index[-1], -1, 0))
    
    BH_df["position"] = get_pos_df(BH_df)

    BH_changes = BH_df["position"] != BH_df["position"].shift(1)
    BH_pos_df = BH_df[BH_changes]

    if os.path.exists("files\\BH_pos.xlsx"):
        os.remove("files\\BH_pos.xlsx")
         
    BH_pos_df.to_excel(r"files\\BH_pos.xlsx")
    
    BH_trade_log_df = create_trade_log("BH_trade_log", BH_pos_df, cost_per_trade)
    
    BH_df["Return"] = BH_df["Zwrot"] * BH_df["position"].shift(1)
    
    wyniki = []
    wyniki = append_resaults(wyniki, BH_df, BH_trade_log_df, "Buy & Hold Strategy", BH_changes, cost_per_trade + slippage_cost)
    
########

######## SMA position - data

    sma_df = pd.DataFrame()
    sma_df["Close"] = data["Close"]
    sma_df["Open"] = data["Open"]
    sma_df["Zwrot"] = data["Zwrot"]
    sma_df["signal"] = np.where((data["SMA5"].shift(1) <= data["SMA20"].shift(1)) & 
                                    (data["SMA5"] > data["SMA20"]) & 
                                    (data["Close"].squeeze() > data["SMA100"]), 1, 
                                    np.where((data["SMA5"].shift(1) >= data["SMA20"].shift(1)) &
                                             (data["SMA5"] < data["SMA20"]), -1, 0))
    
    sma_get_pos_df(sma_df, stop_loss_level)
    sma_changes = sma_df["position"] != sma_df["position"].shift(1)    
    sma_pos_df = sma_df[sma_changes].iloc[1:]
    
    if os.path.exists("files\\sma_pos.xlsx"):
        os.remove("files\\sma_pos.xlsx")
         
    sma_pos_df.to_excel(r"files\\sma_pos.xlsx")
    sma_trade_log_df = create_trade_log("SMA_trade_log", sma_pos_df, cost_per_trade)

    sma_df["Return"] = sma_df["Zwrot"] * sma_df["position"]

    wyniki = append_resaults(wyniki, sma_df, sma_trade_log_df, "SMA Strategy", sma_changes, cost_per_trade + slippage_cost)
    
########

######## random strategy data 

    r_df = pd.DataFrame()
    r_df["Close"] = data["Close"]
    r_df["Open"] = data["Open"]
    r_df["Zwrot"] = data["Zwrot"]
    r_df["signal"] = np.random.randint(-1, 2, size=len(r_df))

    r_df["position"] = get_pos_df(r_df)
    r_changes = r_df["position"] != r_df["position"].shift(1)
    r_position_df = r_df[r_changes].iloc[1:]
    
    r_df["Return"] = r_df["Zwrot"] * r_df["position"]

######## random_trade_log DataFrame

    r_trade_log_df = create_trade_log("r_s_trade_log", r_position_df, cost_per_trade)

######## Random Strategy - data

    wyniki = append_resaults(wyniki, r_df, r_trade_log_df, "Random Strategy", r_changes, cost_per_trade + slippage_cost)

########

######## wyniki

    wyniki_df = pd.DataFrame(wyniki)
    print(wyniki_df)
    
    if os.path.exists("files\\wyniki.xlsx"):
        os.remove("files\\wyniki.xlsx")
        
    wyniki_df.to_excel(r"files\wyniki.xlsx")

########

######## zapis danych do pliku
        
    if os.path.exists("files\\data.xlsx"):
        os.remove("files\\data.xlsx")
         
    data.to_excel(r"files\\data.xlsx")
    
########

######## sanity check

    # main_data_na = data.isna().sum()
    # main_data_index_check = data.sort_index() 
    
    # sma_df_na = sma_df.isna().sum()
    # sma_df_index_check = sma_df.sort_index
    # sma_pos_nan_count = sma_pos_df.isna().sum()
    # sma_pos_df_index_check = sma_pos_df.sort_index()
    
    # print(main_data_na)
    # print(main_data_index_check)
    # print(sma_df_na)
    # print(sma_df_index_check)
    # print(sma_pos_nan_count)
    # print(sma_pos_df_index_check)

########


######## wykresy

    # plt.plot(sma_df["signal"], label="Signal")
    plt.plot(BH_df["cumulative"], label="Hold")
    plt.plot(sma_df["cumulative"], label="Strategy")
    plt.plot(r_df["cumulative"], label="Random")
    # plt.plot(data["ATR"], label="ATR")

    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

#########




######## functions

def append_resaults(tab, strategy_df, s_trade_log_df, strategia: str, strategy_changes, cost):
    
    strategy_df["Return"] = np.where(strategy_changes, strategy_df["Return"] - cost, strategy_df["Return"])
    strategy_df["cumulative"] = (1 + strategy_df["Return"]).cumprod() * 100
    
    
    
    s_return = round(strategy_df["cumulative"].iloc[-1], 2)
    max_drawdown = round(strategy_df["cumulative"].min(), 2)
    peak = round(strategy_df["cumulative"].max(), 2)
    exposure = round(strategy_df["position"].mean()*100, 2)
    trades = (strategy_df["signal"] > 0).sum()
    overtrading = round(trades / len(strategy_df), 2)
    sharpe_ratio = round(strategy_df["Return"].mean()/strategy_df["Return"].std() * np.sqrt(252), 2)
   # winrate = round(s_trade_log_df["Win/Loss"].sum() / len(s_trade_log_df), 2)
    
    tab.append({
        "Strategia" : strategia,
        "Final return [%]" : s_return,
        "Sharpe" : sharpe_ratio,
        "Max Drawdown [%]" : max_drawdown,
        "Peak [%]" : peak,
        "Exposure [%]" : exposure,
        "Trades" : trades,
        "Overtrading" : overtrading,
        #"Win rate" : winrate
    })
    
    return tab

def create_trade_log(name, df, cost):
    
    tab = []
    
    for i in range(0, int(np.floor(len(df)-1)), 2):
        entry_price = df["Close"].squeeze().iloc[i]
        exit_price = df["Close"].squeeze().iloc[i+1]
        ret = round((exit_price - entry_price - (exit_price*cost + entry_price*cost)) / entry_price*100 , 2) # return with included trade cost
        
        tab.append({
            "Entry Date": df.index[i],
            "Exit Date": df.index[i+1],
            "Entry Price": round(entry_price, 5),
            "Exit Price": round(exit_price, 5),
            "PnL [%]": ret,
            "Duration": df.index[i+1] - df.index[i],
            "Win/Loss" : ret > 0,
            "Costs [%]" : 2 * cost * 100
        })
    
    tab_df = pd.DataFrame(tab)
    
    # summary = {
    #     "Entry Date": "-",
    #     "Exit Date": "-",
    #     "Entry Price": "-",
    #     "Exit Price": "-",
    #     "PnL [%]": tab_df["PnL [%]"].mean(),
    #     "Duration": tab_df["Duration"].sum(),
    #     "Win/Loss" : int(tab_df["PnL [%]"].mean() > 0),
    #     "Costs [%]" : tab_df["Costs [%]"].sum()
    # }
    
    # tab_df = pd.concat([tab_df, pd.DataFrame([summary])], ignore_index=True)
    
    tab_df.to_excel(fr"files\{name}.xlsx")
    
    return tab_df

def sma_get_pos_df(df, SL):
    
    df.loc[df.index[0], "position"] = 0
    
    entry = -1
    
    for i in range(1, len(df)):
        
        prev_pos = df.loc[df.index[i-1], "position"]
        
        if prev_pos == 1:
            # check SL/TP
                      
            if (df.loc[df.index[i-1], "Close"] < entry - entry * 0.01 * SL) or (df.loc[df.index[i-1], "signal"] == -1):
                
                df.loc[df.index[i], "position"] = 0
                entry = -1
            
            else:
                
                df.loc[df.index[i], "position"] = 1
                
        else:
            # check signal
            
            if df.loc[df.index[i-1], "signal"] == 1:
                
                df.loc[df.index[i], "position"] = 1
                entry = df.loc[df.index[i], "Open"]
                
            else:
                df.loc[df.index[i], "position"] = 0
                
    if os.path.exists("files\\test_data.xlsx"):
        os.remove("files\\test_data.xlsx")
         
    df.to_excel(r"files\\test_data.xlsx")
                
                
def get_pos_df(df):
    
    df["position"] = df["signal"].shift(1).replace({
        1: 1,
        -1: 0,
        0: np.nan
    })

    df["position"] = df["position"].ffill()
    df["position"] = df["position"].fillna(0)

    return df["position"]
    
########

os.makedirs(r"files", exist_ok=True)
main("TSLA")