# -*- coding: utf-8 -*-
# 公司研发规划及进展

import re

def extract_paragraph(pdf_json, sub_title_feas = {'subs':[], 'verbs':[], 'objs':[]}, sub_title_length = 11, next_max_p = 1):

    sub_title_sample = '产品研发规划'

    # 定位子标题位置
    sub_title_flag = None
    sub_title_idx = None
    for i in range(len(pdf_json)):
        obj = pdf_json[i]
        if obj['type'] == 'text':
            # 去空格
            p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
            if len(p) > 0:
                # 判断是否满足 feas
                c = 0
                p_ = p
                if len(p_) < sub_title_length:
                    all_c = 0
                    sub_c = 0
                    verb_c = 0
                    obj_c = 0
                    if 'subs' in sub_title_feas:
                        all_c += 1
                        subs = sub_title_feas['subs']
                        for fea in subs:
                            if fea in p_:
                                idx = p_.find(fea)
                                p_ = p_[idx + 1:]
                                sub_c += 1
                                break
                    if 'verbs' in sub_title_feas:
                        all_c += 1
                        verbs = sub_title_feas['verbs']
                        for fea in verbs:
                            if fea in p_:
                                idx = p_.find(fea)
                                p_ = p_[idx + 1:]
                                verb_c += 1
                                break
                    if 'objs' in sub_title_feas:
                        all_c += 1
                        objs = sub_title_feas['objs']
                        for fea in objs:
                            if fea in p_:
                                idx = p_.find(fea)
                                p_ = p_[idx + 1:]
                                obj_c += 1
                                break
                    if all_c == sub_c + verb_c + obj_c:
                        sub_title_idx = i
                        break

    result = []
    page_nums = []
    evidence_texts = []
    if sub_title_idx is not None:
        # 选取下文 next_max_p 段内
        for j in range(sub_title_idx + 1, sub_title_idx + 1 + next_max_p):
            obj = pdf_json[j]
            if obj['type'] == 'text':
                # 去空格
                p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
                page_num = obj['page_num']
                if page_num not in page_nums:
                    page_nums.append(page_num)
                result.append(p)

    #print(result)
    #print(page_nums)
    #print('~~~~~~~~~~~~~~~~~~~~~~~')
    if len(result) > 0:
        return result, page_nums, evidence_texts
    else:
        return None, page_nums, evidence_texts


def extract(detail):

    knowledge = None

    pdf_json = detail
    sub_title_feas = {'subs': ['研发'], 'verbs': ['规划', '计划']}
    sub_title_length = 11
    next_max_p = 1
    result, page_nums, evidence_texts = extract_paragraph(pdf_json, sub_title_feas=sub_title_feas,
                                                          sub_title_length=sub_title_length, next_max_p=next_max_p)

    if result is not None:
        knowledge = {"type": "公司研发规划及进展",
                     "text": result[0],
                     "candidate": None,
                     "pages": page_nums}


    print(knowledge)
    return knowledge
