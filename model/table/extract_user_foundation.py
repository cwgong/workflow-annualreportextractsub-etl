# -*- coding: UTF-8 -*-
# 客户基础

import model.utils as utils


def extract(text_list, text_page_list):
    manage_list = []
    manage_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if '经纪业务' in para and '客户' in para and ('万户' in para or '个' in para) and utils.contain_number(
                para):
            # if '经纪业务' in para and '客户' in para and ('零售' in para or '个人' in para)
            # and '机构' in para and contain_number(para) and '风险' not in para:
            manage_list.append(para)
            manage_page_list.append(text_page_list[i])

    table_list = [{"name": "经纪业务零售客户数（万户）",
                   "value": None,
                   "evidence_page_number": manage_page_list},
                  {"name": "经纪业务一般法人机构客户数（万户）",
                   "value": None,
                   "evidence_page_number": manage_page_list},
                  {"name": "经纪业务总客户数（万户）",
                   "value": None,
                   "evidence_page_number": manage_page_list}
                  ]
    knowledge = {"type": "公司客户基础(证券)",
                 "text": '\n'.join(manage_list),
                 "table": table_list}

    return knowledge
