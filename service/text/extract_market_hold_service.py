# -*- coding: UTF-8 -*-
# 市场占有率

import service.utils as service_util
import model.text.extract_market_hold as extract_market_hold
import model.text.extract_market_hold_trend as extract_market_hold_trend


# 仅抽取技术类
def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    if '技术' not in induhc2:
        return [], []
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_market_hold.extract(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


# 全类型抽取
def extract_all(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_all)


def extract_method_all(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_market_hold.extract_all(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


# 市场占有率变化趋势
def extract_trend(start_at, end_at, time_field):
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_trend)


def extract_method_trend(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_market_hold_trend.extract(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
