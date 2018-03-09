#!/usr/bin/env python3
# coding: utf-8
# File: info_extract.py
# Author: lhy
# Date: 18-3-8
from urllib import request
from lxml import etree
from urllib import parse

class SougouBaike():
    def __index__(self):
        pass

    def get_html(self, url):
        return request.urlopen(url).read().decode('utf-8').replace('&nbsp;', '')

    def find_sofouid(self, word):
        url = "http://baike.sogou.com/Search.e?sp=S%s" % parse.quote(word)
        print(url)
        selector = etree.HTML(self.get_html(url))
        id = selector.xpath('//h2/a/@href')[0].split(';')[0]
        info_url = "http://baike.sogou.com/%s"%id
        return info_url

    def info_extract_sogou(self, word):  #sogou百科
        info_url = self.find_sofouid(word)
        selector = etree.HTML(self.get_html(info_url))
        info_list = list()
        info_data = self.extract_sogou(selector)
        if selector.xpath('//li[@class="current_item"]/text()'):
            info_data['current_semantic'] = selector.xpath('//li[@class="current_item"]/text()')[0].replace('    ', '').replace('（','').replace('）','')
        else:
            info_data['current_semantic'] = ''

        info_list.append(info_data)
        polysemantics = self.checksogou_polysemantic(selector)
        if polysemantics:
            info_list += polysemantics
        infos = [info for info in info_list if len(info) > 2]
        return infos

    def extract_sogou(self, selector):
        info_data = {}
        info_data['tags'] = [item.replace('\n', '') for item in selector.xpath('//div[@class="relevant_wrap"]/a/text()')]
        if selector.xpath('//li[@class="current_item"]/text()'):
            info_data['current_semantic'] = selector.xpath('//li[@class="current_item"]/text()')[0].replace('    ', '').replace('（','').replace('）','')
        else:
            info_data['current_semantic'] = ''
        tables = selector.xpath('//table[@class="abstract_list"]')
        for table in tables:
            attributes = table.xpath('./tbody/tr/th/text()')
            values = [td.xpath('string(.)') for td in table.xpath('./tbody/tr/td')]
            for item in zip(attributes, values):
                info_data[item[0].replace(' ', '').replace('\xa0','')] = item[1].replace('    ', '')
        return info_data

    def checksogou_polysemantic(self, selector):
        semantics = ['http://baike.sogou.com' + sem.split('?')[0] for sem in selector.xpath("//ol[@class='semantic_item_list']/li/a/@href")]
        names = [name for name in selector.xpath("//ol[@class='semantic_item_list']/li/a/text()")]
        info_list = list()
        if semantics:
            for item in zip(names, semantics):
                selector = etree.HTML(self.get_html(item[1]))
                info_data = self.extract_sogou(selector)
                info_data['current_semantic'] = item[0].replace('（','').replace('）','')
                if info_data:
                    info_list.append(info_data)
        return info_list

'''Testing'''
'''
if __name__ == "__main__":
    baikeinfo = SougouBaike()
    while(1):
        word = input('enter an word:')
        baikeinfo.info_extract_sogou(word)
'''



