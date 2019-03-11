import urllib.request

import time

import pandas as pd

import json

import datetime

from dateutil import parser


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

coinjar_volume_endpoint = "https://data.exchange.coinjar.com/products/"+coinjar_params["id_ticker"]+ "/stats?at=" + coinjar_params["after_time"]

print("I am volume info", urllib.request.urlopen(coinjar_volume_endpoint ).read())


coinjar_endpoint = "https://data.exchange.coinjar.com/products/" + coinjar_params["id_ticker"] + "/candles?before=" + coinjar_params["before_time"] + "&after=" + coinjar_params["after_time"] + "&interval=" + coinjar_params["interval"]

# print(coinjar_endpoint)


# https://apilayer.net/api/live
#     ? access_key = YOUR_ACCESS_KEY
#     & currencies = AUD,EUR,GBP,PLN

# Get end point to pandas 

# get currency conversion rates

currency_conversion_endpoint = "http://www.apilayer.net/api/live?access_key=97ec6af4d54ae75ef9cf190f8706b6c7&currencies=AUD"

current_currency = urllib.request.urlopen(currency_conversion_endpoint).read()

current_currency_obj = json.loads(current_currency.decode('utf-8'))

# {'success': True, 'terms': 'https://currencylayer.com/terms', 'privacy': 'https://currencylayer.com/privacy', 'timestamp': 1552276146, 'source': 'USD', 'quotes': {'USDAUD': 1.42115}}

print("I am contents", current_currency_obj)

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

    df_coinjar.at[index,"Unix"] = unix_time
    df_coinjar.at[index,"USDConversion"] = current_currency_obj["quotes"]["USDAUD"]
    df_coinjar.at[index,"USDConversion"] = current_currency_obj["quotes"]["USDAUD"]
    df_coinjar.at[index,"USD"] = float(row["Close"]) / float(current_currency_obj["quotes"]["USDAUD"])

    # print(unix_time)


print("i am data frame", df_coinjar)




