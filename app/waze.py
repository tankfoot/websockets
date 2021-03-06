import time
import json
import logging
from subprocess import getoutput
from dialogflow_api.dialogflow_v2 import DialogflowApi

dflogger = logging.getLogger(__name__)

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}

GLOBAL_VAR = 1000
GLOBAL_OPENTABLE = 0
GLOBAL_MUSIC = 0
GLOBAL_PHONE = 0
GLOBAL_TEXT = 0
GLOBAL_RESPONSE = ''

level_map = {
    'waze.main': 1000,
    'waze.report': 1020,
    'waze.navigation': 1100,
    'waze.addstop': 1200


}

"""
TODO: Maintain the list in a new module inside Waze
"""
stopwords = {'themselves', 't', 'why', 'o', 'into', 'to', 'her', "should've",
             'when', 'ours', 're', 'other', 'doesn', "hadn't", 'ourselves',
             'its', 'it', 'are', 'because', 'more', "you've", 'be', 'your',
             'that', 'will', 'how', 'after', 'our', 'at', 'm', 'yourself',
             'his', 'any', 'where', 'she', "you'd", 'has', 'wouldn', 'each',
             'up', 'myself', 'theirs', 'what', 'couldn', 'above', 'shan',
             'by', 'y', 'but', "isn't", "it's", 'only', 'these', 'further',
             'haven', 'their', "weren't", "wasn't", 'who', 'wasn', 'doing',
             'while', 'off', 'some', 'over', 'own', 'himself', 'them', 'hasn',
             'down', 'am', 'won', 'hadn', 'didn', 'did', 'for', 'mustn',
             'through', 'having', 'than', 'about', 'which', 'should', 'been',
             'few', "aren't", 'my', 'we', "won't", 'i', 'with', 'don', "you're",
             'this', 'needn', 'during', 'an', 'until', 'very', 'from', 'herself',
             'or', 'once', 'no', 'such', "you'll", 'the', 'so', 'hers', 'was',
             "shouldn't", 'a', 'under', 'they', 'do', 'both', 'not', 'against',
             's', 'on', 'same', 'most', 'too', 'just', 've', "mightn't", 'before',
             'here', 'in', 'out', 'then', 'as', 'being', 'nor', 'mightn', 'he', 'ma',
             "needn't", 'now', 'yours', 'and', 'below', 'is', 'yourselves', 'aren',
             "mustn't", 'd', 'itself', 'him', 'me', "wouldn't", 'if', "shan't", "she's",
             'does', "didn't", 'you', "don't", 'ain', 'can', "hasn't", 'there', 'weren',
             "couldn't", 'were', 'whom', 'of', "haven't", 'have', 'shouldn', "doesn't",
             'all', 'those', 'isn', 'again', 'had', 'between', 'll', "that'll"}


def remove_stopwords(sentence):
    sentence_token = sentence.split(' ')
    filtered_token = [w for w in sentence_token if w not in stopwords]
    filtered_sentence = ' '.join(filtered_token)

    return filtered_sentence


def entity_formatter():
    favourite = ['home', 'work']
    fallback = ['cancel', 'stop', 'cancel navigation', 'stop navigation']
    try:
        if data_format['data']['entity']['any'] in favourite:
            data_format['header'][3] = 1100
            data_format['data']['entity']['favourite'] = data_format['data']['entity']['any']
            del data_format['data']['entity']['any']
        elif data_format['data']['entity']['any'] in fallback:
            data_format['header'][3] = 1000
            del data_format['data']['entity']['any']
            data_format['data']['speech'] = "Cancelled"
        else:
            data_format['header'][3] = 1100
            data_format['data']['entity']['search'] = remove_stopwords(data_format['data']['entity']['any'])
            del data_format['data']['entity']['any']
    except KeyError:
        print('No Entity detected')

    return


