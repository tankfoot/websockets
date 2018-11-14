#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import logging
import datetime
from main import manager

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def ws_server(ws, path):

    now = datetime.datetime.now()
    fh = logging.FileHandler('log/waze-{}'.format(now.strftime("%Y-%m-%d %H:%M:%S")))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    while True:
        try:
            in_data = await ws.recv()
            out_data = manager(in_data)
            logger.info(in_data)
            logger.info(out_data)
            await ws.send(out_data)
        
        except websockets.exceptions.ConnectionClosed:
            print('disconnected')
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
