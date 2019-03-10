import urllib.request

import time

import pandas as pd

import json


coinjar_params = {
	"id_ticker": "",
	"before_time": "",
	"after_time": "",
	"interval": "5m"
}

# print("I am in coinjar.py", coinjar_endpoint);


coinjar_params["id_ticker"] = "BTCAUD"

# end time for the get call is the current time

current_time = int(time.time()) 

coinjar_params["before_time"] = str(current_time)

# Start time for the get call is the current time

coinjar_params["after_time"] = str(current_time - (24 * 60 * 60))

coinjar_endpoint = "https://data.exchange.coinjar.com/products/" + coinjar_params["id_ticker"] + "/candles?before=" + coinjar_params["before_time"] + "&after=" + coinjar_params["after_time"] + "&interval=" + coinjar_params["interval"]

print(coinjar_endpoint)

# contents is a json string
contents = urllib.request.urlopen(coinjar_endpoint).read()

print("I am contents", contents)

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

contents_obj = json.loads(contents.decode('utf-8'))

df_coinjar = pd.DataFrame(contents_obj, columns=header).set_index('Timestamp')

print("i am data frame", df_coinjar)
