# -*- coding: UTF-8 -*-
# 银行-营业网点
# 证券-分支机构

import service.utils as service_util
import model.text.extract_branch as extract_branch


def extract_bank(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_bank)


def extract_security(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_security)


def extract_method_bank(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    if '银行' not in induhc2:
        return [], []
    knowledge = extract_branch.extract_bank(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


def extract_method_security(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    if '证券' not in induhc2 and '保险' not in induhc2:
        return [], []
    knowledge = extract_branch.extract_security(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
