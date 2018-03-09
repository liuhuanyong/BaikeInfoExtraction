#!/usr/bin/env python3
# coding: utf-8
# File: baikecontent.py
# Author: lhy
# Date: 18-3-9
from hudongbaike import *
from pyltp import SentenceSplitter
import jieba.posseg as pseg



hudong = HudongBaike()
def collect_infos(word):
    infos = hudong.info_extract_hudong(word)
    for info in infos:
        intro_sents = [sent for sent in SentenceSplitter.split(info['intro']) if len(sent) > 0]
        desc_sents = [sent for sent in SentenceSplitter.split(info['desc']) if len(sent) > 0]
        print(intro_sents)
        print('****'*5)
        print(desc_sents)

def question_parser(sentence):
    filter_pos = ['n', 'd', 'm']
    segments = [word.word + '/' + word.flag for word in pseg.cut(sentence) if word.flag[0] in filter_pos]
    segments = [word.word + '/' + word.flag for word in pseg.cut(sentence)]

    print(segments)







while(1):
    sentence = input('enter an sentence to search:')
    #collect_infos(word)
    question_parser(sentence)