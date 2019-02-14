import json
from subprocess import getoutput
from app import container

gcloudProjectID = {
    'Container': 'container-2b060',
    'Waze': 'waze-11f7f',
    'GoogleMap': 'gmap-3ffaa',
    'OpenTable': 'opentable-cf3e6'
}


def manager(data):
    """
    :type data: String
    :rtype: String
    """
    data_json = json.loads(data)

    if data_json['header'][0] not in container.MIC:
        if 'query' not in data_json['data']:
            return ''

        if data_json['header'][1] == 0 or \
                data_json['header'][1] == 5 or \
                data_json['header'][1] == 6:
            try:
                from app.container import Container
                a = Container(data)
                result = a.get_dest_lvl()
            except ImportError:
                raise ImportError('Import container fail')

        elif data_json['header'][1] == 1:
            try:
                from app.waze import waze
                getoutput("gcloud config set project {}".format(gcloudProjectID['Waze']))
                result = waze(data)
            except ImportError:
                raise ImportError('Import Waze fail')

        elif data_json['header'][1] == 2:
            try:
                from app.opentable import opentable
                getoutput("gcloud config set project {}".format(gcloudProjectID['OpenTable']))
                result = opentable(data)
            except ImportError:
                raise ImportError('Import OpenTable fail')

        elif data_json['header'][1] == 3:
            try:
                from app.container import Container
                a = Container(data)
                result = a.get_dest_lvl()
            except ImportError:
                raise ImportError('Import container fail')

        elif data_json['header'][1] == 4:
            try:
                from app.container import Container
                a = Container(data)
                result = a.get_dest_lvl()
            except ImportError:
                raise ImportError('Import container fail')

        elif data_json['header'][1] == 7:
            try:
                from app.gmap import gmap
                getoutput("gcloud config set project {}".format(gcloudProjectID['GoogleMap']))
                result = gmap(data)
            except ImportError:
                raise ImportError('Import gmap fail')

        else:
            print('level not implemented yet')
            result = data
    else:
        command = ['start mic', 'start microphone', 'turn on mic', 'turn on microphone',
                   'start the microphone', 'star microphone']

        if 'query' not in data_json['data']:
            del container.MIC[data_json['header'][0]]
            return ''

        if 'microphone' in data_json['data']['query']:
            j = json.loads(container.MIC[data_json['header'][0]])
            j['header'].insert(3, 410)
            j['data']['speech'] = 'Welcome back'
            result = json.dumps(j)
            del container.MIC[j['header'][0]]
        else:
            result = ''
    return result
