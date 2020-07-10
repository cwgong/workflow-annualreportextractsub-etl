# -*- coding: UTF-8 -*-
# 公司主要产品的服务用途及功能情况
# [{"name":"公司主要产品的服务用途及功能情况",
#
# "value":[{"主要产品类型":"string",
#
# "产品名称":"string",
#
# "主要功能":"string",
#
# "主要应用领域":"string"}],
#
# "evidence_page_number":[int]}]

import logging
import model.utils as utils


def extract(text_list, text_page_list):

    function_keywords = ['功能', '解决方案']

    function_table_list = [['主要产品类型', '产品名称', '主要功能', '主要应用领域']]
    new_page_list = []

    function_list = []
    function_page_list = []

    type_temp_list = []
    type_temp_page_list = []

    product_type_list = []
    product_type_page_list = []

    business_flag = False
    business_title_number = -1
    number_list = -1
    main_business_list = []
    main_business_page_list = []
    # start_flag = False
    find_title_flag = False
    flag = False
    break_is_title = False
    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]
        if not utils.text_valid(para):
            continue
        if para.endswith('报告期内公司所从事的主要业务、经营模式及行业情况说明') or para.endswith('报告期内公司从事的主要业务') and flag == False:
            flag = True
            continue
        if (para.endswith('主要资产重大变化情况') or para.endswith('报告期内公司主要资产发生重大变化情况的说明')) and flag == True:
            break_is_title = True
            break
        if para.endswith('主要资产重大变化情况') == False and para.endswith('报告期内公司主要资产发生重大变化情况的说明') == False and flag == True:
            function_list.append(para)
            function_page_list.append(page)

    if break_is_title == False:  # 不规范的年报直接不做抽取
        logging.info('none')
        return None
    if len(function_list) == 0:
        logging.info('none')
        return None
    # logging.info(str(cost_list))

    for i in range(len(function_list)):
        para = function_list[i]
        page = function_page_list[i]

        if (para.endswith('主营业务') or para.endswith('公司主要业务')) and utils.title_level(
                para) > -1 and business_flag == False:
            business_flag = True
            business_title_number = utils.title_level(para)
            continue
        if utils.title_level(para) >= business_title_number:
            break
        if business_flag == True:
            main_business_list.append(para)
            main_business_page_list.append(page)

    if main_business_list == []:
        return None

    for i in range(len(main_business_list)):
        para = main_business_list[i]
        page = main_business_page_list[i]

        if utils.title_level(para) == -1 and find_title_flag == False:
            continue
        if utils.title_level(para) != -1 and find_title_flag == False:
            find_title_flag = True
            number_list = utils.title_level(para)  # 从整个部分直接到有子标题的那一段

            type_temp_list = []
            type_temp_page_list = []

            type_temp_list.append(para)
            type_temp_page_list.append(page)

        else:
            type_temp_list.append(para)
            type_temp_page_list.append(page)

        if len(main_business_list) == i + 1:
            product_type_list.append(type_temp_list)
            product_type_page_list.append(type_temp_page_list)
            break
        if utils.title_level(main_business_list[i + 1]) == number_list:
            product_type_list.append(type_temp_list)
            product_type_page_list.append(type_temp_page_list)
            find_title_flag = False
            continue

    if product_type_list == []:
        return None

    # if len(product_type_page_list) == 1:
    #     if product_type_page_list[0][0].endswith('业务') == False:
    #         return None
    # else:
    #     for type_list in product_type_page_list:
    for i in range(len(product_type_list)):
        function_item = ''
        vocation = ''
        product = ''
        domain = ''
        product_function_list = []

        type_list = product_type_list[i]
        type_page_list = product_type_page_list[i]
        if type_list == []:
            continue
        if '产品' not in type_list[0] and '业务' not in type_list[0]:
            continue
        else:
            text = utils.delete_index(type_list[0])
            vocation = text.split('：')[0]
            product_ = text.split('：')[0]
            product = product_.replace('业务','')
        for j in range(len(type_list)):
            product_para = type_list[j]
            product_para_page = type_page_list[j]
            if function_item == '':
                product_para = product_para.replace('；', '。')
                para_list = product_para.split('。')
                for word in function_keywords:
                    for para_function in para_list:
                        if word in para_function:
                            function_item = para_function
                            break
                    if function_item != '':
                        break

            if domain == '':
                product_para = product_para.replace('。', '，').replace('：', '，')
                para_list = product_para.split('，')
                for para_domain in para_list:
                    if '客户覆盖' in para_domain and '领域' in para_domain:
                        domain = para_domain
                        break
                    elif '应用' in para_domain and '领域' in para_domain:
                        domain = para_domain
                        break
        new_row = [product, vocation, function_item, domain]
        function_table_list.append(new_row)
        new_page_list.append(type_page_list[0])

    if len(function_table_list) == 1:
        return None

    else:
        knowledge_list = []
        for item in function_table_list:
            if item == ['主要产品类型', '产品名称', '主要功能', '主要应用领域']:
                continue
            if item[0] == '' or item[1] == '':
                continue
            item_dict = {"主要产品类型": item[0],
                         "产品名称": item[1],
                         "主要功能": item[2],
                         "主要应用领域": item[3]}
            knowledge_list.append(item_dict)
        knowledge = {"type": "公司主要产品的服务用途及功能情况",
                     "table": [{"name": "公司主要产品的服务用途及功能情况",
                                "value": knowledge_list,
                                "evidence_page_number": new_page_list}]
                     }
    return knowledge


if __name__ == "__main__":
    print(utils.extract_number('333.12'))
    print(utils.extract_number('333'))
