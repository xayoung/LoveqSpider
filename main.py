# -*- coding: utf-8 -*-
import urllib2
import re
import json


class Spider:

    #页面初始化
    def __init__(self):
        self.siteURL = 'http://www.loveq.cn/program.php?&cat_id=20&'
        self.JSONMP3 = []

    #获取索引页面的内容
    def getPage(self,pageIndex):
        url = self.siteURL + "page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    #获取索引界面所有节目的信息
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<dl.*?clearfix">.*?<dt.*?<a.*?"(.*?)".*?target.*?">(.*?)</a>.*?class="ct"><span>(.*?)</dd>',re.S)
        items = re.findall(pattern,page)

        jsonChinese = []
        jsonMP3 = []
        for item in items:
            downloadURL = self.getDetailPage(item[0])
            message = "下载地址:" + str(item[0]) + "节目期数:" + str(item[1])
            print message
            name=item[2].encode("utf-8")
            if 'MP3格式' in name or 'mp3格式' in name:
                if '普通话' in name:
                    # 保存普通话节目列表
                    jsonChinese.append([downloadURL,item[1],0])
                else:
                    #保存粤语节目列表
                    jsonMP3.append([downloadURL,item[1],1])
                    contents = {}
                    contents.setdefault('url',downloadURL)
                    contents.setdefault('title',item[1])
                    contents.setdefault('type',str(1))
                    self.JSONMP3.append(contents)
                    #2006-2009年的节目没有采用[MP3格式]xxxx这样的方式作为title,手动进行切换代码吧=.=
                    # jsonMP3.append([downloadURL, item[1], 1])
                    # contents = {}
                    # contents.setdefault('url', downloadURL)
                    # contents.setdefault('title', item[1])
                    # contents.setdefault('type', str(1))
                    # self.JSONMP3.append(contents)

    #获取真实下载地址
    def getDetailPage(self,infoURL):
        url = 'http://www.loveq.cn/' + infoURL
        response = urllib2.urlopen(url)
        content = response.read().decode('utf-8')
        pattern = re.compile('<div.*?more_downlink".*?style.*?<a.*?"(.*?)"',re.S)
        items = re.findall(pattern,content)
        for item in items:
             downloadURL = item
        return downloadURL

    #传入起止页码，获取界面json
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"looking for page",i
            self.savePageInfo(i)

    #将整页节目列表保存起来
    def savePageInfo(self,pageIndex):
        self.getContents(pageIndex)

class Tools:
    #工具初始化
    def __init__(self):
        self.JSONFile = {}

    #传入起止月份，获取新json
    def saveNewJSONSInfo(self,year,start,end,JSON):
        self.JSONFile = {}
        for i in range(start,end+1):
            self.saveJSONInfo(year,i,JSON)

    #单个月份
    def saveSingleMonthJSON(self,year,month,JSON):
        monthJSON = []
        monthstr = ''
        monthstr2 = ''
        if month < 10:
            monthstr = year + '.0' + str(month)
            monthstr2 = year + '0' + str(month)
        else:
            monthstr = year + '.' + str(month)
            monthstr2 = year + str(month)
        for item in JSON:
            if monthstr in item['title']:
                monthJSON.append(item)
        return monthJSON

    #将节目保存起来
    def saveJSONInfo(self,year,Index,JSON):
        monthJSON = []
        monthstr = ''
        monthstr2 = ''
        if Index < 10:
            monthstr = year + '.0' + str(Index)
            monthstr2 = year + '0' + str(Index)
        else:
            monthstr = year + '.' + str(Index)
            monthstr2 = year + str(Index)
        for item in JSON:
            if monthstr in item['title']:
                monthJSON.append(item)
                self.JSONFile.setdefault(monthstr2,monthJSON)

    def store(self,fileName,JSON):
        with open( fileName + 'JSONFile.json', 'w') as f:
            f.write(json.dumps(JSON))



#保存JSON文件到当前文件夹
if __name__ == "__main__":
    # 传入起止页码，在此传入了1,71,表示抓取第1到71页的节目
    spider = Spider()
    spider.savePagesInfo(1, 71)
    tool = Tools()
    totalJSON = {}
    # 设置年份,3代表2003年
    for i in range(3, 16):
        year = ''
        if i < 10:
            year = '200' + str(i)
        else:
            year = '20' + str(i)
        tool.saveNewJSONSInfo(year, 1, 12, spider.JSONMP3)
        totalJSON.setdefault(year, tool.JSONFile)
    tool.store(year,totalJSON)



