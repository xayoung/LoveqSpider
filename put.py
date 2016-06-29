# -*- coding: utf-8 -*-
import pycurl
import json
import requests
import xinge
import time


loaclYear = time.strftime("%Y", time.localtime())
loaclMonth = time.strftime("%m", time.localtime())

# iOS全量推送
#print xinge.PushAllIos(2200205039, '284ce032cf63af6633ad743b6cdd13c4', 'python自动推送测试8:56', xinge.XingeApp.ENV_PROD)

f = file("06JSONFile.json")
s = json.load(f)
print s
f.close



url = 'https://pythontest.wilddogio.com/'+ loaclYear + '/' + loaclYear+loaclMonth +'.json'
#json_data = s
#r = requests.request('PUT', url, json=json_data)
array = json.dumps(requests.get(url).json())
data = json.loads(array)
print(len(data))

