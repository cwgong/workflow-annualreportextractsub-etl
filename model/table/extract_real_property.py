# -*- coding: UTF-8 -*-
# 房地产

import model.utils as utils


def extract_lists():
    value_list = []
    value_name = ["在售项目地区分布", "新增土地储备地区分布", "累计土地储备地区分布"]
    for item in value_name:
        value_table = {"name": item,
                       "value": [{"地区": None, "面积（万平方米）": None}],
                       "evidence_page_number": []}
        value_list.append(value_table)

    knowledge = {"type": "公司房地产列表(房地产)",
                 "table": value_list}
    return knowledge


def extract_right_list():
    value_name = ["合同销售金额（万元）", "合同销售面积（万平方米）", "权益比例"]
    value_list = []
    for item in value_name:
        right_table = {"name": item,
                       "value": None,
                       "evidence_page_number": []}
        value_list.append(right_table)

    knowledge = {"type": "公司房地产权益列表(房地产)",
                 "table": value_list}


def extract(table_list, table_page_list):
    merged_table_list, merged_table_page_list = merge_table(table_list, table_page_list)
    selected_table_list, selected_table_page_list = select_table(merged_table_list, merged_table_page_list, '面积')
    develop_result, result_table_page_list = extract_develop(selected_table_list, selected_table_page_list)

    value_list = []
    for key in develop_result.keys():
        value_table = {"name": key,
                       "value": develop_result.get(key),
                       "evidence_page_number": result_table_page_list}
        value_list.append(value_table)

    # 人工抽取的，由运营后台填写
    other_value = ["新增待开发面积（万平方米）", "新增待开发金额（万元）", "累计待开发面积（万平方米）", "累计待开发金额（万元）",
                   "合同销售金额（万元）", "合同销售面积（万平方米）"]
    for item in other_value:
        value_table = {"name": item,
                       "value": None,
                       "evidence_page_number": []}
        value_list.append(value_table)

    knowledge = {"type": "公司房地产指标(房地产)",
                 "table": value_list}

    return knowledge


# 开发情况
# 新开工 累计开工
# 在建
# 竣工 累计竣工
# 面积
def extract_develop(table_list, table_page_list):
    result_table_page_list = []

    total_new_start = 0
    total_add_up_start = 0
    total_completed = 0
    total_add_up_completed = 0
    total_building = 0

    for j in range(len(table_list)):
        table = table_list[j]
        page = table_page_list[j]

        line1 = table[0]
        line1_string = get_table_line(table[0])
        if '开工' not in line1_string:
            continue

        new_start_index = -1
        add_up_start_index = -1
        completed_index = -1
        add_up_completed_index = -1
        building_index = -1

        new_start = 0
        add_up_start = 0
        completed = 0
        add_up_completed = 0
        building = 0

        for i in range(len(line1)):
            item = line1[i]
            if item is None:
                continue
            item = item.replace('\n', '')

            if '开工' in item and '累计开工' not in item and '计划' not in item and '时间' not in item and '竣工' not in item and '预计' not in item:
                new_start_index = i
            if '累计开工' in item:
                add_up_start_index = i
            if ('竣工' in item or '已完工' in item) and '累计竣工' not in item and '计划' not in item and '时间' not in item and '开工' not in item and '预计' not in item and '是否' not in item:
                completed_index = i
            if '累计竣工' in item:
                # print(i)
                add_up_completed_index = i
            if '在建' in item and '面积' in item:
                building_index = i

        last_line = table[-1]
        last_line_string = get_table_line(last_line)

        # print(line1_string)
        # print(last_line_string)
        # print(line1[add_up_completed_index])
        # print(last_line[add_up_completed_index])
        # print(add_up_completed_index)

        if '合计' in last_line_string or '总计' in last_line_string:
            if new_start_index != -1:
                new_start = get_item_number(last_line[new_start_index])
            if add_up_start_index != -1:
                add_up_start = get_item_number(last_line[add_up_start_index])
            if completed_index != -1:
                completed = get_item_number(last_line[completed_index])
            if add_up_completed_index != -1:
                add_up_completed = get_item_number(last_line[add_up_completed_index])
            if building_index != -1:
                building = get_item_number(last_line[building_index])
        else:
            if new_start_index != -1:
                new_start = extract_column_add_on(table, new_start_index)
            if add_up_start_index != -1:
                add_up_start = extract_column_add_on(table, add_up_start_index)
            if completed_index != -1:
                completed = extract_column_add_on(table, completed_index)
            if add_up_completed_index != -1:
                add_up_completed = extract_column_add_on(table, add_up_completed_index)
            if building_index != -1:
                building = extract_column_add_on(table, building_index)

        result_table_page_list.append(page)
        total_new_start += new_start
        total_add_up_start += add_up_start
        total_completed += completed
        total_add_up_completed += add_up_completed
        total_building += building
        # result_table_list.append(line1_string)
        # print(new_start, add_up_start, completed, add_up_completed, building)
    # result_table_list.append('%f\t%f\t%f\t%f\t%f' % (new_start, add_up_start, completed, add_up_completed, building))
    result_table_dict = {"新开工面积（万平方米）": total_new_start,
                         "累计开工面积（万平方米）": total_add_up_start,
                         "竣工面积（万平方米）": total_completed,
                         "累计竣工面积（万平方米）": total_add_up_completed,
                         "在建面积（万平方米）": total_building}

    return result_table_dict, result_table_page_list


