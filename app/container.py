import json
import time
import logging
from subprocess import getoutput
from main import MIC
from dialogflow_api.dialogflow_v2 import DialogflowApi

dflogger = logging.getLogger(__name__)


class Container:

    def __init__(self, data):
        self._gcloud = getoutput("gcloud config set project container-a3c3c")
        self._data = data
        self._query = ''
        self._header = ''
        self._speech = 'Default Container Message'
        self._entity = ''

    def in_data_helper(self):
        j = json.loads(self._data)
        if 'query' in j['data']:
            self._query = j['data']['query']
        else:
            self._query = ''
        self._header = j['header']
        return

    @classmethod
    def phone_format(cls, n):
        return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

    def insert_destination(self, dest):
        return self._header.insert(3, dest)

    @classmethod
    def valid_phone_number(cls, number):
        if number:
            if len(number) != 10:
                return False
            if not str.isalnum(number):
                return False
        return True

    def get_dest_lvl(self):
        self.in_data_helper()
        c = DialogflowApi(session_id=self._header[0])
        start = time.time()
        response = c.text_query(self._query)
        end = time.time()
        dflogger.debug('response time: {}'.format(end - start))
        data = response.json()
        print(data)
        if 'error' in data:
            print('Dialogflow request fail')
            return ''

        dflogger.debug(data)

        try:
            self._speech = data['queryResult']['fulfillmentText']
            d = self._header[2]
            self._header[3] = int(time.time())
            self._header[5] = len(data['queryResult']['fulfillmentText'])
            self._entity = data['queryResult']['parameters']
        except KeyError:
            print('Dialogflow API has some problem')

        try:
            if data['queryResult']['intent']['displayName'] == 'container.opentable':
                d = 2000
            if data['queryResult']['intent']['displayName'] == 'container.phone':
                d = 3000
            if data['queryResult']['intent']['displayName'] == 'container.phone - yes':
                d = 3100
                self._entity = {'phone-number': data['queryResult']['fulfillmentText']}
                self._speech = 'Okay'
            if data['queryResult']['intent']['displayName'] == 'container.phone - no':
                d = 3000
            if data['queryResult']['intent']['displayName'] == 'container.text':
                d = 4000
                MIC[self._header[0]]['context'] = 'phone_number'
            if data['queryResult']['intent']['displayName'] == 'container.stopmusic':
                d = 420
            if data['queryResult']['intent']['displayName'] == 'container.text - yes - custom - yes':
                d = 4100
                t = data['queryResult']['fulfillmentText'].split(' ')
                self._entity = {'phone-number': t[0], 'any': ' '.join(t[1:])}
                self._speech = 'Okay, message sent'
            if data['queryResult']['intent']['displayName'] == 'container.homepage':
                d = 100
            if data['queryResult']['intent']['displayName'] == 'container.micoff':
                MIC[self._header[0]]['mic_off'] = True
                MIC[self._header[0]]['state'] = self.out_data_helper()
                d = 400

            if data['queryResult']['allRequiredParamsPresent']:
                if data['queryResult']['intent']['displayName'] == 'container.phone':
                    d = 3000
                    self._entity = data['queryResult']['parameters']
                    self._speech = 'Okay is your phone number {}'.format(
                        self.phone_format(data['queryResult']['parameters']['phone-number']))

                if data['queryResult']['intent']['displayName'] == 'container.music' and \
                        data['queryResult']['parameters']['music-app'] == 'Spotify':
                    d = 5100
                if data['queryResult']['intent']['displayName'] == 'container.music' and \
                        data['queryResult']['parameters']['music-app'] == 'Pandora':
                    d = 6100
                if data['queryResult']['intent']['displayName'] == 'container.navigation' and \
                        data['queryResult']['parameters']['nav-app'] == 'Waze':
                    d = 1000
                    if data['queryResult']['parameters']['any']:
                        d = 1100
                        from .waze import remove_stopwords
                        self._entity = {'search': remove_stopwords(data['queryResult']['parameters']['any'])}

                if data['queryResult']['intent']['displayName'] == 'container.navigation' and \
                        data['queryResult']['parameters']['nav-app'] == 'Google map':
                    d = 7000
                    if data['queryResult']['parameters']['any']:
                        d = 7100
        except KeyError:
            pass

        self.insert_destination(d)
        return self.out_data_helper()

    def out_data_helper(self):
        out = dict()
        out['header'] = self._header
        out['data'] = {}
        out['data']['speech'] = self._speech
        out['data']['entity'] = self._entity
        return json.dumps(out)
