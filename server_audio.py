#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import sqlite3
import json
import wave
from dialogflow_v2 import DialogflowApi

# sqlite_file = '/home/jim/Documents/sqlite3/chat'
# table_name = 'chat'
# conn = sqlite3.connect(sqlite_file)
# c = conn.cursor()
outfile = None
infile = wave.open('/home/jim/Desktop/hello.wav', 'rb')
params = infile.getparams()

async def ws_server(websocket, path):

    with wave.open('/home/jim/Desktop/hello.wav', 'wb') as out_file:
        while True:
            l = await websocket.recv()
            if not l: break
            out_file.setparams(params)
            out_file.writeframes(l)

    # while True:
    #     try:
    #         in_data= await websocket.recv()
    #     except websockets.exceptions.ConnectionClosed:
    #         break
    #
    #     outfile = wave.open('/home/jim/Desktop/hello_out.wav' ,'wb')
    #     outfile.setparams(params)
    #     outfile.writeframes(in_data)
    #     print('Done')
    #     # a = DialogflowApi()
    #     # r = a.audio_query(in_data)
    #     # response = r.json()
    #     # out_data = response['result']['fulfillment']['speech']
    #     #
    #     # c.execute('INSERT INTO chat VALUES (?, ?)', [in_data, out_data])
    #     # conn.commit()
    #     #
    #     # await websocket.send(out_data)

def start_server():
    host = 'localhost'
    port = 8765
    server = websockets.serve(ws_server, host, port)
    print('start listening at {}:{}'.format(host, port))

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_server()
