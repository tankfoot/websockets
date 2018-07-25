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

async def hello(websocket, path):
    while True:
        name = await websocket.recv()

        print(f"< {name}")

        a = DialogflowApi()
        r = a.post_query(name)
        data = r.json()
        greeting = data['result']['fulfillment']['speech']

        try:
            c.execute('INSERT INTO chat VALUES (?, ?)', [name, greeting])
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column')

        conn.commit()

        await websocket.send(greeting)
        print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
