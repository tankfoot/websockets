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
                        'entity': {}
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
    filtered_token = [w for w in sentence_token if not w in stopwords]
    filtered_sentence = ' '.join(filtered_token)

    return filtered_sentence

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
        if data['queryResult']['intent']['displayName'] == 'waze.any':
            data_format['header'][3] = 1100
        if data['queryResult']['intent']['displayName'] == 'waze.stop':
            data_format['header'][3] = 1000
        if data['queryResult']['allRequiredParamsPresent']:
            if data['queryResult']['intent']['displayName'] == 'waze.addstop':
                data_format['header'][3] = 1010
            if data['queryResult']['intent']['displayName'] == 'waze.choose':
                data_format['header'][3] = 1100
    except KeyError:
        print('intent Key Error')
    
    try:
        entity_all = data['queryResult']['parameters']
        data_format['data']['entity'] = {}
        for k, v in entity_all.items():
            if v:
                data_format['data']['entity'][k] = v
                if k == 'any':
                    data_format['data']['entity']['search'] = remove_stopwords(data_format['data']['entity']['any'])
                    del data_format['data']['entity']['any']

    except KeyError:
        print('No Entity detected')

    return json.dumps(data_format)
