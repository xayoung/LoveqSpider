# -*- coding: utf-8 -*-
import urllib2
import re
import leancloud
import json
import time
import requests

from leancloud import Object
leancloud.init('xSKEPbolbbf8kzTyPwh0k8IN-gzGzoHsz', 'yfsU1LM3UsB2UPQPURS9zvew')


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

    """页面初始化"""
    def __init__(self):
        self.siteURL = 'http://www.loveq.cn/program.php?&cat_id=20&'

    """获取真实下载地址"""
    def get_detail_page(self, info_url):
        url = 'http://www.loveq.cn/' + info_url
        response = urllib2.urlopen(url)
        content = response.read().decode('utf-8')
        pattern = re.compile('<div.*?more_downlink".*?style.*?<a.*?"(.*?)"', re.S)
        items = re.findall(pattern, content)
        for item in items:
            download_url = item
        return download_url

    """获取索引页面的内容"""
    def get_page(self, page_index):
        url = self.siteURL + "page=" + str(page_index)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    """获取索引界面所有节目的信息"""
    def get_contents(self,page_index):
        page = self.get_page(page_index)
        pattern = re.compile('<dl.*?clearfix">.*?<dt.*?<a.*?"(.*?)".*?target.*?">(.*?)</a>.*?class="ct"><span>(.*?)</span>.*?</dd>.*?<dd style="width:7%;">(.*?)</dd>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            title = item[2].encode("utf-8")
            cleared_title = title.strip().lstrip().rstrip(',')
            split_cleared_title = cleared_title[15:]
            download_url = self.get_detail_page(item[0])
            download_count = item[3]
            real_title = split_cleared_title.split(' ', 1)

            # print download_count
            if "MP3" in cleared_title and "普通话" not in split_cleared_title :
                print real_title[-1]
                date_array = item[1].split('.', 3)
                if len(date_array) == 3:
                    print date_array
                    payload = {'title': real_title[-1],
                               'year': date_array[0],
                               'month': date_array[1],
                               'day': date_array[2],
                               'downloadUrl': download_url,
                               'downloadCount': download_count.replace(',', '')}

                    r = requests.post("http://loveq.dev/api/update/", data=payload)
                    print(r.text)
                else:
                    print '===========>' + real_title[-1] + '<==============' + str(page_index)
            #     loveqURLquery = LoveQ()
            #     loveqURLquery.set('date', item[1])
            #     loveqURLquery.set('url', download_url)
            #     loveqURLquery.set('cantonese', False)
            #     loveqURLquery.save()

if __name__ == "__main__":
    spider = Spider()

    for i in range(10, 12):
        spider.get_contents(i)
