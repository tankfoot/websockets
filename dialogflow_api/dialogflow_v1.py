import os
import requests
import json

class DialogflowApi:
    '''
    Interface to dialogflow api request
    '''

    def __init__(self, developer_token=None, client_token=None):
        self._developer_token = developer_token
        self._client_token = client_token
        self.version = '20150910'
        self._base_url = 'https://api.dialogflow.com/v1/'

    '''Header Handling'''
    @property
    def _dev_header(self):
        if self._developer_token is None:
            raise ValueError('No Dialogflow dev_token set. Please set DEV_ACCESS_TOKEN as enviornment variable')
        return {'Authorization': 'Bearer {}'.format(self._developer_token),
                'Content-Type': 'application/json'}

    @property
    def _client_header(self):
        if self._client_token is None:
            raise ValueError('No Dialogflow client_token set.Please set CLIENT_ACCESS_TOKEN as enviornment variable')
        return {'Authorization': 'Bearer {}'.format(self._client_token),
                'Content-Type': 'application/json; charset=utf-8'}

    '''Url handling'''
    @property
    def _query_url(self):
        return '{}query?v={}'.format(self._base_url, self.version)

    def _intent_url(self, intent_id=''):
        if intent_id:
            intent_id = '/' + intent_id
        return '{}intents{}?v={}'.format(self._base_url, intent_id, self.version)

    def _entity_url(self, entity_id = ''):
        if entity_id:
            entity_id = '/' + entity_id
        return '{}entities{}?v={}'.format(self._base_url, entity_id, self.version)

    '''JSON Requests and Response'''
    def _json_get(self, endpoint):
        response = requests.get(endpoint, headers=self._dev_header)
        logger.debug('Response from {}: {}'.format(endpoint, response))
        return response.json()

    def _json_post(self, endpoint, data):
        response = requests.post(endpoint, headers=self._dev_header, data=json.dumps(data))
        return response.json()

    def _json_put(self, endpoint, data):
        response = requests.put(endpoint, headers=self._dev_header, data=json.dumps(data))
        return response.json()

    '''Query '''
    def post_query(self, query, sessionID='123'):
        data = {
            "contexts": [],
            "lang": "en",
            "query": query,
            "sessionId": sessionID,
            "timezone": "America/San_Francisco"
        }
        response = requests.post(self._query_url,
            headers=self._client_header, data=json.dumps(data))
        return response

    '''Intents'''
    def post_intent(self, intent_json):
        #Create a new intent
        return self._json_post(self._intent_url(), data=intent_json)

    def put_intent(self, intent_id, intent_json):
        #Update an existing intent with intent_id
        return self._json_put(self._intent_url(intent_id), data=intent_json)

    '''Entities'''
    def post_entity(self, entity_json):
        #Create a new entity
        return self._json_post(self._entity_url(), data=entity_json)

    def put_entity(self, entity_id, entity_json):
        #Update an existing entity with entity_id
        return self._json_put(self._entity_url(entity_id), data=entity_json)
