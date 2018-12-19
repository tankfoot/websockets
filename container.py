import json
import time
from dialogflow_v2 import DialogflowApi

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}


def container(data):
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

    c = DialogflowApi(session_id=data_json['header'][0])
    response = c.text_query(query)
    data = response.json()

    data_format['data']['speech'] = data['queryResult']['fulfillmentText']
    data_format['header'][6] = len(data['queryResult']['fulfillmentText'])

    try:
        if data['queryResult']['intent']['displayName'] == 'container.navigation':
            data_format['header'][3] = 1000
        if data['queryResult']['intent']['displayName'] == 'container.opentable':
            data_format['header'][3] = 2000
        if data['queryResult']['intent']['displayName'] == 'container.phone':
            data_format['header'][3] = 3000
        if data['queryResult']['intent']['displayName'] == 'container.text':
            data_format['header'][3] = 4000
        if data['queryResult']['intent']['displayName'] == 'container.music':
            data_format['header'][3] = 5000
        if data['queryResult']['allRequiredParamsPresent']:
            pass
    except KeyError:
        print('intent Key Error')

    data_format['data']['entity'] = data['queryResult']['parameters']
    return json.dumps(data_format)
