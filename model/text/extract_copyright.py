# -*- coding: UTF-8 -*-
# 专利数量及金额

import model.utils as utils


def extract(text_list, text_page_list):
    patent_list = []
    patent_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "专利" in para and ("件" in para or "项" in para) and utils.contain_number(para):
            # pattern1 = re.compile(r'\d+件')
            # result1 = pattern1.findall(para)
            #
            # pattern2 = re.compile(r'\d+项')
            # result2 = pattern2.findall(para)

            # if len(result1) > 0 or len(result2) > 0:
            patent_list.append(utils.delete_suffix(para, '如下'))
            patent_page_list.append(text_page_list[i])

    if len(patent_list) == 0:
        return None

    candidate_list = []
    for i in range(len(patent_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": patent_list[i],
                     "textPage": patent_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司专利数量及金额(计算机)",
                 "text": patent_list[0],
                 "candidate": candidate_list,
                 "pages": patent_page_list[0]}

    return knowledge

