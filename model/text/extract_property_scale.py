# -*- coding: UTF-8 -*-
# 主动管理资产规模

import model.utils as utils


def extract(text_list, text_page_list):
    property_list = []
    property_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "规模" in para:
            if "行业发展" in para:
                continue
            if ("主动管理" in para or "主动管理资产" in para or ("主动" in para and "资产管理" in para)) and ("亿元" in para or "万元" in para):
                property_list.append(para)
                property_page_list.append(text_page_list[i])
            if "资产管理规模" in para and utils.contain_number(para) and ("亿元" in para or "万元" in para):
                property_list.append(para)
                property_page_list.append(text_page_list[i])
            if "资管" in para and utils.contain_number(para) and ("亿元" in para or "万元" in para):
                property_list.append(para)
                property_page_list.append(text_page_list[i])

        # if "主动" in para and "管理规模" in para and "亿元" in para and contain_number(para):
        #     property_list.append(para)
        # if "资产" in para and "管理规模" in para and "亿元" in para and contain_number(para):
        #     property_list.append(para)
        # if "规模" in para and "资管" in para and "亿元" in para and contain_number(para):
        #     property_list.append(para)

    if len(property_list) == 0:
        return None

    candidate_list = []
    for i in range(len(property_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": property_list[i],
                     "textPage": property_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司主动管理资产规模(证券)",
                 "text": property_list[0],
                 "candidate": candidate_list,
                 "pages": property_page_list[0]}

    return knowledge
