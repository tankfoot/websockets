#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import logging
import json
from utils.log_utils import setup_logging
import time
import datetime
import base64
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

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


def speech_api(stream):

    client = speech.SpeechClient()

    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
        single_utterance=False)

    responses = client.streaming_recognize(streaming_config, requests)

    return responses


def print_response(r):
    for response in r:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            #print('Finished: {}'.format(result.is_final))
            #print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                #print('Confidence: {}'.format(alternative.confidence))
                #print(u'Transcript: {}'.format(alternative.transcript))
                return alternative.transcript


async def ws_server(ws, path):

    stream = []
    try:
        async for message in ws:
            d = json.loads(message)
            if 'audio' in d['data']:
                stream.append(base64.b64decode(d['data']['audio']))
            else:
                state_init(message)
                manager(message)
                break

            if d['header'][6] == 0:
                out = d
                print(out)
                responses = speech_api(stream)

                start = time.time()
                res = print_response(responses)

                if res:
                    out['data']['query'] = res
                    del out['header'][6]
                    del out['data']['audio']
                    print(out)
                    state_init(json.dumps(out))
                    out_data = manager(json.dumps(out))
                    print(out_data)
                    await ws.send(out_data)

                else:
                    pass

                stop = time.time()

                with open(f"output/{datetime.datetime.now():%Y-%m-%dT%H%M%S}_{res}.pcm", mode='bx') as f:
                    for chunk in stream:
                        f.write(chunk)

                stream = []

                print("response time: {}".format(round(stop - start, 5)))

    except websockets.exceptions.ConnectionClosed:
        '''
        TODO: Logging.info
        '''
        print('user disconnected')

            
start_server = websockets.serve(ws_server, 'localhost', 3456)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

