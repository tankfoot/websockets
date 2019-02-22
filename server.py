#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import logging
import json
from utils.log_utils import setup_logging
import time
from main import state_init
from main import manager

"""
TODO: logger module to clean logger code for each file
logging level
asyncoronize
"""

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
setup_logging(default_path='utils/logging.json')

connected = set()


async def ws_server(ws, path):

    connected.add(ws)
    print('current: ')
    print(connected)

    while True:
        try:
            in_data = await ws.recv()
            logging.info(in_data)
            state_init(in_data)
            out_data = manager(in_data)
            logger.info(out_data)
            await ws.send(out_data)
        
        except websockets.exceptions.ConnectionClosed:
            '''
            TODO: Logging.info
            '''
            print('{}: user disconnected'.format(int(time.time())))
            connected.remove(ws)
            print(connected)
            break
            
start_server = websockets.serve(ws_server, 'localhost', 8765)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

