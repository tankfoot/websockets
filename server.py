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
import wave
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


def speech_api_stream(stream):

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


def print_response_stream(r):
    for response in r:
        for result in response.results:
            #print('Finished: {}'.format(result.is_final))
            #print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                #print('Confidence: {}'.format(alternative.confidence))
                #print(u'Transcript: {}'.format(alternative.transcript))
                return alternative.transcript


def speech_api_buffer(buffer):

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(content=b''.join(buffer))

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    responses = client.streaming_recognize(config, audio)

    return responses


def print_response_buffer(r):
    for result in r.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript


async def ws_server(ws, path):

    stream = []
    while True:
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
                    print('start1: {}'.format(time.time()))
                    responses = speech_api_buffer(stream)
                    print('start2: {}'.format(time.time()))

                    res = print_response_buffer(responses)

                    print('start3: {}'.format(time.time()))

                    if res:
                        out['data']['query'] = res
                        del out['header'][6]
                        del out['data']['audio']
                        print(out)
                        state_init(json.dumps(out))
                        print('start4: {}'.format(time.time()))
                        out_data = manager(json.dumps(out))
                        print('start5: {}'.format(time.time()))
                        print(out_data)
                        await ws.send(out_data)

                    else:
                        pass

                    print('Stop: {}'.format(time.time()))

                    with wave.open(f"output/{datetime.datetime.now():%Y-%m-%dT%H%M%S}_{res}.wav", mode='wb') as f:
                        f.setnchannels(1)
                        f.setsampwidth(2)
                        f.setframerate(16000)
                        f.writeframes(b''.join(stream))

                    stream = []

        except websockets.exceptions.ConnectionClosed:
            '''
            TODO: Logging.info
            '''
            print('user disconnected')
            break

            
start_server = websockets.serve(ws_server, 'localhost', 3456)
print('Start listening:')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

