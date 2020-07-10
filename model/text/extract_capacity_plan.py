# -*- coding: UTF-8 -*-
import model.utils as utils
import logging


def extract_capacity_plan(text_list, text_page_list):
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
    print(len(content_list))
    print(content_list)

    candidate_list = []
    knowledge = {"type": "公司产能规划",
                 "text": '\n'.join(content_list),
                 "candidate": candidate_list,
                 "pages": list(page_set)}

    return None


def title_enable(para):
    key_words = ['研发计划', '研发规划', '研发力度', '技术创新', '科研创新', '技术优势']
    for word in key_words:
        if word in para:
            return True
    return False
