# import json
# from subprocess import getoutput
# from server import USER
# import logging
# from dialogflow_api.dialogflow_v2 import DialogflowApi
#
# gcloudProjectID = {
#     'Container': 'container-a3c3c',
#     'Waze': 'maps-75922',
#     'GoogleMap': 'gmap-74a30',
#     'OpenTable': 'open-table-2'
# }
#
# # MIC = {}
#
#
# # def state_init(data):
# #     init_data = json.loads(data)
# #     logging.info('Status: {}'.format(MIC))
# #     if init_data['header'][0] not in MIC:
# #         MIC[init_data['header'][0]] = {'mic_off': False}
# #         MIC[init_data['header'][0]]['df_v2'] = DialogflowApi(session_id=init_data['header'][0])
# #         getoutput("gcloud config set project container-a3c3c")
# #     else:
# #         pass
#
#
# def manager(data):
#     """
#     :type data: String
#     :rtype: String
#     """
#     data_json = json.loads(data)
#
#     if not USER[data_json['header'][0]]['mic_off']:
#         if 'query' not in data_json['data']:
#             return ''
#
#         if data_json['header'][1] == 0 or \
#                 data_json['header'][1] == 5 or \
#                 data_json['header'][1] == 6:
#             try:
#                 from app.container import Container
#                 getoutput("gcloud config set project container-a3c3c")
#                 a = Container(data)
#                 result = a.get_dest_lvl()
#             except ImportError:
#                 raise ImportError('Import container fail')
#
#         elif data_json['header'][1] == 1:
#             try:
#                 from app.waze import waze
#                 getoutput("gcloud config set project {}".format(gcloudProjectID['Waze']))
#                 print('Waze: {}'.format(USER))
#                 result = waze(data)
#             except ImportError:
#                 raise ImportError('Import Waze fail')
#
#         elif data_json['header'][1] == 2:
#             try:
#                 from app.opentable import opentable
#                 getoutput("gcloud config set project {}".format(gcloudProjectID['OpenTable']))
#                 result = opentable(data)
#             except ImportError:
#                 raise ImportError('Import OpenTable fail')
#
#         elif data_json['header'][1] == 3:
#             try:
#                 from app.container import Container
#                 a = Container(data)
#                 result = a.get_dest_lvl()
#             except ImportError:
#                 raise ImportError('Import container fail')
#
#         elif data_json['header'][1] == 4:
#
#             try:
#                 from app.text_message import text_message
#                 result = text_message(data)
#             except ImportError:
#                 raise ImportError('Import text_message fail')
#             # try:
#             #     from app.container import Container
#             #     a = Container(data)
#             #     result = a.get_dest_lvl()
#             # except ImportError:
#             #     raise ImportError('Import container fail')
#
#         elif data_json['header'][1] == 7:
#             try:
#                 from app.gmap import gmap
#                 getoutput("gcloud config set project {}".format(gcloudProjectID['GoogleMap']))
#                 result = gmap(data)
#             except ImportError:
#                 raise ImportError('Import gmap fail')
#
#         else:
#             print('level not implemented yet')
#             result = data
#     else:
#
#         # print(MIC)
#         # '''Detect the first time user as well as websockets reconnect'''
#         # if 'query' not in data_json['data']:
#         #     del MIC[data_json['header'][0]]
#         #     return ''
#
#         if 'microphone' in data_json['data']['query']:
#             j = json.loads(USER[data_json['header'][0]]['state'])
#             j['header'].insert(3, 410)
#             j['data']['speech'] = 'Welcome back'
#             result = json.dumps(j)
#             #del MIC[j['header'][0]]
#         else:
#             result = ''
#     return result
