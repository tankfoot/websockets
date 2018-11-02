#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import time
from dialogflow_v2 import DialogflowApi

data_format = {
                'header':[0, 0, 0, 0, int(time.time()), 3, 0],
                'data':{
                        'speech': None,
                        'entity': None
                }
}

async def ws_server(ws, path):
    while True:
        try:
            in_data = await ws.recv()
            data_format['data']['speech'] = in_data
            data_format['header'][6] = len(in_data)

            a = DialogflowApi()
            response = a.text_query('Navigation')
            print(response.json())
            await ws.send(json.dumps(data_format))
            print(json.dumps(data_format))
        
        except websocket.exceptions.ConnectionClosed:
            print('disconnected')
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
