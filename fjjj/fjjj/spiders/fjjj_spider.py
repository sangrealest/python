#!/usr/bin/python
#-*- coding:utf-8 -*-

from scrapy import Spider
from scrapy import Selector
from scrapy import log
from fjjj.items import FjjjItem


class FjjjSpider(Spider):
    name = "fjjj"
    allowed_domains = ["jisilu.cn"]
    start_urls = [ 
         "http://www.qiushibaike.com/hot/"
#        "https://www.jisilu.cn/data/sfnew/detail/150195",
#        "https://www.jisilu.cn/data/sfnew/detail/150197"
    ]
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div/div/div/div/div')
        items = []
#        print sites

        for site in sites:
            item = FjjjItem()
            name = site.xpath('div/text()').extract()
            value = site.xpath('tr/td/input/@value').extract()
            item['name'] = [t.encode('utf-8') for t in name]
            item['value'] = [v.encode('utf-8') for v in value]
            items.append(item)
            log.msg("APpending item...", level='INFO')
        log.msg("Append done.", level='INFO')
        return items

#            item['description'] = site.xpath('text()').extract()
#            items.append(item)
#        for i in item['name']:
#            if i != ' ':
#                 print i + '\t'
#        for j in item['value']:
#            if j != ' ':
#                 print j + '\\t'
