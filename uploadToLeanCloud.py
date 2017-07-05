# -*- coding: utf-8 -*-
import urllib2
import re
import leancloud
import time

leancloud.init('xSKEPbolbbf8kzTyPwh0k8IN-gzGzoHsz', 'yfsU1LM3UsB2UPQPURS9zvew')

from leancloud import Object


class LoveQ(Object):
    def is_cheated(self):
        # 可以像正常 Python 类一样定义方法
        return self.get('cheatMode')

    @property
    def score(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('score')

    @score.setter
    def score(self, value):
        # 同样的，可以给对象的score增加setter
        return self.set('url', value)


class Spider:
    # 页面初始化
    def __init__(self):
        self.siteURL = 'http://www.loveq.cn/program.php?&cat_id=20&'
        self.JSONMP3 = []

    # 获取索引页面的内容
    def getPage(self, pageIndex):
        url = self.siteURL + "page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    # 获取索引界面所有节目的信息
    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            '<dl.*?clearfix">.*?<dt.*?<a.*?"(.*?)".*?target.*?">(.*?)</a>.*?class="ct"><span>(.*?)</dd>', re.S)
        items = re.findall(pattern, page)

        jsonChinese = []
        jsonMP3 = []
        CloudDataListStr = []

        year = time.strftime("%Y", time.localtime())
        # 查询leanCloud的当前年份的
        CloudData = leancloud.Object.extend('LoveQ')
        query = CloudData.query
        query.startswith("date", year)
        CloudDataList = query.find()
        #
        for item in CloudDataList:
            title = item.get('date')
            CloudDataListStr.append(title)

        for item in items:
            downloadURL = self.getDetailPage(item[0])
            # message = "下载地址:" + str(item[0]) + "节目期数:" + str(item[1])
            # print message
            name = item[2].encode("utf-8")
            if 'MP3格式' in name or 'mp3格式' in name:
                if '普通话' in name:
                    # 保存普通话节目列表
                    jsonChinese.append([downloadURL, item[1], 0])
                else:
                    # 保存粤语节目列表
                    jsonMP3.append([downloadURL, item[1], 1])
                    contents = {}
                    contents.setdefault('url', downloadURL)
                    contents.setdefault('title', item[1])
                    contents.setdefault('type', str(1))
                    if item[1] not in CloudDataListStr:
                        if year in item[1]:
                            print "没有包含"
                            loveqURLquery = LoveQ()
                            loveqURLquery.set('date', item[1])
                            loveqURLquery.set('url', downloadURL)
                            loveqURLquery.set('cantonese', True)
                            loveqURLquery.save()
                        else:
                            print "none update"
        print time.strftime("%m-%d-%H:%M", time.localtime())



    # 获取真实下载地址
    def getDetailPage(self, infoURL):
        url = 'http://www.loveq.cn/' + infoURL
        response = urllib2.urlopen(url)
        content = response.read().decode('utf-8')
        pattern = re.compile('<div.*?more_downlink".*?style.*?<a.*?"(.*?)"', re.S)
        items = re.findall(pattern, content)
        if len(items) == 0:
            return ""
        else:
            for item in items:
                downloadURL = item
            return downloadURL

    # 传入起止页码，获取界面json
    def savePagesInfo(self, start, end):
        for i in range(start, end + 1):
            print "looking for page", i
            self.savePageInfo(i)

    # 将整页节目列表保存起来
    def savePageInfo(self, pageIndex):
        self.getContents(pageIndex)


# 保存JSON文件到当前文件夹
if __name__ == "__main__":
    # 传入起止页码，在此传入了1,71,表示抓取第1到71页的节目
    spider = Spider()
    spider.savePagesInfo(1, 2)
