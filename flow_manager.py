import json
from dialogflow_v1 import DialogflowApi

token_list = {
              'main_page': 'f06ad886f01f4053b13e58116580a090',
              'list_page': '0695ab771d6442b6b94281981042838b',
              'detail_page':'a75f9e59d9b7482d8ba89ef198e509ad',
              'confirm_page': '0e4800ee137944d7a196997baae98102'
              }

def flow_control(dataJson):
    dataStr = json.loads(dataJson)
    a = DialogflowApi(client_token = token_list[dataStr['currentPage']])
    response = a.post_query(dataStr['query'])
    df_response = response.json()
#    action = data['result']['fulfillment']['speech']

    return df_response

def response_handler(dataJson):
    dataStr = json.loads(dataJson)

