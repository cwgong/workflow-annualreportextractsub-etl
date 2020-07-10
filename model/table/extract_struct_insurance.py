# -*- coding: UTF-8 -*-
# 保险类 13、25个月续保率


def extract(text_list, text_page_list):
    result = {"13个月保单继续率": None,
              "25个月保单继续率": None}
    page_dict = {"13个月保单继续率": None,
                 "25个月保单继续率": None}
    continue_rate_list = []
    continue_rate_page_list = []

    # unit_rgx = "单位：(.*?)元"

    # add_amount_rgx = "(.*)新签合同(.*?)([0|1|2|3|4|5|6|7|8|9|亿|百|千|万|,|，|.|（|）|(|)]{1,})元"
    subs = ['13个月', '25个月']
    keywords = ['继续率']
    # 新签合同
    # index = None
    # slot_keywod = None
    for i in range(len(text_list)):
        p = text_list[i]
        if len(p) > 1000:
            continue

        sub_c = 0
        for sub in subs:
            if sub in p:
                sub_c = 1

        key_c = 0
        for keyword in keywords:
            if keyword in p:
                key_c = 1

        if sub_c + key_c == 2:
            continue_rate_list.append(p)
            continue_rate_page_list.append(text_page_list[i])

    value_list = [{"name": "13个月保单继续率（%）",
                   "value": None,
                   "evidence_page_number": continue_rate_page_list},
                  {"name": "25个月保单继续率（%）",
                   "value": None,
                   "evidence_page_number": continue_rate_page_list},
                  {"name": "剩余边际余额（亿元）",
                   "value": None,
                   "evidence_page_number": continue_rate_page_list}
                  ]

    knowledge = {"type": "公司保险类续保率(保险)",
                 "text": '\n'.join(continue_rate_list),
                 "table": value_list}
    return knowledge

