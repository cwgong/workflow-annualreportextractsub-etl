# -*- coding: UTF-8 -*-
# 公司商誉来源与商誉减值来源情况
# [{"name":"商誉来源",
# "value":[{"日期":string,
# "商誉来源":string,
# "商誉年份":string,
# "商誉金额":float}],
# "evidence_page_number":[int]},
# {"name":"商誉减值来源",
# "value":[{"日期":string,
# "商誉减值来源":string,
# "商誉减值年份":string,
# "商誉减值金额":float}],
# "evidence_page_number":[int]}]

import logging
import model.utils as utils


def extract(detail, title):
    reputation_table = None
    reputation_page = None
    reputation_text_list = []

    # 改成按文本抽取 合计
    for i in range(len(detail)):
        item_type = detail[i].get('type')
        content = detail[i].get('content')
        if item_type == 'text':
            if content.endswith('商誉账面原值'):
                for j in range(1, 100):
                    next_item = detail[i + j]
                    next_type = next_item.get('type')
                    next_content = next_item.get('content')
                    next_page = next_item.get('page_num')
                    if next_type == 'text':
                        if '商誉减值准备' in next_content or '合计' in next_content:
                            break
                        # logging.info('text1: ' + next_item.get('content'))
                        if utils.contain_number(next_content):
                            reputation_text_list.append(next_content)
                            reputation_page = next_page

                    else:
                        reputation_table = next_content
                        reputation_page = next_page
                        break
                break

    reputation_reduce_table = None
    reputation_reduce_page = None
    reputation_reduce_text_list = []
    for i in range(len(detail)):
        item_type = detail[i].get('type')
        content = detail[i].get('content')
        if item_type == 'text':
            if content.endswith('商誉减值准备'):
                title_level = utils.is_title(content)
                for j in range(1, 100):
                    next_item = detail[i + j]
                    next_type = next_item.get('type')
                    next_content = next_item.get('content')
                    next_page = next_item.get('page_num')
                    if next_type == 'text':
                        next_level = utils.is_title(next_content)
                        if next_level == title_level or '合计' in next_content:
                            break
                        # logging.info('text2: ' + next_content)
                        if utils.contain_number(next_content):
                            reputation_reduce_text_list.append(next_content)
                            reputation_reduce_page = next_page
                    else:
                        reputation_reduce_table = next_content
                        reputation_reduce_page = next_page
                        break
                break

    if (reputation_table is None or len(reputation_table) <= 1) and (reputation_reduce_table is None or len(reputation_reduce_table) <= 1):
        return None

    reputation_source_list = []
    reputation_value_list = []
    if reputation_table is not None:
        logging.info(utils.get_table_line(reputation_table[0]))
        for i in range(1, len(reputation_table)):
            if len(reputation_table[i]) < 3:
                continue
            item = reputation_table[i][2]
            name = reputation_table[i][0]
            if item is None or name is None:
                continue
            item_number = utils.get_item_number(item)
            name = name.replace('\n', '').replace(' ', '')
            if item_number == 0 or len(name) == 0:
                continue
            if '合计' == name:
                continue
            reputation_source_list.append(name)
            reputation_value_list.append(item_number)
    elif len(reputation_text_list) > 0:
        logging.info('text list length:' + str(len(reputation_text_list)))
        for i in range(len(reputation_text_list)):
            text = reputation_text_list[i]
            sub_list = text.split(' ')
            if len(sub_list) < 3:
                continue
            source_item = sub_list[0]
            value_item = sub_list[2]
            if source_item is None or value_item is None:
                continue
            source_item = source_item.replace('\n', '').replace(' ', '')
            value_item = utils.get_item_number(value_item)
            if len(source_item) == 0 or value_item == 0:
                continue

            reputation_source_list.append(source_item)
            reputation_value_list.append(value_item)

    reputation_reduce_source_list = []
    reputation_reduce_value_list = []
    if reputation_reduce_table is not None:
        logging.info(utils.get_table_line(reputation_reduce_table[0]))
        for i in range(1, len(reputation_reduce_table) - 1):
            if len(reputation_reduce_table[i]) < 3:
                continue
            item = reputation_reduce_table[i][2]
            name = reputation_reduce_table[i][0]
            if item is None or name is None:
                continue
            item_number = utils.get_item_number(item)
            name = name.replace('\n', '').replace(' ', '')
            if item_number == 0 or len(name) == 0:
                continue
            if '合计' == name:
                continue
            reputation_reduce_source_list.append(name)
            reputation_reduce_value_list.append(item_number)
    elif len(reputation_reduce_text_list) > 0:
        logging.info('text list length:' + str(len(reputation_reduce_text_list)))
        for i in range(len(reputation_reduce_text_list)):
            text = reputation_reduce_text_list[i]
            sub_list = text.split(' ')
            if len(sub_list) < 3:
                continue
            source_item = sub_list[0]
            value_item = sub_list[2]
            if source_item is None or value_item is None:
                continue
            source_item = source_item.replace('\n', '').replace(' ', '')
            value_item = utils.get_item_number(value_item)
            if len(source_item) == 0 or value_item == 0:
                continue
            reputation_reduce_source_list.append(source_item)
            reputation_reduce_value_list.append(value_item)

    if len(reputation_source_list) == 0 and len(reputation_reduce_source_list) == 0:
        return None

    year = utils.extract_number(title)[0]
    value_date = year + '1231'
    value_list = []
    for i in range(len(reputation_source_list)):
        value_list.append({"日期": value_date,
                           "商誉来源": reputation_source_list[i],
                           "商誉年份": year,
                           "商誉金额": reputation_value_list[i]})

    value_list2 = []
    for i in range(len(reputation_reduce_source_list)):
        value_list2.append({"日期": value_date,
                            "商誉减值来源": reputation_reduce_source_list[i],
                            "商誉减值年份": year,
                            "商誉减值金额": reputation_reduce_value_list[i]})

    knowledge = {"type": "公司商誉来源与商誉减值来源情况",
                 "table": [{"name": "商誉来源",
                            "value": value_list,
                            "evidence_page_number": [reputation_page]},
                           {"name": "商誉减值来源",
                            "value": value_list2,
                            "evidence_page_number": [reputation_reduce_page]}
                           ]
                 }
    return knowledge


if __name__ == "__main__":
    print('深圳市环球易购电子商务有限公 866,260,327.26          866,260,327.26'.split(' '))

