#!/usr/bin/env python

# WS server example

import asyncio
import websockets

headers = {'controllerId': 0,
           'applicationId': 1
}

async def ws_server(ws, path):
    while True:
        try:
            in_data = await asyncio.wait_for(ws.recv(), timeout = 20)
        except asyncio.TimeoutError:
            #Check the connection in 20 seconds
            try:
                pong_waiter = await ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=10)
            except asyncio.TimeoutError:
                #No response to ping in 10 seconds, disconnect
                ws.send('disconnect')
                print('disconnect')
                break
        else:
            greeting = f"Hello {in_data}!"

            await ws.send(greeting)
            print(f"> {greeting}")

start_server = websockets.serve(ws_server, 'localhost', 8765, extra_headers = headers)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
