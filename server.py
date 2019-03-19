#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import logging
import json
import os
from utils.log_utils import setup_logging
import time
import datetime
import base64
import wave
from dialogflow_api.dialogflow_v2 import DialogflowApi
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
logging.getLogger("websockets").setLevel(logging.ERROR)
setup_logging(default_path='utils/logging.json')

connected = set()
USER = {1111: {'buffer': []}
        }


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

    responses = client.recognize(config, audio)

    return responses


def print_response_buffer(r):
    for result in r.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript


def register(data):
    init_data = json.loads(data)
    USER[init_data['header'][0]] = {'info': data}
    USER[init_data['header'][0]]['mic_off'] = False
    a = DialogflowApi(session_id=init_data['header'][0])
    USER[init_data['header'][0]]['df_v2'] = a
    USER[init_data['header'][0]]['buffer'] = []
    if not os.path.exists('output/{}'.format(init_data['header'][0])):
        os.makedirs('output/{}'.format(init_data['header'][0]))
    print('register finish')


async def ws_server(ws, path):

    while True:
        try:
            async for message in ws:
                d = json.loads(message)
                if 'audio' in d['data']:
                    USER[d['header'][0]]['buffer'].append(base64.b64decode(d['data']['audio']))
                else:
                    register(message)
                    break

                if d['header'][6] == 0:
                    out = d
                    start1 = time.time()
                    responses = speech_api_stream(USER[d['header'][0]]['buffer'])
                    res = print_response_stream(responses)
                    start2 = time.time()
                    print('ASR delay: {}'.format(round((start2 - start1), 4)))

                    if res:
                        out['data']['query'] = res
                        del out['header'][6]
                        del out['data']['audio']
                        logging.info(out)
                        state_init(json.dumps(out))
                        start3 = time.time()
                        out_data = manager(json.dumps(out))
                        start4 = time.time()
                        print('Dialogflow delay: {}'.format(round((start4 - start3), 4)))
                        logging.info(out_data)
                        await ws.send(out_data)

                    else:
                        pass

                    with wave.open(f"output/{d['header'][0]}/{res}.wav", mode='wb') as f:
                        f.setnchannels(1)
                        f.setsampwidth(2)
                        f.setframerate(16000)
                        f.writeframes(b''.join(USER[d['header'][0]]['buffer']))
                        USER[d['header'][0]]['buffer'] = []

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

