# -*- coding: utf-8 -*-
import main
import requests
import json
import xinge
import time

#输入页码,爬取节目信息
spider = main.Spider()
spider.savePagesInfo(1,2)
#分类工具进行筛选
tool = main.Tools()
totalJSON = {}
#wilddog后台
wilddogURL = 'https://loveq.wilddogio.com/program/'

uploadTool = main.uploadPushData()
newJSON = tool.saveSingleMonthJSON(uploadTool.loaclYear,uploadTool.loaclMonth,spider.JSONMP3)
newJSOND = json.dumps(newJSON)
newJSONdata = json.loads(newJSOND)
#print newJSONdata

#读取老数据
url = wilddogURL+ uploadTool.loaclYear + '/' + uploadTool.loaclYear+uploadTool.loaclMonth +'.json'
#print url
oldJSON = json.dumps(requests.get(url).json())
oldJSONdata = json.loads(oldJSON)
#print oldJSONdata

#如果老数据为空
if  oldJSONdata == None:
    #上传新数据开辟节点,新年份/新月份,必须有数据再上传
    if len(newJSON) > 0 :
        uploadTool.uploadJSON(wilddogURL,newJSON)
        xinge.PushAllIos(2200205039, 'I3327UDVYP4J', '最新节目已更新,快去下载吧!', xinge.XingeApp.ENV_PROD)
        print 'newDataToWilddog'
    else:
        print('this is a new month/year,but nothing update')
else:
    #有老数据,但是需要更新,比对新老数据的个数
    if len(newJSONdata) > len(oldJSONdata):
        uploadTool.uploadJSON(wilddogURL, newJSON)
        xinge.PushAllIos(2200205039, 'I3327UDVYP4J', '最新节目已更新,快去下载吧!', xinge.XingeApp.ENV_PROD)
        print 'updateDataToWilddog'
    else:
        print 'none update'

print time.strftime("%m-%d-%H:%M", time.localtime())
#写入文件
#tool.store('06', tool.saveSingleMonthJSON('2016',6,spider.JSONMP3))
