from data_manager import DataManager
from indicators import IndicatorLibrary
from strategies import SMAStrategy, TrendFollowingStrategy
from analyzer import PerformanceAnalyzer
from my_fun import *
import pandas as pd

all_reports = {}

default_config = {
        'short' : 5,
        'mid' : 20,
        'long' : 40,
        'slope_sma' : 100
    }

strategies_to_test = [
    TrendFollowingStrategy("Trend Follower, {}"),
    SMAStrategy("SMA Cross", default_config)
]

# 1. Przygotowanie danych i wskaźników (To już masz z Dnia 1)
data_manager = DataManager(start_date="2020-01-01", end_date="2024-01-01")
df = data_manager.get_clean_data("AAPL")

indicators = IndicatorLibrary()
df = indicators.prepare_all_indicators(df, default_config)
mapping = indicators.column_mapping # <--- TO JEST KLUCZ!

results_df = pd.DataFrame(index=df.index)

# 2. Wybór strategii (Tutaj dzieje się magia OOP)
# Możemy łatwo przełączać strategie:
# strategy = SMAStrategy("Prosta SMA", {})

# --- TEST STRATEGII 1: Trend Follower ---
strategy1 = TrendFollowingStrategy("Trend Follower", {})
df_1 = strategy1.generate_signals(df.copy(), mapping)
calculate_position(df_1)
results_df['Trend Follower'] = get_strategy_returns(df_1, "Trend Follower")

# --- TEST STRATEGII 2: SMA ---
strategy2 = SMAStrategy("SMA Cross", default_config)
df_2 = strategy2.generate_signals(df.copy(), mapping)
calculate_position(df_2)
results_df['SMA Cross'] = get_strategy_returns(df_2, "SMA Cross")

print(df_1[['Close', 'Regime', 'Signal']].tail(10))
print(df_2[['Close', 'Regime', 'Signal']].tail(10))

plot_results(df, results_df)