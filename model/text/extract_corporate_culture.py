# -*- coding: UTF-8 -*-
# 公司企业文化特征，单段落
# 1.企业文化所在段落
# 2.如果1.是标题，抽取下一个标题前的所有段落
# 3.去重
import model.utils as utils
# import logging


def extract(text_list, text_page_list):
    corporate_culture_list = []
    corporate_culture_page_list = []
    # need_add = False
    # title_index = -1
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_list[i]
        if '企业文化' in para:
            title_index = utils.is_title(para)
            if title_index == -1:  # 不带标题序号
                corporate_culture_list.append(para)
                corporate_culture_page_list.append(page)
            else:
                # logging.info('start title:' + para)
                corporate_culture_list.append(text_list[i + 1])
                corporate_culture_page_list.append(text_page_list[i + 1])
                corporate_culture_list.append(text_list[i + 2])
                corporate_culture_page_list.append(text_page_list[i + 2])
                continue
        if '愿景' in para and '新愿景股权' not in para and para not in corporate_culture_list:
            title_index = utils.is_title(para)
            if title_index == -1:  # 不带标题序号
                corporate_culture_list.append(para)
                corporate_culture_page_list.append(page)
            else:
                # logging.info('start title:' + para)
                corporate_culture_list.append(text_list[i + 1])
                corporate_culture_page_list.append(text_page_list[i + 1])

    if len(corporate_culture_list) == 0:
        return None

    # item 去重，page也需要变化
    new_list = []
    new_page_list = []
    for i in range(len(corporate_culture_list)):
        item = corporate_culture_list[i]
        item = item.strip()
        item = utils.delete_index(item)
        if item in new_list:
            continue
        else:
            # logging.info("para: " + item)
            new_list.append(item)
            new_page_list.append(corporate_culture_page_list[i])

    candidate_list = []
    for i in range(len(new_list)):
        if i == 0:
            isKnowledge = True
        else:
            isKnowledge = False
        candidate = {"text": new_list[i],
                     "textPage": new_page_list[i],
                     "isKnowledge": isKnowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司企业文化特征",
                 "text": new_list[0],
                 "candidate": candidate_list,
                 "pages": new_page_list[0]}

    return knowledge


# if __name__ == "__main__":
#     print(utils.is_title('一、聚焦重点、加速研发，培育持续发展动能'))
#     print(utils.extract_number('12今天'))
#  c. 企业文化活动；
