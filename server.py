#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import logging
import time
from main import manager

"""
TODO: logger module to clean logger code for each file
logging level
asyncoronize
"""
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('log/manager.log')
fh.setFormatter(formatter)
logger.addHandler(fh)


async def ws_server(ws, path):

    while True:
        try:
            in_data = await ws.recv()
            logger.info(in_data)
            out_data = manager(in_data)
            logger.info(out_data)
            print(out_data)
            await ws.send(out_data)
        
        except websockets.exceptions.ConnectionClosed:
            '''
            TODO: Logging.info
            '''
            print('{}: user disconnected'.format(int(time.time())))
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765, timeout=1000)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
