import json
from subprocess import getoutput


def manager(data):
    """
    :type data: String
    :rtype: String
    """
    data_json = json.loads(data)

    if data_json['header'][1] == 0:
        try:
            from container import container
            getoutput("gcloud config set project container-a3c3c")
            result = container(data)
        except ImportError:
            raise ImportError('Import container fail')

    elif data_json['header'][1] == 1:
        try:
            from waze import waze
            getoutput("gcloud config set project maps-75922")
            result = waze(data)
        except ImportError:
            raise ImportError('Import Waze fail')

    elif data_json['header'][1] == 2:
        print('openTable')

    else:
        print('level Error')
    return result
