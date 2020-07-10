# -*- coding: UTF-8 -*-
# 房地产
# 房地产指标(房地产)
# 房地产列表（在售、新增储备、累计储备的地区分布）
# 房地产权益列表（合同金额/面积、权益比例）

import service.utils as service_util
import model.table.extract_real_property as extract_real_property


def extract(start_at, end_at, time_field):
    # print('extract')
    service_util.request_pdf_always(start_at, end_at, time_field, extract_method)


def extract_method(detail, induhc2, sec_name, title):
    # print('extract_method')
    text_knowledges = []
    table_knowledges = []
    if '房地产' not in induhc2:
        return text_knowledges, table_knowledges
    text_list, text_page_list, table_list, table_page_list = service_util.parse_detail(detail)
    knowledge = extract_real_property.extract(table_list, table_page_list)
    if knowledge is not None:
        table_knowledges.append(knowledge)
    return text_knowledges, table_knowledges
