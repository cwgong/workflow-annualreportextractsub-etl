# -*- coding: UTF-8 -*-
# 传媒 著作权
# 未完成


def extract():
    knowledge = {"type": "公司著作权期末余额(传媒)",
                 "table": [{"name": "著作权期末余额",
                            "value": None,
                            "evidence_page_number": [0]}]}
    return knowledge


# def extract(text_list, text_page_list, table_list, table_page_list):
#     result = {"著作权期末余额": None}
#
#     explain = {"子标题": None,
#                "关键词": None}
#
#     unit_rgx = "单位：(.*?)元"
#
#     slot_keywods = ['著作权', '版权', '著作']
#     # 新签合同
#     index = None
#     slot_keywod = None
#     for i in range(len(text_list)):
#         p = text_list[i]
#         if '无形资产情况' in p:
#             # print(p)
#             index = i
#
#         if index is not None:
#             if i < index + 15:
#                 for k in slot_keywods:
#                     if k in p:
#                         slot_keywod = k
#                         print(p)
#                         print('slot_keywod: ', slot_keywod)
#                         explain["子标题"] = '无形资产情况'
#                         explain["关键词"] = slot_keywod
#                         break
#
#     if index is not None and slot_keywod is not None:
#         result["著作权期末余额"] = 1
#
#         for table in table_list:
#             ta = 0
#             for row in table:
#                 for cell in row:
#                     if cell is not None:
#                         cell = ''.join([x for x in cell if len(x.strip()) > 0])
#                         if slot_keywod in cell:
#                             ta += 1
#                             break
#             if ta != 0:
#                 # print(table)
#                 print('=============')
#
#     return explain

