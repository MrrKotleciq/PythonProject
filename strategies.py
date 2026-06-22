import pandas as pd
from strategy_base import StrategyBase

class SMAStrategy(StrategyBase):
    '''
    SMA strategy
    '''

    def generate_signals(self, df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
        
        # 1. Pobieram nazwę kolumny z mapowania
        short_sma_col = column_mapping.get('short')
        mid_sma_col = column_mapping.get('mid')
        long_sma_col = column_mapping.get('long')
        
        required = [short_sma_col, mid_sma_col, long_sma_col]
        
        if not all(required):
            missing = [col for col in required if not col]
            print(f"Błąd: Brak kolumny {missing} w danych!")
            return df
        
        # 2. Obliczam warunki na podstawie danych (wyzwalacz sygnału)
        
        buy_trigger = (df[short_sma_col] > df[mid_sma_col]) & (df[short_sma_col].shift(1) <= df[mid_sma_col].shift(1)) & (df['Close'] > df[long_sma_col])
        sell_trigger = (df[short_sma_col] < df[mid_sma_col]) & (df[short_sma_col].shift(1) >= df[mid_sma_col].shift(1))
        
       # sell_trigger = (df[short_sma_col] < df[mid_sma_col]) & (df[short_sma_col].shift(1) >= df[mid_sma_col].shift(1))
        
        # 3. Tworzymy tymczasową kolumnę z triggerami
        
        df['Trigger'] = 0
        df.loc[buy_trigger, 'Trigger'] = 1
        df.loc[sell_trigger, 'Trigger'] = -1
        
        # 4. Przesuwamy sygnał o 1 dzień w przód, żeby sygnał z dnia 1 
        # stał się sygnałem działania dnia 2.
        
        df['Signal'] = df['Trigger'].shift(1).fillna(0) # Przesuwam i uzupełniam puste pola '0'.
        
        return df
    
    
class TrendFollowingStrategy(StrategyBase):
    
    def generate_signals(self, df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
        
        # Sprawdzamy czy są kolumny 'Regime' i 'Slope' w DataFrame
        if 'Regime' not in df.columns or 'Slope' not in df.columns:
            return df
        
        df['Signal'] = 0
        
        buy_trigger = (df['Regime'] == 'Bullish') & (df['Regime'].shift(1) != 'Bullish') & (df['Slope'] > 0)
        
        sell_trigger = (df['Regime'] == 'Bearish') & (df['Regime'].shift(1) != 'Bearish')
        
        df['Trigger'] = 0
        df.loc[buy_trigger, 'Trigger'] = 1
        df.loc[sell_trigger, 'Trigger'] = -1
        
        df['Signal'] = df['Trigger'].shift(1).fillna(0)
        
        return df