def merge_table(table_list, table_page_list):
    merged_table_list = []
    merged_table_page_list = []

    last_table_line1 = ''
    last_line_item_count = 0
    for i in range(len(table_list)):
        table = table_list[i]
        page = table_page_list[i]

        table_line1 = get_table_line(table[0])
        if len(merged_table_list) == 0:
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])
            continue

        if last_line_item_count != len(table[0]):
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])
            continue

        not_title = utils.contain_number(table_line1) and '年' not in table_line1
        if not_title:
            last_table = merged_table_list[-1]
            last_table.extend(table)
        elif table_line1 == last_table_line1:
            last_table = merged_table_list[-1]
            last_table.extend(table[1:])
        else:
            merged_table_list.append(table)
            merged_table_page_list.append(page)
            last_table_line1 = table_line1
            last_line_item_count = len(table[0])

    return merged_table_list, merged_table_page_list


def select_table(table_list, table_page_list, keyword):
    selected_table = []
    selected_table_page = []

    for i in range(len(table_list)):
        table = table_list[i]
        page = table_page_list[i]

        line1 = ''
        for row in table[0]:
            if row is not None:
                line1 += row + ' '
        line1 = line1.replace('\n', '')

        if keyword in line1:
            selected_table.append(table)
            selected_table_page.append(page)
    return selected_table, selected_table_page


def get_table_line(row):
    row_string = ''
    for item in row:
        if item is not None:
            row_string += item + ' '
    row_string = row_string.replace('\n', '')
    return row_string


def get_item_number(item):
    if item is None:
        return 0
    if item == '/' or item == '-' or len(item) == 0 or item == "—":
        return 0

    item = item.replace(',', '')
    item = item.strip()
    if not item.isnumeric():
        item = get_number_sequence(item)
        if len(item) == 0:
            return 0
    return float(item)


def get_number_sequence(text):
    number_string = ''
    for item in text:
        if item.isdigit():
            number_string += item
        if item == '.':
            number_string += item
        if item == '．':
            number_string += '.'
    return number_string


def extract_column_add_on(table, index):
    column = extract_column(table, index)
    if len(column) == 0:
        print('error')
        return 0

    add_on = 0.0
    for i in range(len(column)):
        if i == 0:
            continue
        item = column[i]
        add_on += get_item_number(item)
    return add_on


def extract_column(table, index):
    column_list = []
    for line in table:
        item = line[index]
        if item is None:
            continue
        item = item.replace('\n', '')
        column_list.append(item)
    return column_list
