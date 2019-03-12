# ****************

# started getting data

# ****************


import ccxt

from datetime import datetime, timedelta, timezone

import math

import argparse

import pandas as pd

import urllib.request

import time

import json

import datetime

from dateutil import parser

import matplotlib.pyplot as plt

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='CCXT Market Data Downloader')


    # parser.add_argument('-s','--symbol',
    #                     type=str,
    #                     required=True,
    #                     help='The Symbol of the Instrument/Currency Pair To Download')

    # parser.add_argument('-e','--exchange',
    #                     type=str,
    #                     required=True,
    #                     help='The exchange to download from')

    parser.add_argument('-t','--timeframe',
                        type=str,
                        default='1d',
                        choices=['1m', '5m','15m', '30m','1h', '2h', '3h', '4h', '6h', '12h', '1d', '1M', '1y'],
                        help='The timeframe to download')


    parser.add_argument('--debug',
                            action ='store_true',
                            help=('Print Sizer Debugs'))

    return parser.parse_args()

# Get our arguments
args = parse_args()

# args
exchange1 = "binance"
# exchange2 = "poloniex"
# exchange3 = "bitfinex"
# exchange4 = "bittrex"
exchange5 = "huobipro"
exchange6 = "coinjar"

exchange_params = {
    'binance': {
        'fees': 0.001,
        'slippage': 0.005
    },
    'huobipro': {
        'fees': 0.002,
        'slippage': 0.005
    },
    'coinjar': {
        'fees': 0.001,
        'slippage': 0.01
    },
}


margin_of_error = 0.01

symbols = "LTC/USDT"

timeframe = "5m"


# 

# unixtime = time.mktime(d.timetuple())
coinjar_params = {
    "id_ticker": "",
    "before_time": "",
    "after_time": "",
    "interval": "5m"
}

# print("I am in coinjar.py", coinjar_endpoint);


coinjar_params["id_ticker"] = "LTCAUD"

# end time for the get call is the current time

current_time = int(time.time()) 

coinjar_params["before_time"] = str(current_time)

# Start time for the get call is the current time

coinjar_params["after_time"] = str(current_time - (24 * 60 * 60))

coinjar_endpoint = "https://data.exchange.coinjar.com/products/" + coinjar_params["id_ticker"] + "/candles?before=" + coinjar_params["before_time"] + "&after=" + coinjar_params["after_time"] + "&interval=" + coinjar_params["interval"]

# print(coinjar_endpoint)


# https://apilayer.net/api/live
#     ? access_key = YOUR_ACCESS_KEY
#     & currencies = AUD,EUR,GBP,PLN

# Get end point to pandas 

# get currency conversion rates

currency_conversion_endpoint = "http://www.apilayer.net/api/live?access_key=97ec6af4d54ae75ef9cf190f8706b6c7&currencies=AUD"


# starting balance in USDT

starting_balance_exchange1_USDT = 1000
starting_balance_exchange2_USDT = 1000


# starting balance in Dash
starting_balance_exchange1_crypto = 12
starting_balance_exchange2_crypto = 12

# Get our Exchange
# Error check if exchange 1 is handled by ccxt

try:
    exchange1_obj = getattr (ccxt, exchange1)();

    print("I am the exchange", exchange1)
    print("I am symbols of,", exchange1, exchange1_obj.symbols)
    # print(" I am ccxt", ccxt.binance)


except AttributeError:
    print('-'*36,' ERROR ','-'*35)
    print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange1))
    print('-'*80)
    quit()

# Error check if exchange 2 is handled by ccxt

# try:
#     # exchange2_obj = getattr (ccxt, exchange2) ()
#     exchange2_obj = ccxt.poloniex({
#         'enableRateLimit': True,
#         'resolutin':"auto"
#     })
#     print("I am the exchange", exchange2)
#     # print(" I am ccxt", ccxt.binance)

# except AttributeError:
#     print('-'*36,' ERROR ','-'*35)
#     print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange2))
#     print('-'*80)
#     quit()


# Error check if exchange 3 is handled by ccxt

# try:
#     exchange3_obj = getattr (ccxt, exchange3) ()
#     print("I am the exchange", exchange3)
#     # print(" I am ccxt", ccxt.binance)

# except AttributeError:
#     print('-'*36,' ERROR ','-'*35)
#     # print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange2))
#     print('-'*80)
#     quit()

# # Error check if exchange 4 is handled by ccxt

# try:
#     exchange4_obj = getattr (ccxt, exchange4) ()
#     print("I am the exchange", exchange4)
#     # print(" I am ccxt", ccxt.binance)

# except AttributeError:
#     print('-'*36,' ERROR ','-'*35)
#     # print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange2))
#     print('-'*80)
    # quit()


# Error check if exchange 5 is handled by ccxt

try:
    exchange5_obj = getattr (ccxt, exchange5) ()
    print("I am the exchange", exchange5)
    # print(" I am ccxt", ccxt.binance)

