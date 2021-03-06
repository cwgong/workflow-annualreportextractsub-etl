# -*- coding: UTF-8 -*-

import model.text.extract_rd_plan as extract_rd_plan
import service.utils as service_util


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_rd_plan.extract_rd_plan(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges


def extract(start_at, end_at, time_field):
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)
