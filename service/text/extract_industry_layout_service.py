# -*- coding: UTF-8 -*-

import service.utils as service_util
import model.text.extract_industry_layout as extract_industry_layout


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_industry_layout.extract_industry_layout(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


def extract(start_at, end_at, time_field):
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)