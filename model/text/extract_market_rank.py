# -*- coding: UTF-8 -*-
# 公司市场排名
# 必须包含具体的排名，不限制条数

import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    raw_list = []
    raw_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if ('排名' in para or '位居' in para or '位列' in para) and utils.contain_all_number(para):
            # logging.info("paragraph:" + para)
            raw_list.append(para)
            raw_page_list.append(page)

    if len(raw_list) == 0:
        return None

    rank_list = []
    rank_page_list = []
    for i in range(len(raw_list)):
        para = raw_list[i]
        page = raw_page_list[i]
        if '。' not in para:
            # logging.info('cannot find 。:' + para)
            continue
        sentence_list = para.split('。')
        for j in range(len(sentence_list)):
            sentence = sentence_list[j]
            if ('排名' in sentence or '位居' in sentence or '位列' in sentence) and utils.contain_all_number(sentence):
                # logging.info("sentence:" + sentence)
                rank_list.append(sentence + '。')
                rank_page_list.append(page)

    if len(rank_list) == 0:
        return None

    candidate_list = []
    for i in range(len(rank_list)):
        candidate = {"text": rank_list[i],
                     "textPage": rank_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    # 公司竞争优势是多段落的，默认全部都是知识
    knowledge = {"type": "公司市场排名",
                 "text": '\n'.join(rank_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(rank_page_list)}

    return knowledge
