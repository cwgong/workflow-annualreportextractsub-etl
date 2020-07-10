# -*- coding: UTF-8 -*-
# 公司主营产品技术趋势
# 比较少
import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    technique_trend_list = []
    technique_trend_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if ('技术趋势' in para or '技术发展' in para) and '技术发展股份' not in para and '技术发展有限' not in para \
                and '补助' not in para and '技术发展公司' not in para and '技术发展中心' not in para and '技术发展成就' not in para\
                and '技术发展总公司' not in para and '技术发展有采购商品' not in para and '技术发展部' not in para:
            para = para.strip()
            para = utils.delete_index(para)
            if para in technique_trend_list:
                continue
            # logging.info('para:' + para)
            technique_trend_list.append(para)
            technique_trend_page_list.append(page)

    if len(technique_trend_list) == 0:
        return None

    candidate_list = []
    for i in range(len(technique_trend_list)):
        candidate = {"text": technique_trend_list[i],
                     "textPage": technique_trend_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    knowledge = {"type": "公司主营产品技术趋势",
                 "text": '\n'.join(technique_trend_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(technique_trend_page_list)}
    return knowledge
