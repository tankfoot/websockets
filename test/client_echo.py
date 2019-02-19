#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import time


async def hello():
    async with websockets.connect(
            'ws://142.93.91.246/ws_echo/') as websocket:

        while True:
            in_data = input("query:")

            await websocket.send(in_data)

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
