import logging
import json
from dialogflow_v2 import DialogflowApi

a = DialogflowApi()
response = a.text_query('Navigation')
print(response.json())
