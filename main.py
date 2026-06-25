from classes.data_manager import DataManager
from classes.indicators import IndicatorLibrary
from classes.strategies import SMAStrategy, TrendFollowingStrategy
from classes.analyzer import PerformanceAnalyzer
from classes.visualizer import Visualizer
from my_fun import *
import pandas as pd

all_reports = {}
all_curves = {}

default_config = {
        'short' : 5,
        'mid' : 15,
        'long' : 50,
        'slope_sma' : 100
    }

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

# --- TEST STRATEGII ---

strategies_to_test = [
    TrendFollowingStrategy("Trend Follower", {}),
    SMAStrategy("SMA Cross", {})
]

for strat in strategies_to_test:
    
    # 1. Generowanie sygnałów na kopii danych
    df_strat = strat.generate_signals(df.copy(), mapping)
    
    # 2. Obliczanie pozycji
    
    df_strat = calculate_position(df_strat)
    
    # 3. Analiza wydajności
    analyzer = PerformanceAnalyzer(df_strat, strat.name)
    all_reports[strat.name] = analyzer.get_full_report()
    all_curves[strat.name] = analyzer.equity_curve_pct
    
# 4. Tworzenie finalnej tabeli porównawczej

comparison_df = pd.DataFrame(all_reports).T
print("\n" + "="*30)
print("REPORT WYDAJNOŚCI STRATEGII")
print("="*30)
print(comparison_df)

viz = Visualizer()
viz.plot_results(all_curves, analyzer.benchmark_curve_pct)