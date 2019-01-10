import time
import json
import logging
import datetime
from dialogflow_api.dialogflow_v2 import DialogflowApi

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}


def gmap(data):
    data_json = json.loads(data)

    print(data)
    try:
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    g = DialogflowApi(session_id=data_json['header'][0])
    response = g.text_query(query)
    data = response.json()

    try:
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    except KeyError:
        data_format['data']['speech'] = 'No Talk back implemented'

    try:
        '''
        TODO: Create a helper function to handle all report request 
        '''
        if data['queryResult']['intent']['displayName'] == 'gmap.stop':
            data_format['header'][3] = 7000
        if data['queryResult']['intent']['displayName'] == 'gmap.nav.fav':
            data_format['header'][3] = 7100
        if data['queryResult']['intent']['displayName'] == 'gmap.homepage':
            data_format['header'][3] = 100
    except KeyError:
        print('intent Key Error')

    try:
        if data['queryResult']['allRequiredParamsPresent']:
            if data['queryResult']['intent']['displayName'] == 'gmap.nav':
                data_format['header'][3] = 7100

    except KeyError:
        print('Required Params not shown')
        pass

    return json.dumps(data_format)
