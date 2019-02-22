import json
import time
from main import MIC
import logging

data_format = {
                'header': [0, 0, 0, 0, int(time.time()), 3, 0],
                'data': {
                        'speech': None,
                        'entity': {}
                }
}

logger = logging.getLogger(__name__)
yes = ['yes', 'correct', 'right']
no = ['no', 'wrong']
cancel = ['cancel']
homepage = ['homepage', 'home']


def valid_phone_number(number):
    number = number.replace('-', '')
    if number:
        if len(number) != 10:
            return False
        if not str.isalnum(number):
            return False
    return True


def text_message(data):
    in_data = json.loads(data)
    data_format['header'] = in_data['header']
    data_format['header'].insert(3, in_data['header'][2])
    query = in_data['data']['query']

    if 'context' not in MIC[in_data['header'][0]]:
        if 'home' in query:
            data_format['header'][3] = 100
            data_format['data']['entity'] = {}
            data_format['data']['speech'] = 'Okay, go back to homepage'
            return json.dumps(data_format)
        else:
            data_format['data']['speech'] = 'Sorry, I don\'t understand'
            return json.dumps(data_format)

    elif MIC[in_data['header'][0]]['context'] == 'phone_number':
            if query in cancel:
                data_format['data']['speech'] = 'okay, cancel sending message'
                data_format['header'][3] = 100
                del (MIC[in_data['header'][0]]['context'])
                return json.dumps(data_format)
            if not valid_phone_number(query):
                data_format['data']['speech'] = 'number not valid, what is the phone number?'
            else:
                data_format['data']['speech'] = 'Is your phone number {}'\
                    .format(query)
                data_format['data']['entity']['phone-number'] = query
                MIC[in_data['header'][0]]['context'] = 'phone_number_confirm'
            return json.dumps(data_format)
    elif MIC[in_data['header'][0]]['context'] == 'phone_number_confirm':
        if query in yes:
            data_format['data']['speech'] = 'what is your message?'
            MIC[in_data['header'][0]]['context'] = 'message'
            return json.dumps(data_format)
        elif query in no:
            data_format['data']['speech'] = 'what is your phone number?'
            MIC[in_data['header'][0]]['context'] = 'phone_number'
            return json.dumps(data_format)
        elif query in cancel:
            data_format['header'][3] = 100
            data_format['data']['speech'] = 'okay, cancel sending message'
            del (MIC[in_data['header'][0]]['context'])
            return json.dumps(data_format)
        else:
            data_format['data']['speech'] = 'Is your phone number {}'.format()
    elif MIC[in_data['header'][0]]['context'] == 'message':
        data_format['data']['speech'] = 'Is your message {}'.format(query)
        MIC[in_data['header'][0]]['context'] = 'message_confirm'
        data_format['data']['entity']['any'] = query
        return json.dumps(data_format)

    elif MIC[in_data['header'][0]]['context'] == 'message_confirm':
        if query in yes:
            data_format['data']['speech'] = 'Okay, send the message'
            del(MIC[in_data['header'][0]]['context'])
            data_format['header'][3] = 4100
            return json.dumps(data_format)
        elif query in no:
            data_format['data']['speech'] = 'what is your message'
            MIC[in_data['header'][0]]['context'] = 'message'
            return json.dumps(data_format)
        elif query in cancel:
            data_format['data']['speech'] = 'okay, cancel sending message'
            del (MIC[in_data['header'][0]]['context'])
            return json.dumps(data_format)
    else:
        return json.dumps(data_format)

