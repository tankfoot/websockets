#!/usr/bin/env python

import wave
import asyncio
import websockets

block_size = 128
sent_count = 0
infile = wave.open('/home/jim/Desktop/hello.wav', 'rb')
sample_width = infile.getsampwidth()
params = infile.getparams()

print('block_size: {}, sample_width: {}'.format(block_size, sample_width))

async def query():
    async with websockets.connect('ws://localhost:8765') as ws:

        with wave.open('/home/jim/Desktop/hello.wav', 'rb') as in_file:
            for l in in_file:
                await websockets.sendall(l)
                
        receive = await websockets.recv()
        print(f"< {receive}")

asyncio.get_event_loop().run_until_complete(query())
