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

def get_API_key():
    try:
        keyfile = os.environ['HOME']+'/.ssh/apikey/finn'
        with open(keyfile, 'rt') as f:
            key = f.readline().strip()
    except:
        print(f"Error: Need {keyfile}")
        sys.exit(1)
    return key

if __name__ == "__main__":
    api_key = get_API_key()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={api_key}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
