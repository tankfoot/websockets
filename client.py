#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json

quest = {
            'currentPage': None,
            'query': None
        }

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:

        quest['currentPage'] = input("What's the current page? ")
        quest['query'] = input("Query:")


        await websocket.send(json.dumps(quest))

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
