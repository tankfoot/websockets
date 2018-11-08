from core import Machine
from dialogflow_v2 import DialogflowApi
import json
import time

data_format = {
                'header':[0, 0, 0, 0, int(time.time()), 3, 0],
                'data':{
                        'speech': None,
                        'entity': None
                }
}

class Waze(object):
    pass


user = Waze()

states = ['first', 'second', 'third', 'fourth']

transitions = [
    {'trigger': 'navigation', 'source': 'first', 'dest': 'second'},
    {'trigger': 'navigation_cancel', 'source': 'second', 'dest': 'first'}
]


machine = Machine(model=user, states=states, transitions=transitions, initial='first')


def manager(data):
    """
    :type data: String
    :rtype: String
    """

    print(data)
    data_json = json.loads(data)

    try:
        header = data_json['header']
        print(header)
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    a = DialogflowApi()
    response = a.text_query(query)
    print(response.json())

    data = response.json()

    try:
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    except KeyError:
        data_format['data']['speech'] = 'KeyError'

    if data['queryResult']['intent']['displayName'] == 'waze.nav.explicit':
        data_format['header'][3] = 2000

    try:
        data_format['data']['entity'] = data['queryResult']['parameters']
    except KeyError:
        print('No Entity detected')

    return json.dumps(data_format)