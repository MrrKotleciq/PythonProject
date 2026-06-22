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


def plot_results(df_prices: pd.DataFrame, results_df: pd.DataFrame):
    '''
    Wykres porównujący procentową zmianę ceny (Buy & Hold)
    z wynikami strategii inwestycyjnej.
    '''
    
    plt.figure(figsize=(12, 6))
    
    # 1. Obliczanie Benchmarku (Buy & Hold)
    benchmark = (df_prices['Close'] / df_prices.loc[df_prices.index[0], 'Close'] - 1) * 100
    plt.plot(benchmark, label='Buy & Hold (Benchmark)', color='gray', alpha=0.6, linestyle='--')
    
    # 2. Wizualizacja strategii z results_df
    
    for strategy_name in results_df.columns:
        plt.plot(results_df[strategy_name], label=strategy_name, linewidth=2)
    
    plt.title(f'Wyniki Backtestu: {strategy_name} vs Benchmark', fontsize=14)
    plt.xlabel('Data')
    plt.ylabel('Zmiana Procentowa (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='black', lw=1) # Linia zero
    
    plt.tight_layout()
    plt.show()
    
    
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