except AttributeError:
    print('-'*36,' ERROR ','-'*35)
    # print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange5))
    print('-'*80)
    quit()


# Error check if exchange 6 is handled by ccxt

# try:
#     exchange6_obj = getattr (ccxt, exchange6) ()
#     print("I am the exchange", exchange6)
#     # print(" I am ccxt", ccxt.binance)

# except AttributeError:
#     print('-'*36,' ERROR ','-'*35)
#     # print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange2))
#     print('-'*80)
#     quit()



# *********

# Get Live Data

# *********


# Check if fetching of OHLC Data is supported

# Check for Exchange 1

if exchange1_obj.has["fetchOHLCV"] != True:
    print('-'*36,' ERROR ','-'*35)
    print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange1))
    print('-'*80)
    quit()

# # Check for Exchange 2
# if exchange2_obj.has["fetchOHLCV"] != True:
#     print('-'*36,' ERROR ','-'*35)
#     print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange2))
#     print('-'*80)
#     quit()

# # Check for Exchange 5
if exchange5_obj.has["fetchOHLCV"] != True:
    print('-'*36,' ERROR ','-'*35)
    print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange5))
    print('-'*80)
    quit()




# Check requested timeframe is available. If not return a helpful error.

# Check for Exchange 1
if (not hasattr(exchange1_obj, 'timeframes')) or (timeframe not in exchange1_obj.timeframes):
    print('-'*36,' ERROR ','-'*35)
    print('The requested timeframe ({}) is not available from {}\n'.format(timeframe, exchange1))
    print("what is up", exchange1_obj)

    for key in exchange1_obj.timeframes.keys():
        print('  - ' + key)
    print('-'*80)
    quit()

# # Check for Exchange 2
# if (not hasattr(exchange2_obj, 'timeframes')) or (timeframe not in exchange2_obj.timeframes):
#     print()
#     print('-'*36,' ERROR ','-'*35)
#     print('The requested timeframe ({}) is not available from {}\n'.format(timeframe, exchange2))
#     print('Available timeframes are:')
#     for key in exchange2_obj.timeframes.keys():
#         print('  - ' + key)
#     print('-'*80)
#     quit()

# Check for Exchange 5
if (not hasattr(exchange5_obj, 'timeframes')) or (timeframe not in exchange5_obj.timeframes):
    print('-'*36,' ERROR ','-'*35)
    print('The requested timeframe ({}) is not available from {}\n'.format(timeframe, exchange5))
    # print("what is up", exchange5_obj)

    for key in exchange5_obj.timeframes.keys():
        print('  - ' + key)
    print('-'*80)
    quit()



# Check if the symbol is available on the Exchange

# Check for Exchange 1

exchange1_obj.load_markets()

# print("I am symbols of,", exchange1, exchange1_obj.symbols)

if symbols not in exchange1_obj.symbols:
    print('-'*36,' ERROR ','-'*35)
    print('The requested symbol ({}) is not available from {}\n'.format(symbols, exchange1))
    print('Available symbols are:')
    for key in exchange1_obj.symbols:
        print('  - ' + key)
    print('-'*80)
    quit()

# Check for Exchange 2

# exchange2_obj.load_markets()

# # print("I am symbols of,", exchange2, exchange2_obj.symbols)

# if symbols not in exchange2_obj.symbols:
#     print('-'*36,' ERROR ','-'*35)
#     print('The requested symbol ({}) is not available from {}\n'.format(symbols, exchange2))
#     print('Available symbols are:')
#     for key in exchange2_obj.symbols:
#         print('  - ' + key)
#     print('-'*80)
#     quit()


# exchange5_obj.load_markets()

# checks for exchanges

# print("I am symbols of,", exchange1, exchange1_obj.symbols)
# print("I am symbols of,", exchange2, exchange2_obj.symbols)

# exchange3_obj.load_markets()
# print("I am symbols of,", exchange3, exchange3_obj.symbols)

# exchange4_obj.load_markets()
# print("I am symbols of,", exchange4, exchange4_obj.symbols)
# # print("I am symbols of,", exchange5, exchange5_obj.symbols)


exchange5_obj.load_markets()
print("I am symbols of,", exchange5, exchange5_obj.symbols)

if symbols not in exchange5_obj.symbols:
    print('-'*36,' ERROR ','-'*35)
    print('The requested symbol ({}) is not available from {}\n'.format(symbols, exchange5))
    print('Available symbols are:')
    for key in exchange5_obj.symbols:
        print('  - ' + key)
    print('-'*80)
    quit()



# exchange6_obj.load_markets()
# print("I am symbols of,", exchange6, exchange6_obj.symbols)



# Get data
# print("I am started getting data")

# Data of Exchange 1

exchange1_data = exchange1_obj.fetch_ohlcv(symbols, timeframe)

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
df1 = pd.DataFrame(exchange1_data, columns=header).set_index('Timestamp')
print("I have finished getting data: ", exchange1, df1)



