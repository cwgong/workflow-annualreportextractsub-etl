# -*- coding: UTF-8 -*-
# 公司产能扩张规划及进展

import service.utils as service_util
import model.text.extract_capacity_extention_plan as extract_capacity_extention_plan


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    knowledge = extract_capacity_extention_plan.extract(detail)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
