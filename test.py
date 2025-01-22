import MetaTrader5 as mt5

import pandas as pd

import numpy as np
from datetime import datetime
import pytz


 


import MetaTrader5 as mt5

# MetaTrader 5 path and credentials
path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
login = 10005401126
password = "GuLaT*8j"
server = "MetaQuotes-Demo"
timeout = 10000

# Attempt to initialize MetaTrader 5
if mt5.initialize(path=path, login=login, password=password, server=server, timeout=timeout):
    print("Initialization successful")
else:
    print("Initialization failed")
    print("Error code:", mt5.last_error())  
    exit()
# account_info_dict = mt5.account_info()._asdict()
# account_info_df = pd.DataFrame(account_info_dict, index=[0])
# print("Profit:", account_info_df["profit"].iloc[0])

# print("Equity:", account_info_df["equity"].iloc[0])

# print("Margin:", account_info_df["margin"].iloc[0])

# print("Margin Free:", account_info_df["margin_free"].iloc[0])
###########################################################################  Retrieve Data  ###############################################
# symbol = "EURUSD"

# timeframe = mt5.TIMEFRAME_H1
end_time = datetime.today().astimezone(pytz.utc)

# eurusd_rates = mt5.copy_rates_from(symbol, timeframe, end_time, 10)

# eurusd_df = pd.DataFrame(eurusd_rates)
# eurusd_df['time'] = pd.to_datetime(eurusd_df['time'], unit='s').dt.tz_localize('UTC')

# print (eurusd_df.head())
###########################################################################  Tick data  ###############################################
euraud_tick = mt5.copy_ticks_from("EURAUD", end_time, 20, mt5.COPY_TICKS_ALL)

euraud_tick = pd.DataFrame(euraud_tick)

euraud_tick['time'] = pd.to_datetime(euraud_tick['time'], unit='s')
print (euraud_tick.head())
###########################################################################  Send Signal  ###############################################
# request = {

#     "action": mt5.TRADE_ACTION_DEAL,

#     "symbol": 'EURUSD',

#     "volume": 0.2,

#     "type": mt5.ORDER_TYPE_BUY,

#     "price": mt5.symbol_info_tick('EURUSD').ask,        

#     "comment": "Quantra Market Buy Order",
# }

# order_result = mt5.order_send(request)
# if order_result.retcode != mt5.TRADE_RETCODE_DONE:
#     print("Error placing order: ", order_result.comment)
# else:
#     print("Order placed successfully, order ticket:", order_result.order)

result = mt5.positions_get()
if result:

      # create a list of dictionaries containing the data for each position
    data = pd.DataFrame([position._asdict() for position in result])
#     print("Unrealized P&L: ", data.profit.sum())
#     # print the DataFrame
#     print(data.head())
# else:
#     print("No positions found")

ticket = int(data.iloc[0].ticket)

 

# check if the position exists and its type

position = mt5.positions_get(ticket=ticket)
if position:
    if position[0].type == mt5.ORDER_TYPE_BUY:
        # if the position is a buy position, send a sell order to close it
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position[0].symbol,
            "volume": position[0].volume,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position[0].ticket,
            "price": mt5.symbol_info_tick(position[0].symbol).bid,
        }
    else:
        # if the position is a sell position, send a buy order to close it
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position[0].symbol,
            "volume": position[0].volume,
            "type": mt5.ORDER_TYPE_BUY,
            "position": position[0].ticket,
            "price": mt5.symbol_info_tick(position[0].symbol).ask,
        }

    # close the position
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Error closing position: ", result.comment)
    else:
        print(f"Position {position[0].ticket} closed \
successfully, order ticket: {result.order}")
else:
    print(f"Position {ticket} not found")