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
            print(in_data)
            in_json = json.loads(in_data)
            try:
                header = in_json['header']
                query = in_json['data']['query']
                data_format['header'][0] = in_json['header'][0]
                data_format['header'][1] = in_json['header'][1]
                data_format['header'][2] = in_json['header'][2]
                data_format['header'][3] = in_json['header'][2]
            except KeyError:
                print('in_data: KeyError')
                break

            a = DialogflowApi()
            response = a.text_query(query)
            print(response.json())

            data = response.json()
            try:
                data_format['data']['speech'] = data['queryResult']['fulfillmentText']
                data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
            except KeyError:
                data_format['data']['speech'] = 'KeyError'

            try:
                data_format['data']['entity'] = data['queryResult']['parameters']
            except KeyError:
                print('No Entity detected')
            
            await ws.send(json.dumps(data_format))
        
        except websockets.exceptions.ConnectionClosed:
            print('disconnected')
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
