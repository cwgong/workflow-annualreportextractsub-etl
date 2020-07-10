# -*- coding: UTF-8 -*-
# 公司竞争优势
# 1.先抽大标题下的所有段落
# 2.如果不包含句号，说明是标题，保留。再保留所有段落的第一句话。

import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    competitive_edge_list = []
    competitive_edge_page_list = []  # 用于 候选集 个体，必须一对一
    need_add = False
    break_with_title = False

    for i in range(len(text_list)):
        para = text_list[i].strip()
        page = text_page_list[i]

        if para.endswith('核心竞争力分析') and utils.is_title(para) != -1:
            need_add = True
            # logging.info("start title: " + para)
            continue

        if need_add and ("√适用" in para or "公司是否需要遵守特殊行业的披露要求" in para or len(para) <= 1):
            continue

        if need_add and '经营情况讨论与分析' in para:
            # logging.info("end title: " + para)
            break_with_title = True
            break

        if need_add:
            # logging.info(para)
            competitive_edge_list.append(para)
            competitive_edge_page_list.append(page)

    if len(competitive_edge_list) == 0:
        return None

    # 如果没有在 经营情况讨论与分析 停下,需要按标题序号重新过滤
    if not break_with_title:
        title_number_1 = 0
        title_number_2 = 0
        new_competitive_edge_list = []
        new_competitive_edge_page_list = []

        need_add = False
        for i in range(len(competitive_edge_list)):
            para = competitive_edge_list[i]
            page = competitive_edge_page_list[i]

            if utils.is_title(para) != -1:
                number_list = utils.extract_number(para)
                if len(number_list) == 0:  # 暂时只考虑数字
                    new_competitive_edge_list.append(para)
                    new_competitive_edge_page_list.append(page)
                    continue
                title_number = int(number_list[0])
                if title_number_1 + 1 == title_number:
                    title_number_1 = title_number
                    title_number_2 = 0
                else:  # 一级标题出现不连续
                    if title_number_2 + 1 == title_number:
                        title_number_2 = title_number
                    else:
                        # logging.info("end title: " + para)
                        break
            new_competitive_edge_list.append(para)
            new_competitive_edge_page_list.append(page)
    else:
        new_competitive_edge_list = competitive_edge_list
        new_competitive_edge_page_list = competitive_edge_page_list

    new_list = []
    for para in new_competitive_edge_list:
        if '\n' in para:
            para = para.replace('\n', '')
        if '。' not in para:
            new_list.append(para)
        else:
            sentence_list = para.split('。')
            new_list.append(sentence_list[0] + '。')

    candidate_list = []
    for i in range(len(new_list)):
        candidate = {"text": new_list[i],
                     "textPage": new_competitive_edge_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    # 公司竞争优势是多段落的，默认全部都是知识
    knowledge = {"type": "公司竞争优势",
                 "text": '\n'.join(new_list),
                 "candidate": candidate_list,
                 "pages": utils.remove_duplicate_item(new_competitive_edge_page_list)}

    return knowledge


# if __name__ == "__main__":
    # print(len("\n"))
#     print(utils.extract_number('(1)采购和销售环节'))
