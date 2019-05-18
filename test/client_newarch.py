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

response = {
            'header': [1111, 0, 1000, int(time.time()), 3, 0],
            'data': {
                'response': None,
            }
        }


async def hello():
    async with websockets.connect(
            'ws://localhost:8080/chipotle') as websocket:

        while True:
            quest['data']['query'] = input("Query:")
            await websocket.send(json.dumps(quest))
            greeting = await websocket.recv()
            print(f"< {greeting}")

            response['header'][2] = int(input("page level:"))
            response['data']['response'] = input("Response:")
            await websocket.send(json.dumps(response))
            greeting = await websocket.recv()
            print(f"< {greeting}")



asyncio.get_event_loop().run_until_complete(hello())
