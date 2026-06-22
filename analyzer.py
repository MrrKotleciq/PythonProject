import pandas as pd
import numpy as np

class PerformanceAnalyzer:
    
    def __init__(self, df_with_position: pd.DataFrame, strategy_name: str):
        
        '''
        :param df_with_position: DataFrane zawierający kolumny 'Close' i 'Position,'
        :param strategy_name: Nazwa strategii dla raportu.
        '''
        
        self.df = df_with_position.copy()
        self.strategy_name = strategy_name
        
        # Obliczam dzienne stopy zwrotu strategii
        daily_returns = self.df['Close'].pct_change().fillna(0)
        self.strategy_returns = daily_returns * self.df['Position']
        
        self.equity_curve = (1 + self.strategy_returns).cumprod()
        
    
    def calculate_cagr(self) -> float:
        
        '''
        Compound Annual Growth Rate - Średni roczny zwrot.
        '''
        
        start_val = self.equity_curve.iloc[0]
        end_val = self.equity_curve.iloc[-1]
        
        # Obliczamy czas trwania w latach
        
        days = (self.df.index[-1] - self.df.index[0]).days
        years = days / 365.25
        
        if years == 0: return 0.0
        cagr = (end_val / start_val) ** (1 / years) - 1
        return cagr * 100
    
    def calculate_max_drawdown(self) -> float:
        
        '''
        Maksymalne odsunięcie kapitału od szczytu do dołka.
        '''
 
        rolling_max = self.equity_curve.cummax()
        drawdown = (self.equity_curve - rolling_max) / rolling_max
        return drawdown.min() * 100 # Zwraca wartość ujemną
    
    def calculate_sharpie_ratio(self, risk_free_rate=0.0) -> float:
        
        '''
        Wskaźnik Sharpie'a - stosunek zysku do ryzyka.
        '''
        
        mean_return = self.strategy_returns.mean()
        std_return = self.strategy_returns.std()
        
        if std_return == 0: return 0.0
        
        # Anuualizacja
        sharpie = (mean_return - risk_free_rate) / std_return * np.sqrt(252)
        
        return sharpie
    
    def _get_trades(self):
        
        '''
        Pomocnicza metoda do identyfikacji pojedyńczych transakcji.
        '''
        
        # Znajdujemy momenty zmiany pozycji ( 0 -> 1 lub 1 -> 0)
        pos_diff = self.df['Position'].diff().fillna(0)
        entries = pos_diff[pos_diff == 1].index
        exits = pos_diff[pos_diff == -1].index
        
        trades = []
        
        # Parsujemy wejścia z wyjściami
        for i in range(min(len(entries), len(exits))):
            entry_price = self.df.loc[entries[i], 'Close']
            exit_price = self.df.loc[exits[i], 'Close']
            trade_return = (exit_price / entry_price) - 1
            trades.append(trade_return)
            
        return np.array(trades)
    
    def calculate_trade_metrics(self) -> dict:
        
        '''
        Oblicza Win Rate i Profit Factor na podstawie zamkniętych transakcji.        
        '''
        
        trades = self._get_trades
        
        if len(trades) == 0:
            return {"Win Rate": 0.0, "Profit Factor": 0.0, "Total Trades": 0}
        
        wins = trades[trades > 0]
        losses = trades[trades <= 0]
        
        win_rate = len(wins) / len(losses) * 100
        
        sum_wins = np.sum(wins)
        sum_losses = np.abs(np.sum(losses))
        
        profit_factor = sum_wins / sum_losses if sum_losses != 0 else np.inf
        
        return {
            "Win Rate": win_rate,
            "Profit Factor": profit_factor,
            "Total Trades": len(trades)
            }
        
    def get_full_report(self) -> pd.Series:
        
        '''
        Generuje pełny raport w formie serii Pandas.
        '''
        
        trade_metrics = self.calculate_trade_metrics()
        
        return pd.Series({
            "CAGR (%)": self.calculate_cagr(),
            "Max Drawdown (%)": self.calculate_max_drawdown(),
            "Sharpie Ratio": self.calculate_sharpie_ratio(),
            "Win Rate (%)": trade_metrics["Win Rate"],
            "Profit Factor": trade_metrics["Profit Factor"],
            "Total Trades": trade_metrics["Total Trades"]
        })