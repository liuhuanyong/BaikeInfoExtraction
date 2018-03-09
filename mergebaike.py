#!/usr/bin/env python3
# coding: utf-8
# File: Merge_baike.py
# Author: lhy
# Date: 18-3-9
from baidubaike import *
from hudongbaike import *
from sogoubaike import *
import jieba

def collect_infos(word):
    baidu = BaiduBaike()
    hudong = HudongBaike()
    sogou = SougouBaike()
    merge_infos = list()
    baidu_infos = baidu.info_extract_baidu(word)
    hudong_infos = hudong.info_extract_hudong(word)
    sogou_infos = sogou.info_extract_sogou(word)
    merge_infos += baidu_infos
    merge_infos += hudong_infos
    merge_infos += sogou_infos

    return merge_infos

def merge_infos_semantic(infos):
    sems_all = [item['current_semantic'] for item in infos]
    '''merge infos by semantics'''
    update_infos = list()
    for sem in set(sems_all):
        sems_dict = {}
        for item in infos:
            if item['current_semantic'] == sem:
                sems_dict.update(item)
        update_infos.append(sems_dict)
    return update_infos

def rank_infos(infos):
    att_nums = 0
    cover = 0.0
    score_dict = {}
    ranked_infos = list()
    covered_list = []
    covered_rate = 0.6
    covered_index = 0

    for info in infos:
        att_nums += len(info)
    for index, info in enumerate(infos):
        info['score'] = len(info)/att_nums
        info['tags'] = ' '.join(info['tags'])
        score_dict[index] = info['score']
    score_dict = sorted(score_dict.items(), key=lambda asd:asd[1], reverse=True)
    '''rank the infos'''
    for tmp in score_dict:
        cover += tmp[1]
        if cover < covered_rate:
            covered_index += 1
        else:
            continue
        ranked_infos.append(infos[tmp[0]])
    '''print'''
    for index, info in enumerate(ranked_infos):
        print(index, info['score'], info['current_semantic'], info)

    return ranked_infos, covered_index

def compute_similarity(a, b):
    return len(set(a).intersection(set(b)))

def merge_infos_sim(infos, covered_index):
    for index in range(0, covered_index):
        for index_ in range(index + 1, covered_index):
            score_attr = compute_similarity(infos[index].keys(), infos[index_].keys())
            score_val = compute_similarity(infos[index].values(), infos[index_].values())

            score_pair = compute_similarity([key + str(value) for key, value in infos[index].items()],
                                            [key + str(value) for key, value in infos[index_].items()])

            print(index, index_, score_attr, score_val, score_pair)

def merge_infos(word):
    infos = collect_infos(word)
    update_infos = merge_infos_semantic(infos)
    ranked_infos, covered_index = rank_infos(update_infos)

    return ranked_infos


while(1):
    word = input('enter an word to search:\n')
    infos = collect_infos(word)
    update_infos = merge_infos_semantic(infos)
    ranked_infos, covered_index = rank_infos(update_infos)
    merge_infos_sim(ranked_infos, covered_index)
