#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

class G:

async def lcfc(websocket, path):
    async for message in websocket:
        await websocket.send(f'got "{message}"')

server = websockets.serve(lcfc, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
