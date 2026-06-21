from data_manager import DataManager
from indicators import IndicatorLibrary
import pandas as pd

def run_validation_test(ticker, sma_config, test_name):
    print(f"\n{'='*20} TEST: {test_name} {'='*20}")
    
    # 1. Inicjacja
    dm = DataManager(start_date="2020-01-01", end_date="2024-01-01")
    lib = IndicatorLibrary()
    
    # 2. Pobieranie danych
    
    data = dm.get_clean_data(ticker)
    if data.empty:
        print(f"Błąd: Nie pobrano danych dla {ticker}")
        return
    
    # 3. Generowanie wskaźników z konkretną konfiguracją
    
    # Przekazujemy sma_config, aby sprawdzić czy dynamiczne nazwy działają
    df_resault = lib.prepare_all_indicators(data, sma_config)
    
    # 4. Weryfikacja
    print(f"Konfiguracja SMA: {sma_config}")
    print(f"Mapowanie kolumn: {lib.column_mapping}")
    
    # Sprawdzamy czy klyuczowe kolumny istnieją 
    required_col = ['ATR', 'Slope', 'Regime']
    all_present = all(col in df_resault.columns for col in required_col)
    
    if all_present:
        print("✅ SUKCES: Wszystkie kluczowe wskaźniki zostały obliczone.")
    else:
        missing = [col for col in required_col if col not in df_resault.columns]
        print(f"❌ BŁĄD: Brakuje kolumn: {missing}")
        
    # Wyświetlanie fragmentu danych dla wizualnej kontroli
    # Wybieramy tylko kolumny z mapowania + kluczowe wskaźniki
    cols_to_show  = list(lib.column_mapping.values()) + required_col + ['Close']
    print(f"\nFragment danych:\n", df_resault[cols_to_show].tail())
    
if __name__ == "__main__":
    ticker_to_test = "AAPL"
    
    default_config = {
        'short' : 14,
        'mid' : 30,
        'long' : 150,
        'slope_sma' : 100
    }
    
    # TEST 1: Ustawienia domyślne (Standard)
    run_validation_test(ticker_to_test, default_config, "Domyślna Konfiguracja")
    
    # TEST 2: Customowe ustawienia (Optymalizacja)
    
    custom_config = {
        'short' : 20,
        'mid' : 50,
        'long' : 200,
        'slope_sma' : 150
    }
    
    run_validation_test(ticker_to_test, custom_config, "Customowa Konfiguracja")