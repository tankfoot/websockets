#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import sqlite3
import json
from dialogflow_v1 import DialogflowApi

sqlite_file = '/home/jim/Documents/sqlite3/dialogflow'
table_name = 'dialogflow'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

async def ws_server(websocket, path):
    while True:
        try:
            in_data= await websocket.recv()
            print(f"< {in_data}")
        except websockets.exceptions.ConnectionClosed:
            break

        a = DialogflowApi()
        r = a.post_query(in_data)
        response = r.json()
        print(response)
        out_data = response['result']['fulfillment']['speech']
        if 'intentName' in response['result']['metadata']:
            intent_name = response['result']['metadata']['intentName']
        else:
            intent_name = 'None'
        intent_score = response['result']['score']

        c.execute('INSERT INTO dialogflow VALUES (?, ?, ?, ?)', [in_data, intent_name, intent_score, out_data])
        conn.commit()

        await websocket.send(out_data)
        print(f"> {out_data}")

def start_server():
    host = 'localhost'
    port = 8765
    server = websockets.serve(ws_server, host, port)
    print('start listening at {}:{}'.format(host, port))

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_server()
