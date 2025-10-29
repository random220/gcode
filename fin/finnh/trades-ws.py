#!/usr/bin/env python

import os, sys

#https://pypi.org/project/websocket_client/
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    #ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

def getToken():
    try:
        tokenfile = os.environ['HOME']+'/.ssh/apikey/finn'
        with open(tokenfile, 'rt') as f:
            key = f.readline().strip()
    except:
        print(f"Error: Need {tokenfile}")
        sys.exit(1)
    return key

if __name__ == "__main__":
    websocket.enableTrace(True)
    token=getToken()
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={token}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
