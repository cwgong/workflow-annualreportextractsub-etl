# -*- coding: UTF-8 -*-
# 传媒 著作权

import service.utils as service_util
import model.table.extract_struct_media as extract_media


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    if '传媒' not in induhc2:
        return text_knowledges, table_knowledges
    # text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_media.extract()
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
