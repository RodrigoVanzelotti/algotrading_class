import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# import pytz module for working with time zone
import pytz

from main_functions import *

# Inicialização ======================================
intialize_mt5()

# Setar a timezone na classe Vanzelottrader
timezone = pytz.timezone('America/Sao_Paulo')

utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime.now()

ticks = mt5.copy_ticks_range("PETR4", utc_from, utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))

# processos acerca do df
df_ticks = pd.DataFrame(ticks)

# convert time in seconds into the datetime format
df_ticks['time']=pd.to_datetime(df_ticks['time'], unit='s')

df_ticks.head()



# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
# request 100 000 EURUSD ticks starting from 10.01.2019 in UTC time zone
max_count = 1000000000
ticks = mt5.copy_ticks_from("PETR4", utc_from, max_count, mt5.COPY_TICKS_TRADE)
print("Ticks received:",len(ticks))
 
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
 
# display data
print("\nDisplay dataframe with ticks")
print(ticks_frame.head(10))  