# -*- coding: utf-8 -*-
import main
import json

#更新单个月份,输入页码
spider = main.Spider()
spider.savePagesInfo(1,2)
tool = main.Tools()
totalJSON = {}
tool.store('06', tool.saveSingleMonthJSON('2016',6,spider.JSONMP3))