from app.container import Container
import time
import json

test_format = {
                'header': [0, 0, 100, int(time.time()), 3, 0],
                'data': {
                        'query': 'send it',
                }
}

a = Container(json.dumps(test_format))
r = a.get_dest_lvl()
print(r)
