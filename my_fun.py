import numpy as np
import pandas as pd
import os
import yfinance as yf

def append_resaults(tab, strategy_df, s_trade_log_df, strategia: str, cost):
    
    strategy_df["Return"] = np.where(strategy_df["position"] != strategy_df["position"].shift(1).fillna(0), strategy_df["Return"] - cost, strategy_df["Return"])
    strategy_df["cumulative"] = (1 + strategy_df["Return"]).cumprod() * 100
    
    
    
    s_return = round(strategy_df["cumulative"].iloc[-1], 2)
    init_capital_drawdown = round(max(100 - strategy_df["cumulative"].min(), 0), 2)
    
    peak = round(strategy_df["cumulative"].max(), 2)
    exposure = round(strategy_df["position"].mean()*100, 2)
    trades = (strategy_df["signal"] > 0).sum()
    overtrading = round(trades / len(strategy_df), 2)
    sharpe_ratio = round(strategy_df["Return"].mean()/strategy_df["Return"].std() * np.sqrt(252), 2)
    winrate = round(s_trade_log_df["Win/Loss"].sum() / len(s_trade_log_df), 2)
    
    tab.append({
        "Strategia" : strategia,
        "Final return [%]" : s_return,
        "Sharpe" : sharpe_ratio,
        "init_capital Drawdown [%]" : init_capital_drawdown,
        "Peak [%]" : peak,
        "Exposure [%]" : exposure,
        "Trades" : trades,
        "Overtrading" : overtrading,
        "Win rate" : winrate
    })
    
    return tab

def create_trade_log(name, df, cost):
    
    tab = []
    
    for i in range(0, int(np.floor(len(df)-1)), 2):
        entry_price = df.loc[df.index[i], "Close"]
        exit_price = df.loc[df.index[i+1], "Close"]
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
    
    summary = {
        "Entry Date": "-",
        "Exit Date": "-",
        "Entry Price": "-",
        "Exit Price": "-",
        "PnL [%]": tab_df["PnL [%]"].mean(),
        "Duration": tab_df["Duration"].sum(),
        "Win/Loss" : int(tab_df["PnL [%]"].mean() > 0),
        "Costs [%]" : tab_df["Costs [%]"].sum()
    }
    
    tab_df = pd.concat([tab_df, pd.DataFrame([summary])], ignore_index=True)
    
    tab_df.to_excel(fr"files\{name}.xlsx")
    
    return tab_df

def TP_SL_pos_df(df, SL, TP):
    
    signal = {
        "SELL"  : -1,
        "BUY"   : 1,
        "NO"    : 0
    }  
    
    df.loc[df.index[0], "position"] = 0
    
    entry = -1
    
    for i in range(1, len(df)):
        
        prev_pos = df.loc[df.index[i-1], "position"]
        
        if prev_pos == 1:
            # check SL/TP
            # take profit is shit rn
            if (df.loc[df.index[i-1],"Close"] < entry*(100-SL)/100) or (df.loc[df.index[i-1],"Close"] > entry*(100+TP)/100) or (df.loc[df.index[i-1],"signal"] == signal["SELL"]):
                
                df.loc[df.index[i], "position"] = 0
                entry = -1
            
            else:
                
                df.loc[df.index[i], "position"] = 1
                
        else:
            # check signal
            
            if df.loc[df.index[i-1], "signal"] == signal["BUY"]:
                
                df.loc[df.index[i], "position"] = 1
                entry = df.loc[df.index[i], "Open"]
                
            else:
                df.loc[df.index[i], "position"] = 0
                
    if os.path.exists("files\\test_data.xlsx"):
        os.remove("files\\test_data.xlsx")
         
    return df["position"]

def get_pos_size(df, target_volality):
    
    df["volality"] = df["volality"].fillna(1)
    
    for i in range(1, len(df)):
        df.loc[df.index[i], "pos_size"] = target_volality / df.loc[df.index[i-1], "volality"]
        df.loc[df.index[i], "pos_size"] = min(df.loc[df.index[i], "pos_size"], 1)

    return df["pos_size"]
                
