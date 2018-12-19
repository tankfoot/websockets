#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json

quest = {
<<<<<<< HEAD
            'header': [1,0,0,1,1,1],
=======
            'header': [1111, 1, 1000, 4, 5, 6],
>>>>>>> 64912582daef96248c97e65d489044d2229c9434
            'data': {
                'query': None,
                'entity': None
            }
        }

async def hello():
    async with websockets.connect(
            'ws://178.128.181.252/ws/') as websocket:

        while True:
            quest['data']['query'] = input("Query:")

            await websocket.send(json.dumps(quest))

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
