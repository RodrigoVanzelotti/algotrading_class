import MetaTrader5 as mt5
from datetime import date, datetime, timedelta  # poderia usar dateoffset ao invés de timedelta
import pandas as pd
from pathlib import Path
import os
from typing import Union, Optional


# Tipagem =========================
'''
Pegar o costume de utilizar o mypy para verificação de tipagem
mypy file.py
'''
timeframe_type = int
data_frame_return = Optional[pd.DataFrame]

# =================================
class Vanzelottrader:
    # Constantes da Classe ==============
    TIMEFRAME_DICT = {  # o quanto cada timeframe pode representar em dias? Ver estudos na função self.read_ohlc()
            'TIMEFRAME_M1': [mt5.TIMEFRAME_M1, 60],
            'TIMEFRAME_M2': [mt5.TIMEFRAME_M2, 120],
            'TIMEFRAME_M3': [mt5.TIMEFRAME_M3, 180],
            'TIMEFRAME_M4': [mt5.TIMEFRAME_M4, 240],
            'TIMEFRAME_M5': [mt5.TIMEFRAME_M5, 300],
            'TIMEFRAME_M6': [mt5.TIMEFRAME_M6, 360],
            'TIMEFRAME_M10': [mt5.TIMEFRAME_M10, 600],
            'TIMEFRAME_M12': [mt5.TIMEFRAME_M12, 720],
            'TIMEFRAME_M15': [mt5.TIMEFRAME_M15, 900],
            'TIMEFRAME_M20': [mt5.TIMEFRAME_M20, 1200],
            'TIMEFRAME_M30': [mt5.TIMEFRAME_M30, 1800],
            'TIMEFRAME_H1': [mt5.TIMEFRAME_H1, 3600],
            'TIMEFRAME_H2': [mt5.TIMEFRAME_H2, 7200],
            'TIMEFRAME_H3': [mt5.TIMEFRAME_H3, 10800],
            'TIMEFRAME_H4': [mt5.TIMEFRAME_H4, 14400],
            'TIMEFRAME_H6': [mt5.TIMEFRAME_H6, 21600],
            'TIMEFRAME_H8': [mt5.TIMEFRAME_H8, 28800],
            'TIMEFRAME_H12': [mt5.TIMEFRAME_H12, 43200],
            'TIMEFRAME_D1': [mt5.TIMEFRAME_D1, 86400],
            'TIMEFRAME_W1': [mt5.TIMEFRAME_W1, 604800],
            'TIMEFRAME_MN1' : [mt5.TIMEFRAME_MN1, 2592000],
    }

    def __init__(self, test, broker):
        # set broker no futuro
        pass

    # Abaixo funções que serão utilizadas pelo usuário
    # Leitura de dados ==================
    def get_market_data(self) -> dict:
        pass

    def get_ohlc(self, 
                 symbol: str, 
                 timeframe: timeframe_type, 
                 initial_date: datetime = datetime(2012, 1, 1), 
                 final_date: datetime = datetime.now()
    ) -> data_frame_return:
        df_raw = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'])
        
        timedelta_default = timedelta(days=self.TIMEFRAME_DICT[timeframe][1])
        final_date_aux = initial_date + timedelta_default
        timeframe = self.TIMEFRAME_DICT[timeframe][0]

        # Appending data to dataframe
        while True:
            data_aux = mt5.copy_rates_range(symbol, timeframe, initial_date, min(final_date_aux, final_date)) 
            df_aux = pd.DataFrame(data_aux)
            df_aux['time'] = pd.to_datetime(df_aux['time'], unit='s')
            df_raw = pd.concat([df_aux, df_raw], ignore_index=True)

            if final_date_aux > final_date: break
            
            initial_date = df_aux['time'].max()
            final_date_aux = initial_date + timedelta_default

        return self._slice(df_raw, initial_date, final_date)

    def get_ticks(self, 
                  symbol: str, 
                  initial_date: datetime = datetime(2012, 1, 1), 
                  final_date: datetime = datetime.now()
    ) -> data_frame_return:
        
        # df_raw = self._get_ticks()
        return None
        return self._slice(df_raw, initial_date, final_date)
        

    # Trading ===========================
    def send_order(self) :
        pass

    def cancel_order(self):
        pass

    def show_my_book(self):
        pass

    def trade_history(self):
        pass

    # Infos =============================
    def show_balance(self) -> float:
        pass

    def show_limit(self) -> float:
        pass

    # def todo!




    # Abaixo funções auxiliares apenas, não utilizadas pelo usuário
    def _slice(self, 
               df: pd.DataFrame,
               initial_date: datetime, 
               final_date: datetime
    ) -> data_frame_return:
        df['time'] = pd.to_datetime(df['time'])
        return df.loc[(df['time'] >= initial_date) & (df['time'] < final_date)]