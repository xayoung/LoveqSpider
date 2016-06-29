# -*- coding: utf-8 -*-
import main
import requests
import json
import xinge

#输入页码,爬取节目信息
spider = main.Spider()
spider.savePagesInfo(1,2)
#分类工具进行筛选
tool = main.Tools()
totalJSON = {}
#upload至wilddog后台
wilddogURL = 'https://loveq.wilddogio.com/program/'

uploadTool = main.uploadPushData()
newJSON = tool.saveSingleMonthJSON(uploadTool.loaclYear,uploadTool.loaclMonth,spider.JSONMP3)
newJSOND = json.dumps(newJSON)
newJSONdata = json.loads(newJSOND)
#print newJSONdata

url = wilddogURL+ uploadTool.loaclYear + '/' + uploadTool.loaclYear+uploadTool.loaclMonth +'.json'
oldJSON = json.dumps(requests.get(url).json())
oldJSONdata = json.loads(oldJSON)
#print oldJSONdata

if  oldJSONdata == None:
    uploadTool.uploadJSON(wilddogURL,newJSON)
    xinge.PushAllIos(2200205039, '284ce032cf63af6633ad743b6cdd13c4',  uploadTool.loaclMonth + 'python自动推送测试', xinge.XingeApp.ENV_PROD)
else:
    if len(newJSONdata) > len(oldJSONdata):
        uploadTool.uploadJSON(wilddogURL, newJSON)
        xinge.PushAllIos(2200205039, '284ce032cf63af6633ad743b6cdd13c4',  uploadTool.loaclMonth + 'python自动推送测试', xinge.XingeApp.ENV_PROD)
        print 'updateToWilddog'
    else:
        print 'none update'
#写入文件
#tool.store('06', tool.saveSingleMonthJSON('2016',6,spider.JSONMP3))