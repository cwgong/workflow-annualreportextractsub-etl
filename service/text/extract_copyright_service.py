# -*- coding: UTF-8 -*-
# 专利数量及金额

import service.utils as service_util
import model.text.extract_copyright as extract_copyright


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    if '计算机' not in induhc2:
        return [], []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_copyright.extract(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
