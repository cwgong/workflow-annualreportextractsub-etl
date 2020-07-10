# -*- coding: UTF-8 -*-
import model.utils as utils
import re
import logging


def extract_industry_layout(text_list, text_page_list):
    content_list = []
    page_list = []
    page_set = set()
    start = False
    t_level = -1
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        para = para.strip()
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
        for i in range(len(text_list)):
            para = text_list[i]
            page = text_page_list[i]
            para = para.strip()
            if enable_content(para):
                content_list.append(para)
                page_list.append(page)
                page_set.add(page)

    if len(content_list) == 0:
        return None
    logging.info(len(content_list))
    logging.info(content_list)

    candidate_list = []
    knowledge = {"type": "公司产业链布局",
                 "text": '\n'.join(content_list),
                 "candidate": candidate_list,
                 "pages": list(page_set)}

    return knowledge


def title_enable(para):
    key_words = ['产业', '行业', '业务']
    if '布局' not in para:
        return False
    for word in key_words:
        if word in para:
            return True
    return False


def enable_content(para):
    if len(para) < 40:
        return False
    rule_list = [
        r'.*在.{1,10}(领域|产业|行业).*布局.*',
        r'.*公司.{1,10}布局.*',
        r'.*完善.{0,10}布局.*']
    split_list = para.split('。')
    for split in split_list:
        for rule in rule_list:
            pattern = re.compile(rule)
            result = pattern.findall(split)
            if len(result) != 0:
                return True
    return False


