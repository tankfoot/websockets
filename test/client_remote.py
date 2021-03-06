#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import time

quest = {
            'header': [1111, 0, 1000, int(time.time()), 3, 0],
            'data': {
                'query': None,
            }
        }


async def hello():
    async with websockets.connect(
            'ws://178.128.181.252/ws/') as websocket:

        while True:
            quest['header'][1] = int(input("app level:"))
            quest['header'][2] = int(input("page level:"))
            quest['data']['query'] = input("Query:")

            await websocket.send(json.dumps(quest))

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
