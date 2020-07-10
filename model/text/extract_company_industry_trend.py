# -*- coding: UTF-8 -*-
import model.utils as utils
import logging


def extract_company_industry_trend(text_list, text_page_list):
    content_list = []
    page_list = []
    page_set = set()
    start = False
    t_level = -1
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if not utils.text_valid(para):
            continue
        if not start and utils.title_level(para) > -1 and title_enable(para):
            start = True
            t_level = utils.title_level(para)
            continue
        if start and utils.title_level(para) >= t_level:
            # 如果没有获取到数据，继续往下找
            if len(content_list) == 0:
                start = False
                continue
            break
        if start:
            content_list.append(para)
            page_list.append(page)
            page_set.add(page)

    if len(content_list) == 0:
        return None
    logging.info(len(content_list))
    logging.info(content_list)

    candidate_list = []
    knowledge = {"type": "公司所属行业发展趋势",
                 "text": '\n'.join(content_list),
                 "candidate": candidate_list,
                 "pages": list(page_set)}

    return knowledge


def title_enable(para):
    key_words = ['现状', '发展趋势', '发展情况', '发展阶段']
    object_words = ['行业', '产业']
    for object_word in object_words:
        if object_word in para:
            break
        return False
    for word in key_words:
        if word in para:
            return True
    return False



