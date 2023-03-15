import MetaTrader5 as mt5
from datetime import date, datetime, timedelta  # poderia usar dateoffset ao invés de timedelta
import pandas as pd
from pathlib import Path
import os
from typing import Union, Optional, Boolean
from collections.abc import Mapping
import pytz


# Tipagem =========================
'''
Pegar o costume de utilizar o mypy para verificação de tipagem
mypy file.py
'''
timeframe_type, action_type = int, int
data_frame_return = Optional[pd.DataFrame]
order_return = Optional[dict]


# =================================
class Vanzelottrader:
    # Constantes da Classe ==============
    keys = ['TIMEFRAME_M1', 'TIMEFRAME_M2', 'TIMEFRAME_M3', 'TIMEFRAME_M4', 'TIMEFRAME_M5', 
            'TIMEFRAME_M6', 'TIMEFRAME_M10', 'TIMEFRAME_M12', 'TIMEFRAME_M15', 'TIMEFRAME_M20', 
            'TIMEFRAME_M30', 'TIMEFRAME_H1', 'TIMEFRAME_H2', 'TIMEFRAME_H3', 'TIMEFRAME_H4', 
            'TIMEFRAME_H6', 'TIMEFRAME_H8', 'TIMEFRAME_H12', 'TIMEFRAME_D1', 'TIMEFRAME_W1', 
            'TIMEFRAME_MN1']
    values =[mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M2, mt5.TIMEFRAME_M3, mt5.TIMEFRAME_M4, mt5.TIMEFRAME_M5,
            mt5.TIMEFRAME_M6, mt5.TIMEFRAME_M10, mt5.TIMEFRAME_M12, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M20,
            mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H2, mt5.TIMEFRAME_H3, mt5.TIMEFRAME_H4, 
            mt5.TIMEFRAME_H6, mt5.TIMEFRAME_H8, mt5.TIMEFRAME_H12, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, 
            mt5.TIMEFRAME_MN1]
    secs = [60, 120, 180, 240, 300, 360, 600, 720, 900, 1200, 1800, 3600, 7200, 10800, 14400, 21600, 28800,
            43200, 86400, 604800, 2592000]

    TIMEFRAME_DICT = {x: y for x, y in zip(keys, [[v,s] for v, s in zip(values, secs)])}
    TIMEZONE = pytz.timezone('America/Sao_Paulo')

    def __init__(self, test, broker):
        # set broker no futuro
        pass

    # Abaixo funções que serão utilizadas pelo usuário
    # Leitura de dados ==================
    def get_market_data(self) -> data_frame_return:
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
                  copy_ticks_type: int = mt5.COPY_TICKS_TRADE,  
                  date_from: datetime = datetime(2012, 1, 1, tzinfo=TIMEZONE)
    ) -> data_frame_return:
        # Importante notar que nem sempre é possível extrair os ticks da data requisitada, visto que são muitos
        max_count = 50000000
        ticks = mt5.copy_ticks_from(symbol, date_from, max_count, copy_ticks_type)
        
        # create DataFrame out of the obtained data
        df_raw = pd.DataFrame(ticks)
        # convert time in seconds into the datetime format
        df_raw['time'] = pd.to_datetime(df_raw['time'], unit='s')

        return self._slice(df_raw, date_from)
    
    # Trading ===========================
    def send_order(self,
                   action: action_type,
                   symbol: str,
                   volume: float,
                   type: action_type,
                   price: float,
                   sl: Optional[float] = None,
                   tp: Optional[float] = None,
                   deviation: Optional[int] = None,
                   magic: Optional[int] = None,
                   comment: Optional[str] = None,
                   type_time: Optional[int] = None,
                   type_filling: Optional[int] = None
    ) -> order_return:
        request = {key: value for key, value in locals().items() if value is not None}

        if self._check_volume(volume, symbol):
            return None
        
        result_check = mt5.order_check(request)._asdict()
        print("Checagem de fundos [ORDER_CHECK], retorno: ",result_check['retcode'], result_check['comment'])

        if self._order_retcode_false_return(result_check):
            print('O resultado não foi positivo, retornando a função de envio de ordem. Rever a ordem.')
            return result_check
        

        



    
        pass

    def cancel_order(self,
                     order_number: int
    ) -> order_return:
        # Create the request
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order_number,
            "comment": f"Removing order #{order_number}"
        }

        # Send order to MT5
        order_result = mt5.order_send(request)._asdict()
        return order_result

    def show_my_book(self) -> pd.DataFrame:
        pass

    def trade_history(self) -> pd.DataFrame:
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
               final_date: datetime = datetime.now()
    ) -> data_frame_return:
        df['time'] = pd.to_datetime(df['time'])
        return df.loc[(df['time'] >= initial_date) & (df['time'] < final_date)]
    
    # Analisa o código de retorno
    def _order_retcode_false_return(self,
                            result: dict
    ) -> bool:
        return True if result['retcode'] != 0 else False
    
    # Analisa se o symbol está disponível/existe
    def _check_symbol(self, 
                     symbol: str
    ) -> bool:
        symbol_info = mt5.symbol_info(symbol)
        
        # se o símbolo não estiver disponível no MarketWatch, adicionamos
        if not symbol_info.visible and not mt5.symbol_select(symbol,True):
            print(f"{symbol} não foi encontrado, não é possível chamar order_check()")
            return True
        else: return False

    # Analisa se o volume é possível de ser executado    
    def _check_volume(self,
                      vol: float, 
                      symbol: str):
        vol = float(vol)
        maxvol = mt5.symbol_info(symbol).volumehigh
        minvol = mt5.symbol_info(symbol).volumelow
        if vol < minvol or vol > maxvol:
            print(f'Erro ao declarar o volume:\n\tVolume Selecionado: {vol}\n\tVolume Mínimo: {minvol}\n\tVolume Máximo: {maxvol}')
            return True
        else: return False
        

