import time
import json
from dialogflow_api.dialogflow_v2 import DialogflowApi


data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}

level_map = {
    'opentable.main': 2000
}


def opentable(data):
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

    w = DialogflowApi(session_id=data_json['header'][0])
    response = w.text_query(query)
    data = response.json()

    try:
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    except KeyError:
        data_format['data']['speech'] = 'KeyError'

    if data['queryResult']['intent']['displayName'] == 'opentable.homepage':
        data_format['header'][3] = 100
    data_format['data']['entity'] = data['queryResult']['parameters']
    return json.dumps(data_format)