# xxxx

ax1 = plt.subplot(311)
ax1.set_ylabel("Binance Price of " + symbols)

df1.loc[:, ["Close"]].plot(ax=ax1)

plt.show()


# # Save it
# symbol_out = symbols.replace("/","")
# filename = '{}-{}-{}.csv'.format(exchange1, symbol_out,timeframe)
# # df.to_csv(filename)

# Data of Exchange 5

exchange5_data = exchange5_obj.fetch_ohlcv(symbols, timeframe)

# header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

df5 = pd.DataFrame(exchange5_data, columns=header).set_index('Timestamp')
# print("I have finished getting data: ", exchange5, df5)
# 


# Get Australian Data



# ***************


# *********


current_currency = urllib.request.urlopen(currency_conversion_endpoint).read()

current_currency_obj = json.loads(current_currency.decode('utf-8'))

# {'success': True, 'terms': 'https://currencylayer.com/terms', 'privacy': 'https://currencylayer.com/privacy', 'timestamp': 1552276146, 'source': 'USD', 'quotes': {'USDAUD': 1.42115}}

# print("I am contents", current_currency_obj)

# contents is a json string
contents = urllib.request.urlopen(coinjar_endpoint).read()

# print("I am contents", contents)

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

contents_obj = json.loads(contents.decode('utf-8'))

df_coinjar = pd.DataFrame(contents_obj, columns=header).set_index('Timestamp')

df_coinjar["Unix"] = ""
df_coinjar["USDConversion"] = ""
df_coinjar["USD"] = ""

for index, row in df_coinjar.iterrows():
    # df2.loc[df2['Timestamp'] == row["Timestamp"]]
    dt = parser.parse(index)

    unix_time = time.mktime(dt.timetuple())

    df_coinjar.at[index,"Unix"] = int(unix_time) * 1000
    df_coinjar.at[index,"USDConversion"] = current_currency_obj["quotes"]["USDAUD"]
    df_coinjar.at[index,"USDConversion"] = current_currency_obj["quotes"]["USDAUD"]
    df_coinjar.at[index,"USD"] = float(row["Close"]) / float(current_currency_obj["quotes"]["USDAUD"])

    # print(unix_time)

# set unix as the index
df_coinjar.set_index("Unix", inplace=True)


print("i am data frame of coinjar", df_coinjar)


# ****************

# finished getting data

# ****************





# *****************

# identify profitable trades after accounting for fees and slippage

# ***************** 


# is profitable to buy at exchange 1

def is_profitable_to_buy(exchange_one, price_exchange_one, exchange_two, price_exchange_two, margin_of_error):

    # est_purchase_ price = (price_exchange_one * (1 + exchange_params[exchange_one].slippage) * (1 + exchange_params[exchange_one].fees))
    
    estimated_buy_price = (price_exchange_one * (1 + exchange_params[exchange_one]['slippage']) * (1 + exchange_params[exchange_one]['fees']))
    
    estimated_sell_price = (price_exchange_two * (1 + exchange_params[exchange_two]['slippage']) * (1 + exchange_params[exchange_two]['fees']))
    
    estimated_final_price_diff =  estimated_buy_price -  estimated_sell_price


    if (estimated_final_price_diff / price_exchange_one > margin_of_error):
        print ("estimated final price diff", estimated_final_price_diff, "estimated final price diff / base price", estimated_final_price_diff / price_exchange_one)
        return True

    return False



# *****************

# once you get trade signal
# make the trade on both exchanges

# *****************

# *****************

# once you get the data, iterate over it and compare time the same time frame for arbitrage opportunities

# *****************

for index, row in df1.iterrows():
    # df2.loc[df2['Timestamp'] == row["Timestamp"]]
    # print(index)

    price_exchange_one = row['Close']
    # price_exchange_five = df5.loc[index]['Close']
    if index in df_coinjar.index:
        price_exchange_six = df_coinjar.loc[index]['USD']

        try: 
            if (is_profitable_to_buy(exchange1, price_exchange_one, exchange6, price_exchange_six, margin_of_error)):
                print ("buy at ", exchange6, df_coinjar.loc[index]['USD'], "sell at ", exchange1, row["Close"], "at time ", index)


            if (is_profitable_to_buy(exchange6, price_exchange_six, exchange1, price_exchange_one, margin_of_error)):
                print ("sell at ", exchange6, df_coinjar.loc[index]['USD'], "buy at ", exchange1, row["Close"], "at time ", index)
        except KeyError:
            print ("No keys for index", index)


# Output: 
#    10 100
#    11 110
#    12 120


# commit a xxx% of the balance to open an order on Exchange 1


# commit the same xxx% of balance to open the opposite order on Exchange 2


# update net profit position after trade


# record trade in object







# *********



# *****************

# analytics

# *****************

# work out number of trades of vertime



# *********

# Backtest for 1 week

# *********



# *****************

# graph prices

# *****************




# *****************

# graph trades

# *****************



