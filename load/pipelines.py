# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
from urllib import request

class BmwPipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),"images")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.datefd = os.path.join(self.path,time.strftime("%Y%m%d"))
        if not os.path.exists(self.datefd):
            os.mkdir(self.datefd)


    def process_item(self, item, spider):

        partname = item['partname']
        urls = item['urls']



        partpath = os.path.join(self.datefd,partname)
        if not os.path.exists(partpath):
            os.mkdir(partpath)
        for url in urls:

            imagename = item['wenjianming']

            filetype = url[(url.index('NAME=')+5):]
            filetype = filetype[(filetype.index('.')):]
            imagename = imagename+filetype
            #print(url)
            # print(self.path,imagename)
            
            print(item['partname'],imagename)
            request.urlretrieve(url,os.path.join(partpath,imagename))
        return item
