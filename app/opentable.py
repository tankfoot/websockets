import time
import json
#from dialogflow_api.dialogflow_v2 import DialogflowApi
from dialogflow_api.dialogflow_v1 import DialogflowApi

# data_format = {
#                 'header': [0, 0, 0, 0, int(time.time()), 3, 0],
#                 'data': {
#                         'speech': None,
#                         'entity': {}
#                 }
# }

data_format = {
                'UserId': None,
                'Time': None,
                'IntentId': None,
                'IntentName': None,
                'Context': None,
                'Speech': None,
                'Entity': None
}

level_map = {
    'opentable.main': 2000
}


def opentable(data):
    data_json = json.loads(data)
    print(data)
    try:
        query = data_json['data']['query']
        # data_format['header'][0] = data_json['header'][0]
        # data_format['header'][1] = data_json['header'][1]
        # data_format['header'][2] = data_json['header'][2]
        # data_format['header'][3] = data_json['header'][2]
    except KeyError:
        query = 'hi'
        print('in_data: KeyError')

    #w = DialogflowApi(session_id=data_json['header'][0])
    #response = w.text_query(query)
    #data = response.json()

##########OLD
    # a = DialogflowApi()
    # r = a.post_query(query)
    # response = r.json()
    #
    # data_format['UserId'] = data_json['header'][0]
    # data_format['Speech'] = response['result']['fulfillment']['speech']
    # if 'parameters' in response['result']:
    #     data_format['Entity'] = response['result']['parameters']
    # else:
    #     data_format['Entity'] = ""
    # if 'intentName' in response['result']['metadata']:
    #     data_format['IntentName'] = response['result']['metadata']['intentName']
    # else:
    #     data_format['IntentName'] = None
    #
    # for item in response['result']['contexts']:
    #     if 'name' in item:
    #         data_format['Context'] = response['result']['contexts'][0]['name']
    #         break
    # else:
    #     data_format['Context'] = None
    #
    # data_format['Time'] = response['timestamp']
    # if 'intentId' in response['result']['metadata']:
    #     data_format['IntentId'] = response['result']['metadata']['intentId']
    # else:
    #     data_format['IntentId'] = None

############OLD
    # try:
    #     data_format['data']['speech'] = data['queryResult']['fulfillmentText']
    #     data_format['header'][6] = len(data['queryResult']['fulfillmentText'])
    # except KeyError:
    #     data_format['data']['speech'] = 'KeyError'

    # if data['queryResult']['intent']['displayName'] == 'opentable.homepage':
    #     data_format['header'][3] = 100
    # data_format['data']['entity'] = data['queryResult']['parameters']
    return data
