import pandas as pd
import path
import regex as re
import time
import binance_config
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import binance.enums
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta

def get_OHLCV_from_Binance_spot(ticker, listing_date):
    '''Function is returning list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)'''
    d = listing_date
    dt = datetime.strptime(d, '%Y-%m-%d %H:%M')
    listing_date_plus_4_hours = dt + timedelta(hours=4)
    listing_date_minus_4_hours = dt - timedelta(hours=4)
    OHLCV_list = binance_client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, str(listing_date_minus_4_hours), str(listing_date_plus_4_hours))
    return OHLCV_list

API_key_binance = binance_config.API_key
secret_key_binance = binance_config.secret_key
binance_client = binance.Client(API_key_binance, secret_key_binance)

futures_data = pd.read_excel(path.filtered_futures_data)
for text, date in zip(futures_data["Article Header"], futures_data["Date"]):
    if re.search("Binance Futures Will Launch USDⓈ-M", text, re.IGNORECASE): # Temporary solution, not super efficient but works
        if re.search("Perpetual Contract", text, re.IGNORECASE):
            if re.search("Leverage", text, re.IGNORECASE):
                splited_text = text.split()
                ticker = splited_text[5]
                full_ticker = ticker + "_USDT"
                print(date)
                print(ticker + "\n")
                full_ticker = ticker + "USDT"
                try:
                    print(get_OHLCV_from_Binance_spot(full_ticker, date))
                except BinanceAPIException as e:
                    print(e.message + "\n")