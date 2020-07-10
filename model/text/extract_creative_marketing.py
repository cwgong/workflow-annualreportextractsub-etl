# -*- coding: UTF-8 -*-
# 公司创意营销、新媒体营销、数字营销等情况
# 比较少
import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    creative_marketing_list = []
    creative_marketing_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if '创意营销' in para or '新媒体营销' in para or '数字营销' in para or '网红直播' in para or '抖音' in para :
            para = para.strip()
            para = utils.delete_index(para)
            if para in creative_marketing_list:
                continue
            # logging.info('para:' + para)
            creative_marketing_list.append(para)
            creative_marketing_page_list.append(page)

    if len(creative_marketing_list) == 0:
        return None

    candidate_list = []
    for i in range(len(creative_marketing_list)):
        candidate = {"text": creative_marketing_list[i],
                     "textPage": creative_marketing_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    knowledge = {"type": "公司创意-新媒体-数字营销",
                 "text": '\n'.join(creative_marketing_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(creative_marketing_page_list)}
    return knowledge
