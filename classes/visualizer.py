import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizer:
    @staticmethod
    def plot_results(equity_curves_pct: dict, benchmark_curve_pct: pd.Series):
        
        '''
        Generuje wykres porównawczy: Equity Curve i Drawdown.
        :param equity_curves_pct: Słownik {'Nazwa Strategii': equity_curve_series}
        :param benchmark_curve_pct: Seria z wynikiem Buy & Hold.
        '''
        
        COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,10), sharex=True, gridspec_kw={'height_ratios': [3,1]})
        
        
        # --- WYKRES 1: Equity Curves ---
        ax1.plot(benchmark_curve_pct, label="Buy & Hold (Benchmark)", color='black', linewidth=1.5, linestyle='--', alpha=0.6)
        
        for i, (name, curve) in enumerate(equity_curves_pct.items()):
            color = COLORS[i % len(COLORS)]
            ax1.plot(curve, label=name, color=color, linewidth=2)
            
        ax1.set_title("Porównanie Krzywych Kapitału", fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel("Mnożnik Kapitału (Start = 1.0)", fontsize=12)
        ax1.legend(frameon=True, facecolor='white', edgecolor='gray')
        ax1.grid(True, alpha=0.3)
        
        
        # --- WYKRES 2: Drawdowns ---
        benchmark_dd = (benchmark_curve_pct - benchmark_curve_pct.cummax()) / benchmark_curve_pct.cummax() * 100
        ax2.fill_between(benchmark_dd.index, benchmark_dd, 0, color='gray', alpha=0.3, label="B&H DD")
        
        for i, (name, curve) in enumerate(equity_curves_pct.items()):
            color = COLORS[i % len(COLORS)]
            dd = (curve - curve.cummax()) / curve.cummax() * 100
            ax2.fill_between(dd.index, dd, 0, color=color, alpha=0.4, label=f"{name} DD")
            ax2.plot(dd, color=color, linewidth=1, alpha=0.8)
        
        ax2.set_title("Maksymalne Obsunięcia (Drawdowns)", fontsize=14, fontweight='bold')
        ax2.set_ylabel("Spadek %", fontsize=12)
        ax2.set_xlabel("Data", fontsize=12)
        ax2.legend(loc='upper left', fontsize='small', ncol=3, frameon=True)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()