# -*- coding: UTF-8 -*-

import logging

import model.utils as utils


def extract_industry_position(text_list, text_page_list):
    content_list = []
    page_list = []
    page_set = set()
    start = False
    t_level = -1
    start_title = ''

    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        para = para.strip()
        if not utils.text_valid(para):
            continue

        # 相关段落开始的标题
        if not start and ('产业链地位' in para or '行业地位' in para) and utils.title_level(para) > -1:
            start = True
            t_level = utils.title_level(para)
            start_title = para
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

    if len(content_list) == 0 or (
            len(content_list) > 4 and ('基本情况' in start_title or '发展阶段' in start_title or '发展情况' in start_title)):
        content_list.clear()
        # TODO 内容的关键词，内容只用关键词匹配好像是不够的，应该是使用规则；还有一些规则，居**位
        content_key_words = ['龙头企业', '行业龙头地位', '行业前列', '领军企业']
        for i in range(len(text_list)):
            para = text_list[i]
            page = text_page_list[i]
            para = para.strip()
            if utils.is_title(para) > -1:
                continue
            for word in content_key_words:
                if word in para:
                    content_list.append(para)
                    page_list.append(page)
                    page_set.add(page)
                    break
    if len(content_list) == 0:
        return None
    logging.info(len(content_list))
    logging.info(content_list)

    candidate_list = []

    knowledge = {"type": "公司行业地位",
                 "text": '\n'.join(content_list),
                 "candidate": candidate_list,
                 "pages": list(page_set)}

    return knowledge
