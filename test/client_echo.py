#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import string
import time
import random


async def hello():
    async with websockets.connect(
            'ws://142.93.91.246/ws_echo/') as websocket:

        for i in range(6):
            in_data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1000000))

            start = time.time()
            await websocket.send(in_data)
            greeting = await websocket.recv()
            end = time.time()
            #print(f"< {greeting}")
            print("response time: {}".format(end - start))

asyncio.get_event_loop().run_until_complete(hello())
