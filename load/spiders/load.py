# -*- coding: utf-8 -*-
import scrapy
from load.items import BmwItem


class Bmw5Spider(scrapy.Spider):
    name = 'load'
    allowed_domains = ['10.177.9.37:81/suichuan']
    start_urls = ['http://10.177.9.37:81/suichuan']
    # cookies = input("cookie:")


    cookies ='84A6F BE7FC6B56DD862BDF671DB6F5AD'

    def start_requests(self):
        
        url='http://10.177.9.37:81/suichuan/document/list_doLogin.jsp?sysUserID=63904&sysUserCurrentEntityId=120204&sysUserBelongedEntityId=120104'
        temp = ' JSESSIONID='+self.cookies
        cookies = {i.split('=')[0]: i.split('=')[1] for i in temp.split(';')}
        self.cookies = cookies
       
        yield scrapy.Request(url=url,callback=self.parse,cookies=cookies)
         
            

    def parse(self, response):

   

        node_list=response.xpath('//tr[@class="idx_item2a"]')

        print('新到来文数据',len(node_list))


        for node in node_list:
     
            biaoti = node.xpath('.//a/@title').get()
            
            docid = node.xpath('.//a/@href').get()
           
            docid_str=docid[(docid.index("&NDOCID=")+8):docid.index("&NDOCSORTID")]
            
            link = 'http://10.177.9.37:81/suichuan/document/ifr_docinfo_file.jsp?NDOCID={}&NDOCSORTID=2&subFrame=doWaiting&NPROCID=19&showCPQB=&newCPQB=0'.format(docid_str)

            
            yield scrapy.Request(url=link,callback=self.parse2,cookies=self.cookies,dont_filter=True,meta={'biaoti':biaoti})


    def parse2(self, response):
        
        biaoti = response.meta['biaoti']
        file_nodes = response.xpath('//tr[@class="secondRightContent"]')
        #print(len(file_nodes))

        for node in file_nodes:
            filepagelink = node.xpath('.//a/@href').get()
            wenjianming = node.xpath('.//a/text()').get()
            filepagelink = 'http://10.177.9.37:81/suichuan/document/'+filepagelink
            
            yield scrapy.Request(url=filepagelink,callback=self.parse3,cookies=self.cookies,dont_filter=True,meta={'biaoti':biaoti,'wenjianming':wenjianming})
        pass


    def parse3(self, response):
        print('==============================')

        biaoti = response.meta['biaoti']

        wenjianming = response.meta['wenjianming']

        #print('=================='+str(wenjianming)+'==================')
        
        body = str(response.text)

        file=body[(body.index('//方正打印')+152):(body.index('var URLPath = igrpUrlHeader'))]

        if len(file)>50:
            file=file[(file.index('FILENAME=')+9):(file.index('&flag='))]
            pass
        file = file.rstrip('";\r\n\t')
        # print(file)
        file = 'http://10.177.9.37:81/suichuan/downLoadFileServlet?FILENAME='+file
        partname = biaoti
        urls = [file]
        
        # print(partname)
        # print(urls)
        item = BmwItem(partname=partname, urls=urls,wenjianming = wenjianming )
        yield item

