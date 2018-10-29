#!/usr/bin/env python

# WS client example

import asyncio
import websockets

headers = {'controllerId' : 1,
           'applicationId' : 0}

async def hello():
    async with websockets.connect(
            'ws://localhost:8765', extra_headers = headers) as websocket:
        
        while True:
            name = input("What's your name? ")

            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
