# from catalyst import run_algorithm
# from catalyst.api import order, record, symbol
# import pandas as pdt
#
#
# from catalyst import ingest-exchange
#
# print(ingest-exchange -x bitfinex -i btc_usd)


# STORIES
# create server
# select crypto to track to track pricing data and make trades
# select crypto exchange to track pricing data and make trades
# select fiat pair to track forex rates
# select forex rate exchange to pull exchange data from
# pull pricing data from selected crypto exchanges every 1 minute
# pull forex data from selected forex source every 1 hour
# plot data as a live graph that updates every 1 minute
# provide trade suggestions 
# plot trade suggestions on graph updated every 1 minute
# plot trade suggestions on the graph every 1 minute
# make trades to selected trades based on key trade parameters - balance, trading amount, trading currency, trading direction, trading price
# track balance after every trade
# calculate profitability of every trade

# create server

import http.server
import socketserver as SocketServer
import ccxt
import hashlib
import base64
import chardet



#  coinjar endpoint format
#  coinjar_endpoint = "https://data.exchange.coinjar.com/products/" + coinjar_params["id_ticker"] + "/candles?before=" + coinjar_params["before_time"] + "&after=" + coinjar_params["after_time"] + "&interval=" + coinjar_params["interval"]
#  forex_format = "http://www.apilayer.net/api/live?access_key=97ec6af4d54ae75ef9cf190f8706b6c7&currencies=AUD"

context = {
	"selected_exchanges": {
		"exchange_1": "binance",
		"exchange_2": "coinjar",	
	},
	"crypto_exchange_parameters": {
		"coinjar": {
			"data_endpoint": "https://data.exchange.coinjar.com/products/"
		}
	},
	"forex_parameters":{
		"forex_api": "http://www.apilayer.net/api/live?access_key=97ec6af4d54ae75ef9cf190f8706b6c7&currencies="
	},
	"selected_trading_pairs": {
		"crypto_1": "LTC/USD",
		"crypto_2": "LTC/AUD",
		"fiat_1": "AUD",
		"fiat_2": "USD"
	}
}


WS_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("I am in handle: ", self.data)
        headers = self.data.split(b"\r\n")

        # is it a websocket request?
        # if "Connection: Upgrade" in self.data and "Upgrade: websocket" in self.data:
        #     # getting the websocket key out
        print("I am headers: ", headers)
        for h in headers:
            print("this is my type of h", type(h))
            the_encoding = chardet.detect(h)['encoding']
            print("I am in str encode", the_encoding)
            string_header_element = h.decode("TIS620")
            print("decoded", string_header_element)
            if str.encode("Sec-WebSocket-Key") in string_header_element:
                print("I am in str encode")
                # the_encoding = chardet.detect(h)['encoding']
                key = string_header_element.split(" ")[1]
                print("I am in str encode", the_encoding, string_header_element)
   #      # let's shake hands shall we?
                self.shake_hand(key)

    #     while True:
    #         payload = self.decode_frame(bytearray(self.request.recv(1024).strip()))
    #         decoded_payload = payload.decode('utf-8')
    #         self.send_frame(payload)
    #         if "bye" == decoded_payload.lower():
    #             "Bidding goodbye to our client..."
    #             return
    # # else:
    #     self.request.sendall("HTTP/1.1 400 Bad Request\r\n" + \
    #                          "Content-Type: text/plain\r\n" + \
    #                          "Connection: close\r\n" + \
    #                          "\r\n" + \
    #                          "Incorrect request")

    def shake_hand(self,key):
        # calculating response as per protocol RFC
        key = key + WS_MAGIC_STRING
        resp_key = base64.standard_b64encode(hashlib.sha1(key.encode("ASCII")).digest())
        print("I am in RESP encode", resp_key)

        resp="HTTP/1.1 101 Switching Protocols\r\n" + \
             "Upgrade: websocket\r\n" + \
             "Connection: Upgrade\r\n" + \
             "Sec-WebSocket-Accept: %s\r\n\r\n"%(resp_key)

        self.request.sendall(resp.encode("ASCII"))

    # def decode_frame(self,frame):
    #     opcode_and_fin = frame[0]

    #     # assuming it's masked, hence removing the mask bit(MSB) to get len. also assuming len is <125
    #     payload_len = frame[1] - 128

    #     mask = frame [2:6]
    #     encrypted_payload = frame [6: 6+payload_len]

    #     payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)])

    #     return payload

    # def send_frame(self, payload):
    #     # setting fin to 1 and opcpde to 0x1
    #     frame = [129]
    #     # adding len. no masking hence not doing +128
    #     frame += [len(payload)]
    #     # adding payload
    #     frame_to_send = bytearray(frame) + payload

    #     self.request.sendall(frame_to_send)


# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "localhost", 3000

server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
server.serve_forever()




