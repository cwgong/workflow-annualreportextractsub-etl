# -*- coding: utf-8 -*-
# 公司资产权利受限情况

import service.utils as service_util
import model.table.extract_right_restrict_money as extract_right_restrict_money


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    # text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_right_restrict_money.extract(detail)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
