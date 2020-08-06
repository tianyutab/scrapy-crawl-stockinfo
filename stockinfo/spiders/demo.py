# -*- coding: utf-8 -*-
import scrapy

import re



class DemoSpider(scrapy.Spider):
    name = 'demo'

    start_urls = ['https://quote.eastmoney.com/stocklist.html']
    def parse(self,response):
        for herf in response.css('a::attr(herf)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}",herf)[0]
                url = 'http://quote.eastmoney.com/'+stock+'.html'
                yield scrapy.Request(url,callback = self.parse_stock)
            except:
                continue

    def parse_stock(self, response):

        infoDict = {}

        name = response.css('.header-title-h2 fl').extract()[0]
        key = response.css('.header-title-c fl xh-highlight').extract()[0]

        value = response.css('.xpl').extract()[0]
        # for i in range(len(keylist)):
        #     key = re.findall(r'>.*</dt>', keylist[i][0][1:-5])
        #     try:
        #         val = re.findall(r'\d+\.?.*</dd>', valuelist[i][0][0:-5])
        #     except:
        #         val = '--'
        #     infoDict[key] = val
        infoDict.update(
            {'name':name, 'key':key,'value':value}
        )

        # infoDict.update(
        #         {'股票名称': re.findall('\s.*\(', name)[0].split()[0] +\
        #                  re.findall('\>.*\<', name)[0][1:-1] })
        yield infoDict


