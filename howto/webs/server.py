#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import re
import os

async def lcfc(websocket, path):
    async for message in websocket:
        m = re.search(r'^user\n', message)
        if m:
            m = re.search(r'\n(.+?)\n?$', message)
            if m:
                user = m.group(1)
                datafile = f"data/{user}"
                alltext='anyany'
                if os.path.isfile(datafile):
                    with open(datafile, 'rt') as f:
                        alltext = f.read()
                await websocket.send(f'{user}\n{alltext}')
            else:
                await websocket.send(f'got "{message}"')

server = websockets.serve(lcfc, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
