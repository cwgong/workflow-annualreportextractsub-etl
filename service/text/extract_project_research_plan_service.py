# -*- coding: UTF-8 -*-
# 公司研发规划及进展

import service.utils as service_util
import model.text.extract_project_research_plan as extract_project_research_plan


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    knowledge = extract_project_research_plan.extract(detail)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
