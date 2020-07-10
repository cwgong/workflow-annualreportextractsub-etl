# -*- coding: utf-8 -*-
# 公司前五大客户关联情况

import re

# 抽取 slot 对应的 value（数值） 形式
def extract_value_by_slot(pdf_json, slot, feas, rgx, fea_idx):
    value = None
    evidence = None
    page_num = None

    for obj in pdf_json:
        if obj['type'] == 'text':
            # 去空格
            p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
            if len(p) > 0:
                # 判断是否满足 feas
                c = 0
                p_ = p
                for fea in feas:
                    if fea in p_:
                        idx = p_.find(fea)
                        p_ = p_[idx+1:]
                        c += 1
                # 根据 rgx 查找 value
                if c == len(feas):
                    evidence = p
                    p2 = p
                    for i in range(len(feas)):
                        if i < fea_idx:
                            idx = p2.find(feas[i])
                            p2 = p2[idx + 1:]
                    # 匹配
                    r = re.match(rgx, p2)
                    if r is not None:
                        value = r.group(2)
                        page_num = obj['page_num']

    if value is not None:
        value = float(value) * (0.01)
        value = round(value, 4)

    return value, evidence, page_num


def extract(detail):

    knowledge = None

    pdf_json = detail
    slot = '关联方销售额占比'
    feas = ['前', '名', '关联方销售额', '%']
    rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9|.]{1,})(%)"
    fea_idx = 3
    value, evidence, page_num = extract_value_by_slot(pdf_json, slot, feas, rgx, fea_idx)

    if value is not None:

        knowledge = {"type": "公司前五大客户关联情况",
                     "table": [{"name": "关联方销售额占比",
                                "value": value,
                                "evidence_page_number": [page_num]}],
                     "text": '\n'.join([evidence])
                     }
        print(knowledge)
    return knowledge
