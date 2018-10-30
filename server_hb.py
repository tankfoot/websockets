#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import time

data_format = {
                'header':[0, 0, 0, 0, time.time(), 3, 0],
                'data':{
                        'speech': None,
                        'entity': None
                }
}

async def ws_server(ws, path):
    while True:
        try:
            in_data = await asyncio.wait_for(ws.recv(), timeout = 20)
        except asyncio.TimeoutError:
            #Check the connection in 20 seconds
            try:
                pong_waiter = await ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=10)
            except asyncio.TimeoutError:
                #No response to ping in 10 seconds, disconnect
                print('timeout')
        else:
            data_format['data']['speech'] = in_data
            data_format['header'][6] = len(in_data)
            await ws.send(json.dumps(data_format))
            print(json.dumps(data_format))

start_server = websockets.serve(ws_server, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
