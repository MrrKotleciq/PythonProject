import pandas as pd
import yfinance as yf
import logging


class DataManager:
    
    '''Klasa odpowiedzialna za pobieranie i przygotowanie danych.'''
    
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("DataManager")
        
        
    def fetch_data(self, ticker: str) -> pd.DataFrame:
        
        '''Pobiera dane z yfinance i wykonuje wstępne czyszczenie.'''
        
        try:
            self.logger.info(f"Pobieranie danych dla: {ticker}...")
            df = yf.download(ticker, start=self.start_date, end=self.end_date)
            
            if df.empty:
                self.logger.warning(f"Nie pobrano żadnych danych dla {ticker}.")
                return pd.DataFrame()
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.ffill().bfill() # Uzupełnienie nan
            return df
        except Exception as e:
            self.logger.error(f"Bąd podczas pobierania {ticker}: {e}")
            return pd.DataFrame()
    
    
    def get_clean_data(self, ticker: str) -> pd.DataFrame:
        
        '''Metoda pomocnicza, która gwarantuje, że dane są gotowe do analizy.'''
        
        df = self.fetch_data(ticker)
        
        # Można dodać dodatkowe filtry
        
        return df