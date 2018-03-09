#!/usr/bin/env python3
# coding: utf-8
# File: hudongbaike.py
# Author: lhy
# Date: 18-3-8

from urllib import request
from lxml import etree
from urllib import parse


class HudongBaike():
    def __init__(self):
        pass

    def get_html(self, url):
        return request.urlopen(url).read().decode('utf-8').replace('&nbsp;', '')

    def info_extract_hudong(self, word):  # 互动百科
        url = "http://www.baike.com/wiki/%s" % parse.quote(word)
        print(url)
        selector = etree.HTML(self.get_html(url))
        info_list = list()
        info_data = self.extract_hudong(selector)
        if selector.xpath('//li[@class="current"]/strong/text()'):
            info_data['current_semantic'] = selector.xpath('//li[@class="current"]/strong/text()')[0].replace('    ', '').replace('（','').replace('）','')
        else:
            info_data['current_semantic'] = ''
        info_list.append(info_data)
        polysemantics = self.checkhudong_polysemantic(selector)
        if polysemantics:
            info_list += polysemantics
        infos = [info for info in info_list if len(info) > 2]

        return infos

    def extract_hudong(self, selector):
        info_data = {}
        info_data['desc'] = selector.xpath('//div[@id="content"]')[0].xpath('string(.)')
        info_data['intro'] = selector.xpath('//div[@class="summary"]')[0].xpath('string(.)').replace('编辑摘要', '')
        info_data['tags'] = [item.replace('\n', '') for item in selector.xpath('//p[@id="openCatp"]/a/text()')]
        for info in selector.xpath('//td'):
            attribute = info.xpath('./strong/text()')
            val = info.xpath('./span')
            if attribute and val:
                value = val[0].xpath('string(.)')
                info_data[attribute[0].replace('：','')] = value.replace('\n','').replace('  ','').replace('    ', '')
        return info_data

    def checkhudong_polysemantic(self, selector):
        semantics = [sem for sem in selector.xpath("//ul[@id='polysemyAll']/li/a/@href") if 'doc_title' not in sem]
        names = [name for name in selector.xpath("//ul[@id='polysemyAll']/li/a/text()")]
        info_list = list()
        if semantics:
            for item in zip(names, semantics):
                selector = etree.HTML(self.get_html(item[1]))
                info_data = self.extract_hudong(selector)
                info_data['current_semantic'] = item[0].replace('（','').replace('）','')
                if info_data:
                    info_list.append(info_data)
        return info_list

'''Testing'''
'''
hudong = HudongBaike()
while(1):
    word = input('enter an word to search:')
    info = hudong.info_extract_hudong(word)
    for item in info:
        print(item['desc'])
'''