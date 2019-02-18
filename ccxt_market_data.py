# ****************

# started getting data

# ****************


import ccxt

from datetime import datetime, timedelta, timezone

import math

import argparse

import pandas as pd


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
exchange2 = "acx"

symbols = "ETH/USDT"

timeframe = "1d"


# Get our Exchange
# Error check if exchange 1 is handled by ccxt

try:
    exchange1_obj = getattr (ccxt, exchange1) ()
    print("I am the exchange", exchange1)
    # print(" I am ccxt", ccxt.binance)


except AttributeError:
    print('-'*36,' ERROR ','-'*35)
    print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange1))
    print('-'*80)
    quit()

# Error check if exchange 2 is handled by ccxt

try:
    exchange2_obj = getattr (ccxt, exchange2) ()
    print("I am the exchange", exchange2)
    # print(" I am ccxt", ccxt.binance)

except AttributeError:
    print('-'*36,' ERROR ','-'*35)
    print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange2))
    print('-'*80)
    quit()






# Check if fetching of OHLC Data is supported

# Check for Exchange 1

if exchange1_obj.has["fetchOHLCV"] != True:
    print('-'*36,' ERROR ','-'*35)
    print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange1))
    print('-'*80)
    quit()

# Check for Exchange 2
if exchange2_obj.has["fetchOHLCV"] != True:
    print('-'*36,' ERROR ','-'*35)
    print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange2))
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

# Check for Exchange 2
if (not hasattr(exchange2_obj, 'timeframes')) or (timeframe not in exchange2_obj.timeframes):
    print()
    print('-'*36,' ERROR ','-'*35)
    print('The requested timeframe ({}) is not available from {}\n'.format(timeframe, exchange2))
    print('Available timeframes are:')
    for key in exchange2_obj.timeframes.keys():
        print('  - ' + key)
    print('-'*80)
    quit()


# Check if the symbol is available on the Exchange

# Check for Exchange 1

exchange1_obj.load_markets()

print("I am symbols of,", exchange1, exchange1_obj.symbols)

if symbols not in exchange1_obj.symbols:
    print('-'*36,' ERROR ','-'*35)
    print('The requested symbol ({}) is not available from {}\n'.format(symbols, exchange1))
    print('Available symbols are:')
    for key in exchange1_obj.symbols:
        print('  - ' + key)
    print('-'*80)
    quit()

# Check for Exchange 2

exchange2_obj.load_markets()

print("I am symbols of,", exchange2, exchange2_obj.symbols)

if symbols not in exchange2_obj.symbols:
    print('-'*36,' ERROR ','-'*35)
    print('The requested symbol ({}) is not available from {}\n'.format(symbols, exchange2))
    print('Available symbols are:')
    for key in exchange2_obj.symbols:
        print('  - ' + key)
    print('-'*80)
    quit()



# Get data
# print("I am started getting data")
# data of first exchange

exchange1_data = exchange1_obj.fetch_ohlcv(symbols, timeframe)

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
df = pd.DataFrame(exchange1_data, columns=header).set_index('Timestamp')
# Save it
symbol_out = symbols.replace("/","")
filename = '{}-{}-{}.csv'.format(exchange1, symbol_out,timeframe)

# df.to_csv(filename)
print("I have finished getting data: ", df)

# Get Data


# ****************

# finished getting data

# ****************