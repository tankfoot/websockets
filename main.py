from dialogflow_v2 import DialogflowApi
import json
import time
import datetime
import logging
from subprocess import getoutput

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

def manager(data):
    """
    :type data: String
    :rtype: String
    """
    logger.info(data)
    data_json = json.loads(data)

    try:
        query = data_json['data']['query']
        data_format['header'][0] = data_json['header'][0]
        data_format['header'][1] = data_json['header'][1]
        data_format['header'][2] = data_json['header'][2]
        data_format['header'][3] = data_json['header'][2]
    except KeyError:
        print('in_data: KeyError')

    if data_json['header'][1] == 0:
        getoutput("gcloud config set project container-a3c3c")
        container = DialogflowApi(session_id=data_json['header'][0])
        response = container.text_query(query)
        data = response.json()
        data_format['data']['speech'] = data['queryResult']['fulfillmentText']
        data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
        result = json.dumps(data_format)

    elif data_json['header'][1] == 1:
        try:
            from waze import waze
            getoutput("gcloud config set project maps-75922")
            result = waze(data)
            logger.info(result)
        except ImportError:
            raise ImportError('Import Waze fail')

    else:
        print('level Error')
    return result
