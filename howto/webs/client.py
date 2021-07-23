#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://0.0.0.0:5678"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(message)

asyncio.get_event_loop().run_until_complete(hello())
