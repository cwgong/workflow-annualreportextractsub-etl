# -*- coding: UTF-8 -*-
# 销售模式

import re

def extract(text_list, text_page_list):
    cooperate_list = []
    cooperate_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        para_list = split_by_comma(para)
        for sen in para_list:
            sen = sen.strip()
            if "直销" in sen and '经销' in sen:
                cooperate_list.append(sen)
                cooperate_page_list.append(text_page_list[i])
            if "直销" in sen:
                cooperate_list.append(sen)
                cooperate_page_list.append(text_page_list[i])
            if "经销" in sen and "经销商" not in sen and '经销处' not in sen:
                cooperate_list.append(sen)
                cooperate_page_list.append(text_page_list[i])
            # if "代理" in sen:
            #     cooperate_list.append(sen)
            #     cooperate_page_list.append(text_page_list[i])

    if len(cooperate_list) == 0:
        return None

    candidate_list = []
    for i in range(len(cooperate_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": cooperate_list[i],
                     "textPage": cooperate_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司销售模式",
                 "text": cooperate_list[0],
                 "candidate": candidate_list,
                 "pages": cooperate_page_list[0]}

    return knowledge

def split_by_comma(para):
    para_ = para.replace('.',',').replace('。',',').replace(';',',').replace('；',',').replace('!','')
    para_new = para_.replace('，',',')
    para_list = para_new.split(',')
    return para_list

def strip_num(para):
    para = para.strip()
    p = re.compile(r'\d+')
    para = p.match('',para)
    return para

if __name__ == "__main__":
    s = '建筑工程施工业务是公司营业收入的主要组成部分。公司全资子公司上海浦兴路桥建设工有限公司拥有市政公用工程施工总承包一级、公路路面工程专业承包一级、公路工程施工总承包二级、水利水电工程施工总承包三级、河湖整治工程专业承包三级等多项专业资质。公司全资子公司上海市浦东新区建设（集团）有限公司拥有建筑工程施工总承包一级、市政公用工程施工总承包一级、地基基础工程专业承包一级、建筑装饰装修工程专业承包一级、桥梁工程专业承包一'
    para_list = split_by_comma(s)
    print(para_list)