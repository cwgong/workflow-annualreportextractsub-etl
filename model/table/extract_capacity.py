# -*- coding: UTF-8 -*-
# 公司主要产品产能产销情况
# 产能
# 产能利用率=产量/产能
# 产销率=销量/产量
# 注意统一单位

# 1.抽取 产能、产量、销量

import logging
import model.utils as utils
import re


def extract(detail):
    text_list = []
    table_list = []
    text_page_list = []
    table_page_list = []
    for i in range(len(detail)):
        item_type = detail[i].get('type')
        content = detail[i].get('content')
        page = detail[i].get('page_num')
        if item_type == 'text':
            if '产能' in content and utils.contain_number(content) and utils.has_unit(content) and\
                    ('年' in content or '月' in content or '日' in content) and content not in text_list:
                # logging.info('产能:' + content)
                text_list.append(content)
                text_page_list.append(page)
        elif item_type == 'table':
            if len(content) <= 1:
                continue
            row_1_string = utils.get_table_line(content[0])
            row_1_string = row_1_string.replace(' ', '').replace('（', '').replace('）', '')
            if ('产量' in row_1_string or '销量' in row_1_string) and ('产品' in row_1_string or '主要' in row_1_string) and '销量变动' not in row_1_string and len(table_list) == 0:
                # logging.info('产量/销量：' + str(content))
                table_list.append(content)
                table_page_list.append(page)

    new_text_list = []
    new_text_page_list = []
    for i in range(len(text_list)):
        text = text_list[i]
        if '。' not in text:
            continue
        sentence_list = text.split('。')
        for j in range(len(sentence_list)):
            sentence = sentence_list[j] + '。'
            if '产能' in sentence and utils.contain_number(sentence) and utils.has_unit(sentence) \
                    and ('年' in sentence or '月' in sentence or '日' in sentence) and sentence not in new_text_list:
                # logging.info('产能:' + sentence)
                new_text_list.append(sentence)
                new_text_page_list.append(text_page_list[i])

    new_table = [['主要产品', '产量', '销量', '产销率']]
    new_table_page_list = []
    for i in range(len(table_list)):
        table = table_list[i]

        main_product_index = 0
        produce_quantity_index = -1
        sale_quantity_index = -1
        capacity_use_index = -1
        row_1 = table[0]
        for j in range(len(row_1)):
            item = row_1[j]
            if item is None:
                continue
            item = row_1[j].replace('\n', '').replace(' ', '').replace('（', '').replace('）', '')
            if '主要产品' in item:
                main_product_index = j
            elif '产品' in item:
                main_product_index = j
            elif '主要' in item:
                main_product_index = j
            if (item.endswith('产量') or item.startswith('产量') or '生产量' in item) and produce_quantity_index == -1:
                produce_quantity_index = j
            if item.endswith('销量') or item.startswith('销量') or '销售量' in item and sale_quantity_index == -1:
                sale_quantity_index = j
            if '产能利用率' in item and capacity_use_index == -1:
                capacity_use_index = j

        if produce_quantity_index == -1 and sale_quantity_index == -1:
            continue
        for j in range(1, len(table)):
            row = table[j]
            main_product = row[main_product_index]
            if main_product is None:
                main_product = ''
            main_product = main_product.replace('\n', '').replace(',', '').replace(' ', '')

            produce_quantity = row[produce_quantity_index]
            if produce_quantity is None:
                produce_quantity = ''
            produce_quantity = produce_quantity.replace('\n', '').replace(',', '')

            sale_quantity = row[sale_quantity_index]
            if sale_quantity is None:
                sale_quantity = ''
            sale_quantity = sale_quantity.replace('\n', '').replace(',', '')

            temp_numbers = utils.extract_number(sale_quantity)
            if len(temp_numbers) > 0:
                sale_quantity_num = float(temp_numbers[0])
            else:
                sale_quantity_num = None

            temp_numbers = utils.extract_number(produce_quantity)
            if len(temp_numbers) > 0:
                produce_quantity_num = float(temp_numbers[0])
            else:
                produce_quantity_num = None

            if produce_quantity_num == 0:
                logging.info('produce quantity zero! str:' + produce_quantity + " num: " + str(produce_quantity_num))
                produce_quantity_num = None
            if sale_quantity_num is not None and produce_quantity_num is not None:
                produce_sale_rate = str(round(sale_quantity_num / produce_quantity_num, 4))
            else:
                produce_sale_rate = ''
            new_row = [main_product, produce_quantity, sale_quantity, produce_sale_rate]
            new_table.append(new_row)
        new_table_page_list.append(table_page_list[i])

    if len(new_table) == 1 and len(new_text_list) == 0:
        knowledge = None
    elif len(new_table) == 1 and len(new_text_list) > 0:
        knowledge_value = [{"主要产品": None,
                            "产能": None,
                            "产量": None,
                            "销量": None,
                            "产能利用率": None,
                            "产销率": None}]
        knowledge = {"type": "公司主要产品产能产销情况",
                     "table": [{"name": "公司主要产品产能产销情况",
                                "value": knowledge_value,
                                "evidence_page_number": utils.remove_duplicate_item(new_text_page_list)}],
                     "text": '\n'.join(new_text_list)
                     }
        # logging.info(str(knowledge))
    else:
        # logging.info('产量/销量: ' + str(new_table))
        knowledge_list = []
        new_table = new_table[1:]
        for item in new_table:
            item_dict = {"主要产品": item[0],
                         "产能": None,
                         "产量": item[1],
                         "销量": item[2],
                         "产能利用率": None,
                         "产销率": item[3]}
            knowledge_list.append(item_dict)
        # logging.info(str(knowledge_list))
        total_page = []
        total_page.extend(new_text_page_list)
        total_page.extend(new_table_page_list)
        total_page = utils.remove_duplicate_item(total_page)
        if len(new_text_list) > 0:
            evidence_text = '\n'.join(new_text_list)
        else:
            evidence_text = ''
        knowledge = {"type": "公司主要产品产能产销情况",
                     "table": [{"name": "公司主要产品产能产销情况",
                                "value": knowledge_list,
                                "evidence_page_number": total_page}],
                     "text": evidence_text
                     }
    return knowledge


def delete_word_in_brackets(text):
    text = re.sub(r'^（*）', '', text)  # 替换（）
    text = re.sub(r'^\(*\)', '', text)  # 替换()
    return text
