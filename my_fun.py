import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_position(df: pd.DataFrame) -> pd.DataFrame:
    
    '''
    Zmienia sygnały (1, -1, 0) na stan pozycji (1, 0).
    
    Sygnał 1 -> wchodzimy w Long (1)
    Sygnał -1 -> wychodzimy z Long (0)
    Sygnał 0 -> zostajemy w tym, w czym byliśmy wczoraj
    '''

    df['Position'] = df['Signal'].replace({
        1: 1,
        -1 : 0,
        0 : np.nan
    })
    
    df['Position'] = df['Position'].ffill().fillna(0)
    
    return df
    
    
def get_strategy_returns(df: pd.DataFrame, strategy_name: str):
    
    '''
    Oblicza skumulowaną stopę zwrotu dla konkretnej strategii
    bez modyfikowania oryginalnego DataFrame.
    '''

    daily_returns = df['Close'].pct_change().fillna(0)
    
    # Obliczamy dzienną stopę zwrotu dla strategii
    strategy_returns = daily_returns * df['Position'] 
    
    equity_curve = (1 + strategy_returns).cumprod() - 1
    equity_curve_pct = equity_curve * 100
    
    return equity_curve_pct