import json
import time
from dialogflow_api.dialogflow_v2 import DialogflowApi

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}

level_map = {
    'container.navigation': 1000,
    'container.opentable': 2000,
    'container.phone': 3000,
    'container.phone.done': 3100,
    'container.text.done': 4100,
    'container.text': 4000,
    'container.music': 5000
}

GLOBAL_VAR_PHONE = ""
GLOBAL_VAR_TEXT = ""


def phone_format(n):
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]


def container(data):
    data_json = json.loads(data)
    global GLOBAL_VAR_PHONE
    global GLOBAL_VAR_TEXT
    print(data)
    '''
    TODO: Error handling
    '''
    try:
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    c = DialogflowApi(session_id=data_json['header'][0])
    response = c.text_query(query)
    data = response.json()

    '''
    TODO: text pre process if not recognize
    '''
    data_format['data']['speech'] = data['queryResult']['fulfillmentText']
    data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    data_format['data']['entity'] = data['queryResult']['parameters']

    try:
        if data['queryResult']['intent']['displayName'] == 'container.opentable':
            data_format['header'][3] = 2000
        if data['queryResult']['intent']['displayName'] == 'container.phone':
            data_format['header'][3] = 3000
            GLOBAL_VAR_PHONE = data['queryResult']['parameters']
        if data['queryResult']['intent']['displayName'] == 'container.phone - yes':
            data_format['header'][3] = 3100
            data_format['data']['entity'] = GLOBAL_VAR_PHONE
        if data['queryResult']['intent']['displayName'] == 'container.phone - no':
            data_format['header'][3] = 100
        if data['queryResult']['intent']['displayName'] == 'container.text':
            data_format['header'][3] = 4000
            GLOBAL_VAR_TEXT = data['queryResult']['parameters']
        if data['queryResult']['intent']['displayName'] == 'container.text - send':
            data_format['header'][3] = 4100
            data_format['data']['entity'] = GLOBAL_VAR_TEXT
        if data['queryResult']['intent']['displayName'] == 'container.homepage':
            data_format['header'][3] = 100
    except KeyError:
        print('intent Key Error')

    try:
        if data['queryResult']['allRequiredParamsPresent']:
            if data['queryResult']['intent']['displayName'] == 'container.phone':
                data_format['header'][3] = 3000
                GLOBAL_VAR_PHONE = data['queryResult']['parameters']
                data_format['data']['speech'] = 'Okay is your phone number {}'.format(
                    phone_format(data['queryResult']['parameters']['phone-number']))

            if data['queryResult']['intent']['displayName'] == 'container.music' and \
                    data['queryResult']['parameters']['music-app'] == 'Spotify':
                data_format['header'][3] = 5000
            if data['queryResult']['intent']['displayName'] == 'container.music' and \
                    data['queryResult']['parameters']['music-app'] == 'Pandora':
                data_format['header'][3] = 6000
            if data['queryResult']['intent']['displayName'] == 'container.navigation' and \
                    data['queryResult']['parameters']['nav-app'] == 'Waze':
                data_format['header'][3] = 1000
            if data['queryResult']['intent']['displayName'] == 'container.navigation' and \
                    data['queryResult']['parameters']['nav-app'] == 'Google map':
                data_format['header'][3] = 7000
    except KeyError:
        pass

    return json.dumps(data_format)
