# -*- coding: UTF-8 -*-
import logging
import model.utils as utils
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def extract(text_list, text_page_list):
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
        if not start and utils.title_level(para) > -1 and len(para) < 25 and (para.endswith('先进性') or para.endswith('可替代性') or para.endswith('行业地位') or para.endswith('领先优势')):
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

    logging.info(len(content_list))
    logging.info(content_list)

    if len(content_list) == 0:
        return None

    candidate_list = []

    knowledge = {"type": "公司主要产品的技术先进性及可替代性",
                 "text": '\n'.join(content_list),
                 "candidate": candidate_list,
                 "pages": list(page_set)}

    return knowledge

