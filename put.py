# -*- coding: utf-8 -*-
import pycurl
import json
import requests


f = file("06JSONFile.json")
s = json.load(f)
print s
f.close



url = 'https://pythontest.wilddogio.com/test.json'
json_data = s
#headers = {'X-Api-Key': 'asdf1234'}

r = requests.request('PUT', url, json=json_data)
print(r.json)


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