def waze(d):
    data_json = json.loads(d)
    global GLOBAL_VAR, GLOBAL_OPENTABLE, GLOBAL_PHONE, GLOBAL_MUSIC, GLOBAL_RESPONSE, GLOBAL_TEXT
    try:
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    w = DialogflowApi(session_id=data_json['header'][0])
    response = w.text_query(query)
    data = response.json()

    dflogger.debug(data)

    try:
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
        data_format['data']['entity'] = data['queryResult']['parameters']
    except KeyError:
        data_format['data']['speech'] = 'No Talk back implemented'

    try:
        '''
        TODO: Create a helper function to handle all report request 
        '''
        if data['queryResult']['intent']['displayName'] == 'waze.report':
            data_format['header'][3] = 1020
            GLOBAL_VAR = data_format['header'][2]
        if data['queryResult']['intent']['displayName'] == 'waze.report_police':
            data_format['header'][3] = 1020
            if data_format['header'][2] != 1020:
                GLOBAL_VAR = data_format['header'][2]
        if data['queryResult']['intent']['displayName'] == 'waze.report_traffic':
            data_format['header'][3] = 1020
            if data_format['header'][2] != 1020:
                GLOBAL_VAR = data_format['header'][2]
        if data['queryResult']['intent']['displayName'] == 'waze.report_crash':
            data_format['header'][3] = 1020
            if data_format['header'][2] != 1020:
                GLOBAL_VAR = data_format['header'][2]
        if data['queryResult']['intent']['displayName'] == 'waze.report_camera':
            data_format['header'][3] = 1020
            if data_format['header'][2] != 1020:
                GLOBAL_VAR = data_format['header'][2]

        if data['queryResult']['intent']['displayName'] == 'Default Fallback Intent':
            getoutput('gcloud config set project container-a3c3c')
            c = DialogflowApi(session_id=data_json['header'][0])
            response = c.text_query(query)
            data2 = response.json()
            dflogger.debug(data2)

            if data2['queryResult']['intent']['displayName'] == 'container.opentable':
                data_format['data']['speech'] = 'Do you want to switch to OpenTable?'
                GLOBAL_OPENTABLE = 1
                GLOBAL_RESPONSE = data2['queryResult']['fulfillmentText']
            if data2['queryResult']['intent']['displayName'] == 'container.phone':
                data_format['data']['speech'] = 'Do you want to switch to phone call?'
                GLOBAL_RESPONSE = data2['queryResult']['fulfillmentText']
                GLOBAL_PHONE = 1
            if data2['queryResult']['intent']['displayName'] == 'container.text':
                data_format['data']['speech'] = 'Do you want to switch to text message?'
                GLOBAL_RESPONSE = data2['queryResult']['fulfillmentText']
                GLOBAL_TEXT = 1

            if data2['queryResult']['intent']['displayName'] == 'container.music':
                data_format['header'][3] = 100
                data_format['data']['speech'] = data2['queryResult']['fulfillmentText']

            if data2['queryResult']['allRequiredParamsPresent']:
                if data2['queryResult']['intent']['displayName'] == 'container.music' and \
                        data2['queryResult']['parameters']['music-app'] == 'Spotify':
                    data_format['header'][3] = 5100
                    data_format['data']['speech'] = data2['queryResult']['fulfillmentText']
                if data2['queryResult']['intent']['displayName'] == 'container.music' and \
                        data2['queryResult']['parameters']['music-app'] == 'Pandora':
                    data_format['header'][3] = 6100
                    data_format['data']['speech'] = data2['queryResult']['fulfillmentText']

            if data2['queryResult']['intent']['displayName'] == 'container.stopmusic':
                data_format['header'][3] = 420
                data_format['data']['speech'] = data2['queryResult']['fulfillmentText']

            if data2['queryResult']['intent']['displayName'] == 'container.reminders':
                data_format['header'][3] = 100
                data_format['data']['speech'] = data2['queryResult']['fulfillmentText']

            if data2['queryResult']['intent']['displayName'] == 'container.micoff':
                data_format['header'][3] = 400
                from main import MIC
                MIC[data_format['header'][0]]['mic_off'] = True
                MIC[data_format['header'][0]]['state'] = json.dumps(data_format)
                data_format['data']['speech'] = data2['queryResult']['fulfillmentText']

        if GLOBAL_OPENTABLE == 1 and data['queryResult']['intent']['displayName'] == 'waze.yes':
            data_format['header'][3] = 2000
            data_format['data']['speech'] = GLOBAL_RESPONSE
            GLOBAL_OPENTABLE = 0

        if GLOBAL_OPENTABLE == 1 and data['queryResult']['intent']['displayName'] == 'waze.no':
            data_format['data']['speech'] = 'Sure, Stay Waze'
            GLOBAL_OPENTABLE = 0

        if GLOBAL_PHONE == 1 and data['queryResult']['intent']['displayName'] == 'waze.yes':
            data_format['header'][3] = 3000
            data_format['data']['speech'] = GLOBAL_RESPONSE
            GLOBAL_PHONE = 0

        if GLOBAL_PHONE == 1 and data['queryResult']['intent']['displayName'] == 'waze.no':
            data_format['data']['speech'] = 'Sure, Stay Waze'
            GLOBAL_PHONE = 0

        if GLOBAL_TEXT == 1 and data['queryResult']['intent']['displayName'] == 'waze.yes':
            data_format['header'][3] = 4000
            data_format['data']['speech'] = GLOBAL_RESPONSE
            GLOBAL_TEXT = 0

        if GLOBAL_OPENTABLE == 1 and data['queryResult']['intent']['displayName'] == 'waze.no':
            data_format['data']['speech'] = 'Sure, Stay Waze'
            GLOBAL_TEXT = 0

        if GLOBAL_MUSIC == 1 and data['queryResult']['intent']['displayName'] == 'waze.yes':
            data_format['header'][3] = 100
            data_format['data']['speech'] = GLOBAL_RESPONSE
            GLOBAL_MUSIC = 0

        if GLOBAL_MUSIC == 1 and data['queryResult']['intent']['displayName'] == 'waze.no':
            data_format['data']['speech'] = 'Sure, Stay Waze'
            GLOBAL_MUSIC = 0

        '''
        TODO: Create a list of Dialogflow intents will go to navigation page
        '''
        if data['queryResult']['intent']['displayName'] == 'waze.stop - yes':
            data_format['header'][3] = 1000
            data_format['data']['entity'] = {'stop_navigation': 'yes'}

        if data['queryResult']['intent']['displayName'] == 'waze.homepage':
            data_format['header'][3] = 100

        if data['queryResult']['intent']['displayName'] == 'waze.addstop':
            if data_json['header'][2] == 1200:
                data_format['data']['speech'] = 'Sorry, Waze can only add one stop.'
                w.delete_context()
            entity_formatter()
            data_format['header'][3] = 1010
        if data['queryResult']['intent']['displayName'] == 'waze.choose':
            data_format['header'][3] = 1100
    except KeyError:
        print('intent Key Error')

    try:
        if data['queryResult']['allRequiredParamsPresent']:
            if data['queryResult']['intent']['displayName'] == 'waze.navigation':
                entity_formatter()
            if data['queryResult']['intent']['displayName'] == 'waze.report_police':
                data_format['header'][3] = GLOBAL_VAR
            if data['queryResult']['intent']['displayName'] == 'waze.report_traffic':
                data_format['header'][3] = GLOBAL_VAR
            if data['queryResult']['intent']['displayName'] == 'waze.report_crash':
                data_format['header'][3] = GLOBAL_VAR
            if data['queryResult']['intent']['displayName'] == 'waze.report_camera':
                data_format['header'][3] = GLOBAL_VAR
    except KeyError:
        print('Required Params not shown')
        pass

    return json.dumps(data_format)
