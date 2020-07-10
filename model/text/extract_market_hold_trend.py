# -*- coding: UTF-8 -*-
# 公司市场占有率变化趋势
# 比较少
import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    market_hold_trend_list = []
    market_hold_trend_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if '市场份额' in para:
            para = para.strip()
            if para in market_hold_trend_list:
                continue
            # logging.info("para:" + para)
            market_hold_trend_list.append(para)
            market_hold_trend_page_list.append(page)

    if len(market_hold_trend_list) == 0:
        return None

    new_list = []
    new_page_list = []
    for i in range(len(market_hold_trend_list)):
        para = market_hold_trend_list[i]
        page = market_hold_trend_page_list[i]
        if '。' not in para:
            para = utils.delete_index(para)
            new_list.append(para)
            new_page_list.append(page)
            continue
        sentence_list = para.split('。')
        for sentence in sentence_list:
            if '市场份额' in sentence:
                sentence = utils.delete_index(sentence)
                # logging.info("sentence:" + sentence)
                new_list.append(sentence + '。')
                new_page_list.append(page)

    candidate_list = []
    for i in range(len(new_list)):
        candidate = {"text": new_list[i],
                     "textPage": new_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    knowledge = {"type": "公司市场占有率变化趋势",
                 "text": '\n'.join(new_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(new_page_list)}
    return knowledge
