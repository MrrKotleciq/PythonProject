import os
import pandas as pd  
from pathlib import Path

from my_fun import *

def run_backtest(ticker, data, df, wyniki, CpT, SlP, ATR_sp, SL, TP, target_volality, BH:bool, R:bool):      

######## Buy and Hold - data

    BH_df = pd.DataFrame()
    if BH:
        BH_df, wyniki = run_BH(ticker, data, ATR_sp, CpT, SlP, wyniki)
    
########

######## random strategy data 

    r_df = pd.DataFrame()
    if R:
        r_df, wyniki = run_rnd(ticker, data, ATR_sp, CpT, SlP, wyniki)

########

######## SMA position - data
    
    df["pos_size"] = get_pos_size(df, target_volality)
    sma_pos_df = get_position_df(df)

    file_path = Path(f"files/{ticker}") / "sma_pos.xlsx"
    if os.path.exists(file_path):
        os.remove(file_path)
         
    sma_pos_df.to_excel(file_path)

    sma_trade_log_df = create_trade_log("SMA_trade_log", sma_pos_df, CpT)

    df["Return"] = df["Zwrot"] * df["position"] * df["pos_size"]

    wyniki = append_resaults(ticker, wyniki, df, sma_trade_log_df, "SMA Strategy", CpT + SlP)
    
    file_path = Path(f"files/{ticker}") / "df.xlsx"
    if os.path.exists(file_path):
        os.remove(file_path)
         
    df.to_excel(file_path)
########

    return [BH_df, r_df, wyniki] 