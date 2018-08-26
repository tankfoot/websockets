#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
from dialogflow_v1 import DialogflowApi
from flow_manager import flow_control

async def hello(websocket, path):
    clientJson = await websocket.recv()
    print(f"< {clientJson}")

    greeting = flow_control(clientJson)

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
