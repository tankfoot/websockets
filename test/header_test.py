#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import time

quest = {
            'header': [1111, 0, 1000, int(time.time()), 3, 0],
            'data': {
                'info': 'AppVersion: 1.0.01252019, DeviceId: 990012012045891, \
                SystemVersion: 9, SystemSdk: 28, Brand: google, Manufacturer: Google, \
                Model: Pixel 3 XL, SystemLanguage: en'
            }
        }


async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:

        while True:
            quest['header'][1] = int(input("app level:"))
            quest['header'][2] = int(input("page level:"))

            await websocket.send(json.dumps(quest))

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
