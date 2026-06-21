import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Optional

class IndicatorLibrary:
    
    '''Klasa odpowiedzialna za obliczenia techniczne i klasyfikację rynku.'''
    
    def __init__(self, default_sma_periods: Optional[Dict[str, int]] = None, atr_period: int = 14, slope_period: int = 20):
        self.default_sma_periods = default_sma_periods or {
            'short' : 14,
            'mid' : 30,
            'long' : 150,
            'slope_sma' : 100
        }
        self.atr_period = atr_period
        self.column_mapping = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Indicators")
    
    def add_sma(self, df: pd.DataFrame, period: int, label: str = "SMA") -> pd.DataFrame:
        
        '''
        Generyczna metoda dodawania SMA.
        label pozwala na nazywanie kolumn np. 'SMA_short' lub 'SMA_20'.
        '''
        
        column_name = f"{label}_{period}"
        df[column_name] = df['Close'].rolling(window=period).mean()
        
        self.column_mapping[label] = column_name
        
        return df
    
    
    def add_atr(self, df: pd.DataFrame, period: Optional[int] = None) -> pd.DataFrame:
        
        '''Dodaje Average True Range (ATR) do DataFrame.'''
        
        p = period if period else self.atr_period
        high_low = df['High'] - df['Low']
        high_cp = np.abs(df['High'] - df['Close'].shift())
        low_cp = np.abs(df['Low'] - df['Close'].shift())
        
        tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=p).mean()
        return df
    
    
    def add_slope(self, df: pd.DataFrame, label: str, period: int = 5) -> pd.DataFrame:
        
        '''Dodaje slope do DataFrame'''
        
        col_name = self.column_mapping.get(label)
        
        if col_name is None:
            raise KeyError(f"Nie nzaleziono wskaźnika z etykietą '{label}'. \nUpewnij się, że najpierw wywołałeś add_sma z tą etykietą")
        
        df['Slope'] = df[col_name].pct_change(period).ffill()
        
        return df
    
      
    def classify_regimes(self, df: pd.DataFrame, label: str = "long") -> pd.DataFrame:
        
        target_col = self.column_mapping.get(label)
        if target_col is None:
            raise KeyError(f"Nie nzaleziono wskaźnika z etykietą '{label}'. \nUpewnij się, że najpierw wywołałeś add_sma z tą etykietą")
        
        df['Regime'] = np.where((df['Close'] > df[target_col]) & (df['Slope'] > 0.01), 'Bullish',
                            np.where((df['Close'] < df[target_col]) & (df['Slope'] < -0.01), 'Bearish', 'Sideways'))
        
        return df
        
        
    def prepare_all_indicators(self, df: pd.DataFrame, sma_configs: Optional[Dict[str, int]] = None) -> pd.DataFrame:
        df = df.copy()
        self.column_mapping = {} # Resetowanie mapowania
        configs = sma_configs if sma_configs else self.default_sma_periods
        
        # 1. SMA
        for label, period in configs.items():
            df = self.add_sma(df, period=period, label=label)
            
        # 2. ATR
        df = self.add_atr(df)
        
        # 3. Slope dla slope_sma
        df = self.add_slope(df, label="slope_sma")
        
        # 4. Regime dla Slope
        df = self.classify_regimes(df, label="slope_sma")
        
        return df
    
    