# -*- coding: UTF-8 -*-
# 市场占有率
# 1,技术类
# 2,全部，要含有数字，可多条
# import logging

import model.utils as utils


def extract(text_list, text_page_list):
    market_list = []
    market_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "市场占有率" in para or "市占率" in para or "市场规模" in para:
            market_list.append(para)
            market_page_list.append(text_page_list[i])
        if len(market_list) == 0 and "覆盖全国" in para and utils.contain_number(para):
            market_list.append(para)
            market_page_list.append(text_page_list[i])
        if len(market_list) == 0 and "酒店规模" in para and utils.contain_number(para):
            market_list.append(para)
            market_page_list.append(text_page_list[i])
        if len(market_list) == 0 and "餐饮规模" in para and utils.contain_number(para):
            market_list.append(para)
            market_page_list.append(text_page_list[i])

    if len(market_list) == 0:
        return None

    candidate_list = []
    for i in range(len(market_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": market_list[i],
                     "textPage": market_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司市场占有率(技术)",
                 "text": market_list[0],
                 "candidate": candidate_list,
                 "pages": market_page_list[0]}

    return knowledge


# 抽取所有类型
def extract_all(text_list, text_page_list):
    temp_list = []
    temp_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if ("市场占有率" in para or "市占率" in para) and utils.contain_number(para) and '%' in para:
            para = utils.delete_index(para)
            temp_list.append(para)
            temp_page_list.append(page)

    market_list = []
    market_page_list = []
    for i in range(len(temp_list)):
        para = temp_list[i]
        page = temp_page_list[i]
        sentence_list = para.split('。')
        for sentence in sentence_list:
            sentence = sentence.strip()
            sentence = utils.delete_index(sentence) + '。'
            if ("市场占有率" in sentence or "市占率" in sentence) and utils.contain_number(sentence) and '%' in sentence:
                # logging.info("sentence: " + sentence)
                market_list.append(sentence)
                market_page_list.append(page)

    if len(market_list) == 0:
        return None

    candidate_list = []
    for i in range(len(market_list)):
        candidate = {"text": market_list[i],
                     "textPage": market_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    knowledge = {"type": "公司市场占有率",
                 "text": '\n'.join(market_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(market_page_list)}

    return knowledge
