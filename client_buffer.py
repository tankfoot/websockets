#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import time
import base64

quest = {
            'header': [1111, 1, 1000, int(time.time()), 3, 0, 1],
            'data': {
                'audio': None
            }
}


async def hello():
    async with websockets.connect(
            'ws://localhost:3456') as websocket:

        start = time.time()
        with open("data/test.wav", "rb") as speech:
            content = speech.read()

        n = 512
        stream = [content[i:i + n] for i in range(0, len(content), n)]

        for chunk in stream:
            quest['data']['audio'] = base64.b64encode(chunk).decode('utf-8')
            await websocket.send(json.dumps(quest))

        quest['header'][6] = 0
        await websocket.send(json.dumps(quest))
        greeting = await websocket.recv()
        stop = time.time()
        print(f"< {greeting}")
        print('round trip time: {}'.format(round(stop - start, 5)))

asyncio.get_event_loop().run_until_complete(hello())
