# -*- coding: UTF-8 -*-
# 创新能力


def extract(text_list, text_page_list):
    innovate_list = []
    innovate_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        if "创新业务" in para and "风险" not in para:
            innovate_list.append(para)
            innovate_page_list.append(text_page_list[i])
        # if len(innovate_list) == 0 and "科技" in para and "业务" in para:
        #     innovate_list.append(para)

    if len(innovate_list) == 0:
        return None

    candidate_list = []
    for i in range(len(innovate_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": innovate_list[i],
                     "textPage": innovate_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司创新能力(证券)",
                 "text": innovate_list[0],
                 "candidate": candidate_list,
                 "pages": innovate_page_list[0]}

    return knowledge