def get_pos_df(df):
    
    df["position"] = df["signal"].shift(1).replace({
        1: 1,
        -1: 0,
        0: np.nan
    })

    df["position"] = df["position"].ffill()
    df["position"] = df["position"].fillna(0)

    return df["position"]
    
def load_data(ticker:str, start, end):
    
    df = yf.download(ticker, start, end, multi_level_index=False)
    
    return df
    
def get_indicators(base_df, ATR_span:int, volality_span:int, S1:int, S2:int, S3:int):
    
    df = pd.DataFrame(base_df)
    
    df["Zwrot"] = df["Close"].pct_change()
    df["SMA1"] = df["Close"].rolling(S1).mean()
    df["SMA2"] = df["Close"].rolling(S2).mean()
    df["SMA3"] = df["Close"].rolling(S3).mean()
    
    df["ATR"] = (df["Close"] - df["Close"].shift(1)).abs().rolling(ATR_span).mean()
    df["volality"] = df["Zwrot"].rolling(volality_span).std()
    
    df["Zwrot"] = df["Zwrot"].fillna(0)
    df["ATR"] = df["ATR"].fillna(0)
    df["volality"] = df["volality"].fillna(1)
    
    #print(df)
    
    return df

def get_sma_signal(df, SL, TP):
    
    signal = {
        "SELL"  : -1,
        "BUY"   : 1,
        "NAN"    : 0
    } 
    
    df["signal"] = np.where((df["SMA1"].shift(1) <= df["SMA2"].shift(1)) & 
                                    (df["SMA1"] > df["SMA2"]) & 
                                    (df["Close"].squeeze() > df["SMA3"]), signal["BUY"], 
                                    np.where((df["SMA1"].shift(1) >= df["SMA2"].shift(1)) &
                                             (df["SMA1"] < df["SMA2"]), signal["SELL"], signal["NAN"]))
    
    df["position"] = TP_SL_pos_df(df, SL, TP)

    return df

def run_BH(data, ATR_span:int, CpT:float, SlC:float, wyniki): # CpT - cost per trade, SlC - slippage cost
    BH_df = get_indicators(data, ATR_span, 20, 12, 25, 100)
    BH_df["signal"] = np.where(BH_df.index == BH_df.index[0], 1, 
                                np.where(BH_df.index == BH_df.index[-2], -1, 0))
    
    BH_df["position"] = get_pos_df(BH_df)

    BH_pos_df = get_position_df(BH_df)

    if os.path.exists("files\\BH_pos.xlsx"):
        os.remove("files\\BH_pos.xlsx")
         
    BH_pos_df.to_excel(r"files\\BH_pos.xlsx")
    
    BH_trade_log_df = create_trade_log("BH_trade_log", BH_pos_df, CpT)
    
    BH_df["Return"] = BH_df["Zwrot"] * BH_df["position"].shift(1)
    BH_df["Return"] = BH_df["Return"].fillna(0)
    
    wyniki = append_resaults(wyniki, BH_df, BH_trade_log_df, "Buy & Hold Strategy", CpT + SlC)
    
    if os.path.exists("files\\BH_df.xlsx"):
        os.remove("files\\BH_df.xlsx")
         
    BH_df.to_excel(r"files\\BH_df.xlsx")
    
    return [BH_df, wyniki]

def run_rnd(data, ATR_span:int, CpT:float, SlC:float, wyniki):
    
    r_df = get_indicators(data, ATR_span, 20, 12, 25, 100)
    r_df["signal"] = np.random.randint(-1, 2, size=len(r_df))

    r_df["position"] = get_pos_df(r_df)
    r_changes = r_df["position"] != r_df["position"].shift(1)
    r_position_df = r_df[r_changes].iloc[1:]
    
    r_df["Return"] = r_df["Zwrot"] * r_df["position"]

    r_trade_log_df = create_trade_log("r_s_trade_log", r_position_df, CpT)

    wyniki = append_resaults(wyniki, r_df, r_trade_log_df, "Random Strategy", CpT + SlC)
    
    return [r_df, wyniki]

def get_position_df(df):
    changes = df["position"] != df["position"].shift(1).fillna(0)   
    pos_df = df[changes]
    
    return pos_df