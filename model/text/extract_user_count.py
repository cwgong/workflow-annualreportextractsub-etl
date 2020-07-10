# -*- coding: UTF-8 -*-
# 客户数量
import re
import model.utils as utils


# 银行
def extract(text_list, text_page_list):
    # user_count_list = []
    user_count_page_list = []

    keywords = ['零售客户', '公司客户', '零售非零客户', '企业客户']
    unit_rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9|千|万]{1,})(户|人)"
    candidates = []
    for i in range(int(len(text_list) * (1 / 3))):
        p = text_list[i]
        if len(p) > 1000 or len(p) < 10:
            continue
        for s in p.split("。"):
            key_c = 0
            for keyword in keywords:
                if keyword in s:
                    key_c = 1
                    break
            if key_c == 1:
                s = utils.get_striped(s)
                r = re.match(unit_rgx, s)
                # unit_count = len(re.findall(unit_rgx, s))
                if r is not None:
                    s = s + '。'
                    candidates.append(s)
                    user_count_page_list.append(text_page_list[i])

    if len(candidates) == 0:
        return None

    user_count_list = candidates
    # user_count_list = candidates_filter_sort(candidates)
    candidate_list = []
    for i in range(len(user_count_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": user_count_list[i],
                     "textPage": user_count_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司客户数量(银行)",
                 "text": user_count_list[0],
                 "candidate": candidate_list,
                 "pages": user_count_page_list[0]}
    return knowledge


# 根据观察，将多个 c 合并起来效果可能较好，暂不处理
def candidates_filter_sort(candidates):
    candidates_ = []
    unit_rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9|千|万]{1,})(户|人)"
    dic = {}
    for c in candidates:
        unit_count = len(re.findall(unit_rgx, c))
        dic[c] = unit_count
    source_count_sort = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for c, count in source_count_sort:
        candidates_.append(c)
    return candidates_

