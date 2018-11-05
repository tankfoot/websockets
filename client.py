#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json

quest = {
            'header': [1,2,3,4,5,6,7],
            'data':{
                'query': None,
                'entity': None
            }
        }

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:

        quest['data']['query'] = input("Query:")


        await websocket.send(json.dumps(quest))

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
