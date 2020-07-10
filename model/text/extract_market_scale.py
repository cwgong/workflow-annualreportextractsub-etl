# -*- coding: UTF-8 -*-
# 市场规模

import model.utils as utils


def extract(text_list, text_page_list):
    market_scale_list = []
    market_scale_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "产业规模" in para or "市场规模" in para or '产值' in para and ('亿元' in para or '万元' in para) and utils.contain_number(para):
            market_scale_list.append(para)
            market_scale_page_list.append(text_page_list[i])

    if len(market_scale_list) == 0:
        return None

    candidate_list = []
    for i in range(len(market_scale_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": market_scale_list[i],
                     "textPage": market_scale_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司市场规模(技术)",
                 "text": market_scale_list[0],
                 "candidate": candidate_list,
                 "pages": market_scale_page_list[0]}

    return knowledge

