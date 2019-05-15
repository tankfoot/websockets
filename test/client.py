#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import time

quest = {
            'header': [1111, 0, 1000, int(time.time()), 3, 0],
            'data': {
                'query': "",
            }
        }

chipotle_holder = "ws://54.218.175.199:8080/chipotle"
local_holder = "ws://localhost:8080/chipotle"


async def hello():
    async with websockets.connect(
            'ws://54.218.175.199:8080/chipotle') as websocket:

        while True:
            quest['header'][1] = int(input("app level:"))
            quest['header'][2] = int(input("page level:"))
            quest['data']['query'] = input("Query:")

            await websocket.send(json.dumps(quest))
            start = time.time()
            greeting = await websocket.recv()
            end = time.time()
            print("round trip time: {}".format(end - start))
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
