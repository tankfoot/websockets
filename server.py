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

            a = DialogflowApi()
            response = a.text_query(in_data)
            print(response.json())

            data = response.json()
            data_format['data']['speech'] = data['queryResult']['fulfillmentText']
            data_format['header'][6] = len(data['queryResult']['fulfillmentText'])

            if 'parameters' in data['queryResult']:
                data_format['data']['entity'] = data['queryResult']['parameters']
            else:
                data_format['data']['entity'] = None
            
            await ws.send(json.dumps(data_format))
        
        except websockets.exceptions.ConnectionClosed:
            print('disconnected')
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
