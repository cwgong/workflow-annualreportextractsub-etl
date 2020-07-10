# -*- coding: UTF-8 -*-
# 公司创意营销、新媒体营销、数字营销等情况

import service.utils as service_util
import model.text.extract_creative_marketing as extract_creative_marketing


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name,title):
    # print('extract_method')
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_creative_marketing.extract(text_list, text_page_list)
    text_knowledges = []
    table_knowledges = []
    if knowledge is not None:
        text_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
