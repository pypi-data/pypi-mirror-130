# -*- coding:utf-8 -*-
import requests
import json

url = "http://localhost:8888/operate"
payload = {"method": "updateAIStudioDataframe", "fileName": "Jupyter_Notebook_Base2.ipynb", "nodeId": "123"}
headers = {"content-type": "application/json"}

ret = requests.post(url, data=json.dumps(payload), headers=headers)

print(ret.text)
