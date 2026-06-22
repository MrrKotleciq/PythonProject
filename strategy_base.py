from abc import ABC, abstractmethod
import pandas as pd

class StrategyBase(ABC):
    
    ''' Klasa bazowa strategii '''
    
    def __init__(self, name: str, params: dict = None):
        
        ''' 
        Konstruktor:
        :param name: Nazwa strategii (np. TrendFollowing, SMA)
        :param params: Słownik z parametrami (np. progi wejścia)
        '''
        
        self.name = name
        self. params = params if params is not None else {}
        print(f"Inicjacja strategii {self.name}")
        
        @abstractmethod
        def generate_signals(self, df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
            
            '''
            Metoda konieczna do implementacji
            :param df: DataFrame z danymi i wskaźnikami
            :param column_mapping: Słownik mapujący nazwy (np. 'short' -> 'short_14')
            :return: DataFrame z dodaną kolumną 'Signal'
            '''
                    
            pass

