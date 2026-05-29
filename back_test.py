import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np    

from my_fun import *

def run_backtest(data, wyniki, CpT, SlP, ATR_sp, SL, TP, target_volality, BH:bool, R:bool):      

######## Buy and Hold - data

    if BH:
        BH_df, wyniki = run_BH(data, ATR_sp, CpT, SlP, wyniki)
    
########

######## random strategy data 

    if R:
        r_df, wyniki = run_rnd(data, ATR_sp, CpT, SlP, wyniki)

########

######## SMA position - data
   
    sma_df = get_indicators(data, ATR_sp, 20, 12, 25, 100)
    
    sma_df = get_sma_signal(sma_df, SL, TP)
    
    sma_df["pos_size"] = get_pos_size(sma_df, target_volality)
    sma_pos_df = get_position_df(sma_df)
    
    
    if os.path.exists("files\\sma_pos.xlsx"):
        os.remove("files\\sma_pos.xlsx")
         
    sma_pos_df.to_excel(r"files\\sma_pos.xlsx")
    sma_trade_log_df = create_trade_log("SMA_trade_log", sma_pos_df, CpT)

    sma_df["Return"] = sma_df["Zwrot"] * sma_df["position"] #* sma_df["pos_size"]

    wyniki = append_resaults(wyniki, sma_df, sma_trade_log_df, "SMA Strategy", CpT + SlP)
    
    if os.path.exists("files\\sma_df.xlsx"):
        os.remove("files\\sma_df.xlsx")
         
    sma_df.to_excel(r"files\\sma_df.xlsx")
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

    if BH:
        plt.plot(BH_df["cumulative"], label="Hold")
    if R:
        plt.plot(r_df["cumulative"], label="Random")
    
    plt.plot(sma_df["cumulative"], label="Strategy")


    plt.ylabel("Wartość")
    plt.xlabel("Dzień")
    plt.legend()
    plt.show()

#########
