# -*- coding: UTF-8 -*-
# 主要渠道


def extract(text_list, text_page_list):
    main_list = []
    main_page_list = []
    need_add = False
    for i in range(len(text_list)):
        para = text_list[i]
        if para.endswith('销售模式'):
            need_add = True
            continue

        if need_add:
            main_list.append(para)
            main_page_list.append(text_page_list[i])
            need_add = False

        # if '经营模式' in para and '说明' not in para:
        #     main_list.append(para)
    if len(main_list) == 0:
        return None

    candidate_list = []
    for i in range(len(main_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": main_list[i],
                     "textPage": main_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司主要渠道(工程)",
                 "text": main_list[0],
                 "candidate": candidate_list,
                 "pages": main_page_list[0]}
    return knowledge

