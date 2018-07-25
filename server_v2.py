#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import sqlite3
import json
from dialogflow_v1 import DialogflowApi

sqlite_file = '/home/jim/Documents/sqlite3/chat'
table_name = 'chat'
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
        out_data = response['result']['fulfillment']['speech']

        c.execute('INSERT INTO chat VALUES (?, ?)', [in_data, out_data])
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
