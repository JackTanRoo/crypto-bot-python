# ****************

# started getting data

# ****************


import ccxt

from datetime import datetime, timedelta, timezone

import math

import argparse

import pandas as pd

import binance_api

print(binance_api.binance_api)


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
# exchange6 = "huobipro"

exchange_params = {
    'binance': {
        'fees': 0.01
        'slippage': 0.005
    },
    'huobipro': {
        'fees': 0.02
        'slippage': 0.005
    },
}


margin_of_error = 0.01

symbols = "DASH/BTC"

timeframe = "5m"

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

# # Save it
# symbol_out = symbols.replace("/","")
# filename = '{}-{}-{}.csv'.format(exchange1, symbol_out,timeframe)
# # df.to_csv(filename)

# Data of Exchange 5

exchange5_data = exchange5_obj.fetch_ohlcv(symbols, timeframe)

# header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

df5 = pd.DataFrame(exchange5_data, columns=header).set_index('Timestamp')
print("I have finished getting data: ", exchange5, df5)
# 

# ****************

# finished getting data

# ****************


# *****************

# once you get the data, iterate over it and compare time the same time frame for arbitrage opportunities

# *****************

for index, row in df1.iterrows():
    # df2.loc[df2['Timestamp'] == row["Timestamp"]]
    print(index)

    price_exchange_one = row['Close']
    price_exchange_five = df5.loc[index]['Close']

    try: 
        if (is_profitable_to_buy(exchange1, price_exchange_one, exchange5, price_exchange_five, margin_of_error)):
            print ("sell at ", exchange5, df5.loc[index]['Close'], "buy at ", exchange1, row["Close"], "at time ", index)


        if (df5.loc[index]['Close']) < ((1- margin_of_error) * row['Close']):
            print ("buy at ", exchange5, df5.loc[index]['Close'], "sell at ", exchange1, row["Close"], "at time ", index)
    except KeyError:
        print ("No keys for index", index)


# Output: 
#    10 100
#    11 110
#    12 120


# *****************

# identify profitable trades after accounting for fees and slippage

# ***************** 


# is profitable to buy at exchange 1

def is_profitable_to_buy(exchange_one, price_exchange_one, exchange_two, price_exchange_two, margin_of_error):

    estimated_final_purchase_ price_ex1 = price_exchange_one * (1 + exchange_params[exchange_one].slippage) * (1 + exchange_params[exchange_one].fees)

    estimated_final_sell_ price_ex2 = price_exchange_two * (1 + exchange_params[exchange_two].slippage) * (1 + exchange_params[exchange_two].fees)
    
    estimated_final_price_diff = estimated_final_purchase_price_ex1 - estimated_final_sell_price_ex2;

    print ("estimated final price diff", estimated_final_price_diff, "estimated final price diff / base price", estimated_final_price_diff / price_exchange_one)

    if (estimated_final_price_diff / price_exchange_one > margin_of_error):
        return True

    return False





# *****************

# once you get trade signal
# make the trade on both exchanges

# *****************


# commit a xxx% of the balance to open an order on Exchange 1


# commit the same xxx% of balance to open the opposite order on Exchange 2


# update net profit position after trade


# record trade in object



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



