import pandas as pd
import path
import regex as re
import time
import binance_config
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import binance.enums

API_key_binance = binance_config.API_key
secret_key_binance = binance_config.secret_key
binance_client = binance.Client(API_key_binance, secret_key_binance)

futures_data = pd.read_excel(path.filtered_futures_data)
for text in futures_data["Article Header"]:
    if re.search("Binance Futures Will Launch USDⓈ-M", text, re.IGNORECASE): # Temporary solution, not super efficient but works
        if re.search("Perpetual Contract", text, re.IGNORECASE):
            if re.search("Leverage", text, re.IGNORECASE):
                splited_text = text.split()
                ticker = splited_text[5]
                full_ticker = ticker + "_USDT"
                print(ticker)

# fetch 1 minute klines for the last day up until now
klines = binance_client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# fetch 30 minute klines for the last month of 2017
# klines = binance_client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
# klines = binance_client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

print(type(klines)) # List with OHLC?