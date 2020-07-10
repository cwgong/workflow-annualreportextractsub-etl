# -*- coding: UTF-8 -*-
# 税收优惠

import service.utils as service_util
import model.text.extract_tax as extract_tax


def extract_free(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_free)


def extract_vat(start_at, end_at, time_field):
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method_vat)


def extract_method_free(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_tax.extract_tax(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


def extract_method_vat(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_tax.extract_vat(text_list, text_page_list, table_list, table_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
