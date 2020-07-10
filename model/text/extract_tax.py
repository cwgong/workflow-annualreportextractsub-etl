# -*- coding: UTF-8 -*-

# 1.增值税率 vat
# 2.税收优惠 tax free

# 包装为List<Map<String, Object>>形式

import model.utils as utils


def extract_tax(text_list, text_page_list):
    print('extract_tax')
    tax_off_list = []
    tax_off_page_set = set()
    tax_off_page_list = []
    need_add = False
    tax_index = 0
    dot = ''

    for i in range(len(text_list)):
        para = text_list[i]
        page = text_page_list[i]

        if para.endswith('税收优惠') and '%' not in para and len(tax_off_list) == 0:
            number_list = utils.extract_number(para)
            if len(number_list) == 0:
                continue
            tax_index = int(number_list[0])
            number_index = para.index(number_list[0])
            # print(tax_index)
            dot = para[(number_index + 1):(number_index + 2)]
            # print(dot)
            need_add = True
            # print(para)
            continue

        if "√适用" in para:
            continue

        if tax_index != 0 and para.startswith(str(tax_index + 1) + dot):
            # print(para)
            # need_add = False
            break

        if '风险' in para:
            need_add = False

        if need_add:
            para = utils.delete_half_sentence(para, '根据')
            para = utils.delete_index(para)
            # para = delete_page_number(para)

            tax_off_list.append(para)
            tax_off_page_set.add(page)  # 用于 知识 整体，需要去重
            tax_off_page_list.append(page)  # 用于 候选集 个体，必须一对一

    if len(tax_off_list) == 0:
        return None

    candidate_list = []
    for i in range(len(tax_off_list)):
        candidate = {"text": tax_off_list[i],
                     "textPage": tax_off_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    # 税收优惠是多段落的，默认全部都是知识
    knowledge = {"type": "公司税收优惠",
                 "text": '\n'.join(tax_off_list),
                 "candidate": candidate_list,
                 "pages": list(tax_off_page_set)}

    return knowledge


# 仅当从json中抽取增值税为空时，从文本中抽取
def extract_vat(text_list, text_page_list, table_list, table_page_list):
    # 先从表格抽取
    vat_list, vat_page_list = extract_vat_table(table_list, table_page_list)
    if len(vat_list) == 0:
        # 再从文本中直接抽取
        vat_list, vat_page_list = extract_vat_text(text_list, text_page_list)

    if len(vat_list) == 0:
        return None

    candidate_list = []
    for i in range(len(vat_list)):
        candidate = {"text": vat_list[i],
                     "textPage": vat_page_list[i],
                     "isKnowledge": True}
        candidate_list.append(candidate)

    knowledge = {"type": "公司增值税率",
                 "text": '\n'.join(vat_list),
                 "candidate": candidate_list,
                 "pages": vat_page_list}

    return knowledge


def extract_vat_text(text_list, text_page_list):
    vat_list = []
    vat_page_list = []
    need_add = False
    vat_index = 0
    dot = ''

    for i in range(len(text_list)):
        para = text_list[i]

        if para.endswith('增值税') and '%' not in para and len(vat_list) == 0:
            number_list = utils.extract_number(para)
            if len(number_list) == 0:
                continue
            vat_index = int(number_list[0])
            number_index = para.index(number_list[0])
            # print(para)
            # print(vat_index)
            # print(number_index)
            dot = para[(number_index + 1):(number_index + 2)]
            # print(dot)
            need_add = True
            # print(para)
            continue

        if "√适用" in para:
            continue

        if vat_index != 0 and para.startswith(str(vat_index + 1) + dot):
            # print(para)
            need_add = False

        if '风险' in para:
            need_add = False

        if need_add:
            # para = para.replace('注1', '')
            # para = delete_page_number(para)
            vat_list.append(para)
            vat_page_list.append(text_page_list[i])

    return vat_list, vat_page_list


def extract_vat_table(table_list, table_page_list):
    # [["税种", "计税依据", "税率"], ["增值税", "应税收入", "6%、17%"]]
    vat_table_list = []
    vat_table_page_list = []
    for i in range(len(table_list)):
        table = table_list[i]
        table_line1_string = utils.get_table_line(table[0])
        table_line1_string = table_line1_string.replace(' ', '')

        if '税种' in table_line1_string:
            if len(table) == 1:
                table.extend(table_list[i + 1])
            vat_table_list.append(table)
            vat_table_page_list.append(table_page_list[i])

    if len(vat_table_list) == 0:
        return []

    # print(len(vat_table_list))
    # print(vat_table_list)

    vat_result_list = []
    for table in vat_table_list:
        type_index = -1
        rate_index = -1
        reason_index = -1
        title_row = table[0]

        for i in range(len(title_row)):
            item = title_row[i]
            if item is None:
                continue
            item = item.replace('\n', '')
            item = item.replace(' ', '')

            if item == '税种':
                type_index = i
            if item == '税率':
                rate_index = i
            if item == '纳税依据' or item == '计税依据' or item == '计税基础':
                reason_index = i
        # print(type_index, reason_index, rate_index)
        for row in table:
            tax_type = row[type_index]
            if tax_type is None:
                continue
            tax_type = tax_type.replace('\n', '')
            if '增值税' in tax_type:
                tax_rate = row[rate_index]
                if tax_rate is None:
                    continue
                tax_rate = tax_rate.replace('\n', '')

                tax_reason = row[reason_index]
                if tax_reason is None:
                    continue
                tax_reason = tax_reason.replace('\n', '')
                vat_result_list.append(tax_type + '\n纳税依据:' + tax_reason + '\n税率:' + tax_rate)
    # print(vat_result_list)
    return vat_result_list, vat_table_page_list

