# -*- coding: UTF-8 -*-
# 信托数量


def extract(text_list, text_page_list):
    count_list = []
    count_page_list = []
    for i in range(len(text_list)):
        para = text_list[i]
        # if "信托规模" in para and len(count_list) == 0:
        #     count_list.append(para)
        if "信托项目" in para and len(count_list) == 0:
            sentence_list = para.split('。')
            if len(sentence_list) != 1:
                para = sentence_list[0] + '。'
            count_list.append(para)
            count_page_list.append(text_page_list[i])

    if len(count_list) == 0:
        return None

    candidate_list = []
    for i in range(len(count_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": count_list[i],
                     "textPage": count_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司信托项目数量及资产规模(信托)",
                 "text": count_list[0],
                 "candidate": candidate_list,
                 "pages": count_page_list[0]}

    return knowledge

