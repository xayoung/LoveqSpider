#!/usr/bin/env python
#-*- coding: utf-8 -*-
#import pycurl
#import json
import requests
import xinge


#f = file("06JSONFile.json")
#s = json.load(f)
#print s
#f.close


# iOS全量推送

print(xinge.PushAllIos(2200205039, '284ce032cf63af6633ad743b6cdd13c4', 'python服务器自动推送测试', xinge.XingeApp.ENV_PROD))

url = 'https://pythontest.wilddogio.com/test.json'
#json_data = s
#headers = {'X-Api-Key': 'asdf1234'}

r = requests.request('PUT', url, json=json_data)
#print(r.json)


#c = pycurl.Curl()
#c.setopt(pycurl.URL, "https://pythontest.wilddogio.com/test.json/")
#c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: application/json'])
#c.setopt(pycurl.CUSTOMREQUEST, "PUT")
#data = json.dumps({"xayoung":"001"})
#c.setopt(pycurl.PUT, True)
#c.setopt(pycurl.POSTFIELDS,data)
#c.perform()
#c.close()

#curl -X PUT -d '{ "alanisawesome": { "name": "Alan Turing", "birthday": "June 23, 1912" } }' 'https://pythontest.wilddogio.com/test.json'