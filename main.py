import json
from subprocess import getoutput


agent_list = {
    'Voiceplay': 'con'
}


def manager(data):
    """
    :type data: String
    :rtype: String
    """
    data_json = json.loads(data)

    if data_json['header'][1] == 0 or \
            data_json['header'][1] == 5 or \
            data_json['header'][1] == 6:
        try:
            from app.container import container
            getoutput("gcloud config set project container-a3c3c")
            result = container(data)
        except ImportError:
            raise ImportError('Import container fail')

    elif data_json['header'][1] == 1:
        try:
            from app.waze import waze
            getoutput("gcloud config set project maps-75922")
            result = waze(data)
        except ImportError:
            raise ImportError('Import Waze fail')

    elif data_json['header'][1] == 2:
        try:
            from app.opentable import opentable
            getoutput("gcloud config set project open-table-2")
            result = opentable(data)
        except ImportError:
            raise ImportError('Import OpenTable fail')

    elif data_json['header'][1] == 3:
        try:
            from app.container import container
            getoutput("gcloud config set project container-a3c3c")
            result = container(data)
        except ImportError:
            raise ImportError('Import container fail')

    elif data_json['header'][1] == 4:
        try:
            from app.container import container
            getoutput("gcloud config set project container-a3c3c")
            result = container(data)
        except ImportError:
            raise ImportError('Import container fail')

    elif data_json['header'][1] == 7:
        try:
            from app.gmap import gmap
            getoutput("gcloud config set project gmap-74a30")
            result = gmap(data)
        except ImportError:
            raise ImportError('Import gmap fail')

    else:
        print('level not implemented yet')
        result = data
    return result
