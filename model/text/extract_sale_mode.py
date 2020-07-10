# -*- coding: UTF-8 -*-
# 营销模式


def extract(text_list, text_page_list):
    cooperate_list = []
    cooperate_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "营销渠道" in para:
            cooperate_list.append(para)
            cooperate_page_list.append(text_page_list[i])
        if "销售渠道" in para:
            cooperate_list.append(para)
            cooperate_page_list.append(text_page_list[i])
        if "直销" in para:
            cooperate_list.append(para)
            cooperate_page_list.append(text_page_list[i])

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

    knowledge = {"type": "公司营销模式(技术,制造)",
                 "text": cooperate_list[0],
                 "candidate": candidate_list,
                 "pages": cooperate_page_list[0]}

    return knowledge

