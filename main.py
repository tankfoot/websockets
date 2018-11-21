from core import Machine
from dialogflow_v2 import DialogflowApi
import json
import time
import datetime
import logging

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': None
                }
}

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
now = datetime.datetime.now()
dffh = logging.FileHandler('dflog/waze-df-log')
dffh.setFormatter(formatter)
logger.addHandler(dffh)

level_map = {
    'mapView': 1000,
    'report': 1200,
    'report_traffic': 1210,
    'report_police': 1220,
    'report_crash': 1230,
    'report_hazard': 1240
}


class Waze(object):
    pass


user = Waze()

states = ['1000', '1100', '1200']

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
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    a = DialogflowApi(session_id=data_json['header'][0])
    response = a.text_query(query)
    data = response.json()
    logger.info(data)

    try:
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    except KeyError:
        data_format['data']['speech'] = 'KeyError'
    
    try:
        if data['queryResult']['intent']['displayName'] == 'waze.report':
            data_format['header'][3] = 1200
        if data['queryResult']['intent']['displayName'] == 'waze.nav.explicit':
            data_format['header'][3] = 1100
        if data['queryResult']['intent']['displayName'] == 'waze.stop':
            data_format['header'][3] = 1000
        if data['queryResult']['allRequiredParamsPresent']:
            if data['queryResult']['intent']['displayName'] == 'waze.report_police':
                data_format['header'][3] = 1300
            if data['queryResult']['intent']['displayName'] == 'waze.report_traffic':
                data_format['header'][3] = 1300
            if data['queryResult']['intent']['displayName'] == 'waze.report_crash':
                data_format['header'][3] = 1300
            if data['queryResult']['intent']['displayName'] == 'waze.location':
                data_format['header'][3] = 1100
            if data['queryResult']['intent']['displayName'] == 'waze.address':
                data_format['header'][3] = 1100
            if data['queryResult']['intent']['displayName'] == 'waze.city':
                data_format['header'][3] = 1100
    except KeyError:
        print('intent Key Error')
    
    try:
        data_format['data']['entity'] = data['queryResult']['parameters']
    except KeyError:
        print('No Entity detected')

    return json.dumps(data_format)
