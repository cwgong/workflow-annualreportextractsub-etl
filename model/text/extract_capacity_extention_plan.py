# -*- coding: utf-8 -*-

# 公司产能扩张规划及进展

import re

def extract_sentences(pdf_json, feas=[]):

    result = []
    page_nums = []
    candidate_texts = []
    for i in range(len(pdf_json)):
        obj = pdf_json[i]
        if obj['type'] == 'text':
            # 去空格
            p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
            if len(p) > 0:
                s_list = p.split("。")
                for s in s_list:
                    # 判断是否满足 feas
                    all_c = len(feas)
                    fea_c = 0
                    for fea in feas:
                        for fe in fea:
                            if fe in s:
                                fea_c += 1
                                break
                    if all_c == fea_c:
                        if s not in result:
                            result.append(s)
                            page_num = obj['page_num']
                            if page_num not in page_nums:
                                page_nums.append(page_num)

    if len(result) > 0:
        sentences = '。'.join(result)
        print(sentences)
        print(page_nums)
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        return sentences, page_nums, candidate_texts
    else:
        return None, page_nums, candidate_texts



def extract(detail):

    knowledge = None

    pdf_json = detail
    feas= [['扩产','扩建'], ['吨','项目']]
    result, page_nums, evidence_texts = extract_sentences(pdf_json, feas=feas)

    if result is not None:
        knowledge = {"type": "公司产能扩张规划及进展",
                     "text": result,
                     "candidate": None,
                     "pages": page_nums}


    print(knowledge)
    return knowledge
