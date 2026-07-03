import pandas as pd
import itertools
from classes.analyzer import PerformanceAnalyzer
from classes.indicators import IndicatorLibrary
from classes.strategies import *
from my_fun import *

class Optimizer:
    
    def __init__(self, df: pd.DataFrame, strategy_name: str, strategy_class):
        
        self.df = df
        self.strategy_name = strategy_name
        self.indicator_lib = IndicatorLibrary()
        self.strategy_class = strategy_class
        self.param_grid = {
            'short' : [5, 8, 10, 12, 14, 16, 18, 20, 22, 25],
            'mid' : [12, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80],
            'long' : [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170],
            'slope_sma' : [100]
        } if strategy_class == SMAStrategy else {
            'short' : [5],
            'mid' : [15],
            'long' : [50],
            'slope_sma' : [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190 ,200]
        }
        self.constaints = {
            'max_dd' : -20.0 if strategy_class == SMAStrategy else -30,
            'min_sharpe' : 0.5,
            'min_cagr' : 5.0
        }
        self.sort_by = 'Sharpe Ratio'
        
    def run(self):
        
        iterations = list(itertools.product(*self.param_grid.values()))
        
        all_results = []
        i = 0
        
        for [short, mid, long, slope_sma] in iterations:
            
            i += 1
            print(f"{i}/{len(iterations)}")
            
            if short >= mid or mid >= long:
                continue
            
            df_temp = self.df.copy()
            current_params = {
                'short': short,
                'mid': mid,
                'long': long,
                'slope_sma': slope_sma
                }
            
            df_temp = self.indicator_lib.prepare_all_indicators(df_temp, current_params)
            strat = self.strategy_class(self.strategy_name, current_params)
            df_temp = strat.generate_signals(df_temp, self.indicator_lib.column_mapping)
            df_temp = calculate_position(df_temp)
            
            analyzer = PerformanceAnalyzer(df_temp, self.strategy_name)
            raport = analyzer.get_full_report()
            raport = pd.concat([raport, pd.Series(current_params)])
            
            all_results.append(raport)
            
        result_df = pd.DataFrame(all_results)
        
        maska_dd = result_df['Max Drawdown [%]'] >= self.constaints['max_dd']
        maska_sharpe = result_df['Sharpe Ratio'] >= self.constaints['min_sharpe']
        maska_cagr = result_df['CAGR [%]'] >= self.constaints['min_cagr']
        
        result_df = result_df[maska_cagr & maska_dd & maska_sharpe]
        
        if result_df.empty:
            print("Brak konfiguracji spełniającej wymagania.")
        
        result_df = result_df.sort_values(by=self.sort_by, ascending=False)
        
        return result_df