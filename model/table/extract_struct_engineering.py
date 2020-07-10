# -*- coding: UTF-8 -*-
# 工程类，结构化数据抽取

import re


def extract(detail_list):
    # all_p = txt.split('\n')

    result = {"竣工项目金额": None,
              "在建项目金额": None,
              "新增项目金额": None}
    page_dict = {"竣工项目金额": None,
                 "在建项目金额": None,
                 "新增项目金额": None}

    unit_rgx = "单位：(.*?)元"
    # 定位子标题
    title_sub_position = None
    title_sub = "报告期内竣工验收的项目情况"
    for i in range(len(detail_list)):
        item = detail_list[i]
        content_type = item.get('type')
        content = item.get('content')
        if content_type == 'text' and title_sub in content:
            title_sub_position = i
            break
    if title_sub_position is not None:
        unit = "元"
        for item in detail_list[title_sub_position: title_sub_position + 10]:
            content = item.get('content')
            content_type = item.get('type')
            if content_type == 'text':
                r = re.match(unit_rgx, content)
            else:
                r = None
                # r = re.match(unit_rgx, str(content))
            if r is not None:
                unit = r.group(1).strip() + '元'

            if content_type == 'table':
                for row in content:
                    if '总金额' in row[0]:
                        amount = row[-1].replace(',', '').replace('，', '') + unit
                        result["竣工项目金额"] = amount
                        page_dict["竣工项目金额"] = item.get('page_num')
                        # page_list.append(item.get('page_num'))
                        break

    # 定位子标题
    title_sub_position = None
    title_sub = "报告期内在建项目情况"
    for i in range(len(detail_list)):
        item = detail_list[i]
        content_type = item.get('type')
        content = item.get('content')
        if title_sub in content and content_type == 'text':
            title_sub_position = i
            break
    if title_sub_position is not None:
        unit = "元"
        for item in detail_list[title_sub_position: title_sub_position + 10]:
            content = item.get('content')
            content_type = item.get('type')
            if content_type == 'text':
                r = re.match(unit_rgx, content)
            else:
                r = None
            if r is not None:
                unit = r.group(1).strip() + '元'

            if content_type == 'table':
                for row in content:
                    if '总金额' in row[0]:
                        amount = row[-1].replace(',', '').replace('，', '') + unit
                        result["在建项目金额"] = amount
                        page_dict["在建项目金额"] = item.get('page_num')
                        # page_list.append(item.get('page_num'))
                        break

    add_amount_rgx = "(.*)新签合同(.*?)([0|1|2|3|4|5|6|7|8|9|亿|百|千|万|,|，|.|（|）|(|)]{1,})元"
    # 新签合同
    for i in range(len(detail_list)):
        item = detail_list[i]
        content_type = item.get('type')
        if content_type == 'table':
            continue
        content = item.get('content')
        p = content.replace("；", "。").replace(";", "。")
        if len(p) < 500:
            for s in p.split("。"):
                if '新签合同' in s and "元" in s:
                    s = ''.join([x for x in s if len(x.strip()) > 0])
                    r = re.match(add_amount_rgx, s)
                    if r is not None:
                        amount = r.group(3) + '元'
                        result["新增项目金额"] = amount
                        page_dict["新增项目金额"] = item.get('page_num')
                        # page_list.append(item.get('page_num'))
                        print(s)
                        print(r)
                        print(r.group(3))
                        break

    value_list = []
    for key in result.keys():
        value = handle_money(result.get(key))
        value_table = {"name": key + '/万元',
                       "value": value,
                       "evidence_page_number": [page_dict.get(key)]}
        value_list.append(value_table)

    knowledge = {"type": "公司工程类项目金额(工程)",
                 "table": value_list}

    return knowledge


def handle_money(text):
    if text is None:
        return None
    if ',' in text:
        text = text.replace(',', '')
    result = None
    if '万亿元' in text:
        number = text[:-3]
        if len(number) == 0:
            return None
        result = round(float(number) * 10000 * 10000, 4)
    elif '亿元' in text:
        number = text[:-2]
        if len(number) == 0:
            return None
        result = round(float(number) * 10000, 4)
    elif '万元' in text:
        number = text[:-2]
        if len(number) == 0:
            return None
        result = round(float(number), 4)
    elif '千元' in text:
        number = text[:-2]
        if len(number) == 0:
            return None
        result = round(float(number) / 10, 4)
    elif '元' in text:
        number = text[:-1]
        if len(number) == 0:
            return None
        result = round(float(number) / 10000, 4)
    return result

