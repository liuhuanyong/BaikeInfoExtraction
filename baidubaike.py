#!/usr/bin/env python3
# coding: utf-8
# File: baidubaike.py
# Author: lhy
# Date: 18-3-8

from urllib import request
from lxml import etree
from urllib import parse



class BaiduBaike():
    def __init__(self):
        pass

    def get_html(self, url):
        return request.urlopen(url).read().decode('utf-8').replace('&nbsp;', '')

    def info_extract_baidu(self, word):  # 百度百科
        url = "http://baike.baidu.com/item/%s" % parse.quote(word)
        print(url)
        selector = etree.HTML(self.get_html(url))
        info_list = list()
        info_list.append(self.extract_baidu(selector))
        polysemantics = self.checkbaidu_polysemantic(selector)
        if polysemantics:
            info_list += polysemantics
        infos = [info for info in info_list if len(info) > 2]

        return infos

    def extract_baidu(self, selector):
        info_data = {}
        if selector.xpath('//h2/text()'):
            info_data['current_semantic'] = selector.xpath('//h2/text()')[0].replace('    ', '').replace('（','').replace('）','')
        else:
            info_data['current_semantic'] = ''
        if info_data['current_semantic'] == '目录':
            info_data['current_semantic'] = ''

        info_data['tags'] = [item.replace('\n', '') for item in selector.xpath('//span[@class="taglist"]/text()')]
        if selector.xpath("//div[starts-with(@class,'basic-info')]"):
            for li_result in selector.xpath("//div[starts-with(@class,'basic-info')]")[0].xpath('./dl'):
                attributes = [attribute.xpath('string(.)').replace('\n', '') for attribute in li_result.xpath('./dt')]
                values = [value.xpath('string(.)').replace('\n', '') for value in li_result.xpath('./dd')]
                for item in zip(attributes, values):
                    info_data[item[0].replace('    ', '')] = item[1].replace('    ', '')
        return info_data

    def checkbaidu_polysemantic(self, selector):
        semantics = ['https://baike.baidu.com' + sem for sem in
                     selector.xpath("//ul[starts-with(@class,'polysemantList-wrapper')]/li/a/@href")]
        names = [name for name in selector.xpath("//ul[starts-with(@class,'polysemantList-wrapper')]/li/a/text()")]
        info_list = []
        if semantics:
            for item in zip(names, semantics):
                selector = etree.HTML(self.get_html(item[1]))
                info_data = self.extract_baidu(selector)
                info_data['current_semantic'] = item[0].replace('    ', '').replace('（','').replace('）','')
                if info_data:
                    info_list.append(info_data)
        return info_list
'''
baidu = BaiduBaike()
while(1):
    word = input('enter an word:')
    baidu.info_extract_baidu(word)
'''