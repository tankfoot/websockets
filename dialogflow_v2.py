import os
import requests
import json
from subprocess import getoutput
import base64

class DialogflowApi:
    '''
    Interface to dialogflow apiv2 request
    '''

    def __init__(self, auth_token=None, project_id=None, session_id='123'):
        self._auth_token = getoutput("gcloud auth application-default print-access-token")
        self._project_id = getoutput("gcloud config get-value project")
        self._base_url = 'https://dialogflow.googleapis.com/v2/'
        self._session_id = session_id

    '''Header Handling'''

    @property
    def _header(self):
        if self._auth_token is None:
            raise ValueError('No Dialogflow token set. Please install google cloud sdk')
        return {'Authorization': 'Bearer {}'.format(self._auth_token),
                'Content-Type': 'application/json; charset=utf-8'}

    '''Url handling'''
    @property
    def _query_url(self):
        if self._project_id is None:
            raise ValueError('No gcloud project opened.')
        return '{}projects/{}/agent/sessions/{}:detectIntent'.format(self._base_url, self._project_id, self._session_id)


    '''Query '''
    def text_query(self, query):
        data = {
            "queryInput": {
                "text": {
                    "text": query,
                    "languageCode": 'en'
                }
            }
        }
        response = requests.post(self._query_url, headers=self._header, data=json.dumps(data))
        return response

    def audio_query(self, path):
        with open(path, 'rb') as speech:
            # Base64 encode the binary audio file for inclusion in the JSON request.
            speech_content = base64.b64encode(speech.read()).decode('utf-8')
        data = {
            "queryInput": {
                "audioConfig": {
                    "audioEncoding": 'AUDIO_ENCODING_LINEAR_16',
                    "sampleRateHertz": 16000,
                    "languageCode": 'en-US'
                }
            },
            "inputAudio": speech_content
        }
        response = requests.post(self._query_url, headers=self._header, data=json.dumps(data))
        return response
