#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

class G:
    ID = 99

async def time(websocket, path):
    G.ID = G.ID + 1
    myid = G.ID
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send('ID: '+str(myid)+' '+now)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
