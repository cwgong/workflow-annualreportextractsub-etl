# -*- coding: UTF-8 -*-
# 营业网点 / 分支机构

import model.utils as utils
import re


# 证券
def extract_security(text_list, text_page_list):
    branch_list = []
    branch_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "营业部" in para and "家" in para and "共" in para and len(branch_list) == 0 and '扶贫' not in para:
            para = utils.delete_suffix(para, '如下')  # 之后所有
            # para = delete_suffix_sentence(para, '参见')  # 整句
            branch_list.append(para)
            branch_page_list.append(text_page_list[i])

    if len(branch_list) == 0:
        return None

    candidate_list = []
    for i in range(len(branch_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": branch_list[i],
                     "textPage": branch_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司分支机构(证券,保险)",
                 "text": branch_list[0],
                 "candidate": candidate_list,
                 "pages": branch_page_list[0]}

    return knowledge


# 银行
def extract_bank(text_list, text_page_list):
    # branch_list = []
    branch_page_list = []

    keywords = ['分支机构', '营业网点', '分行', '支行']
    verbs = ['设', '有', '达', '覆盖']
    unit_rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9]{1,})(家|个)"
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
            verb_c = 0
            for verb in verbs:
                if verb in s:
                    verb_c = 1
                    break
            if key_c + verb_c == 2:
                s = utils.get_striped(s)
                r = re.match(unit_rgx, s)
                if r is not None:
                    s = s + '。'
                    candidates.append(s)
                    branch_page_list.append(text_page_list[i])

    if len(candidates) == 0:
        return None

    # 排序后的候选集作为最后的结果---页码的数组需要同样的排序，暂时忽略
    branch_list = candidates
    candidate_list = []
    for i in range(len(branch_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": branch_list[i],
                     "textPage": branch_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司营业网点(银行)",
                 "text": branch_list[0],
                 "candidate": candidate_list,
                 "pages": branch_page_list[0]}

    return knowledge


def candidates_filter_sort(candidates):
    candidates_ = []
    unit_rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9]{1,})(家|个)"
    dic = {}
    for c in candidates:
        unit_count = len(re.findall(unit_rgx, c))
        dic[c] = unit_count
    source_count_sort = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for c, count in source_count_sort:
        candidates_.append(c)
    return candidates_

