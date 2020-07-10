# -*- coding: utf-8 -*-
# 公司资产权利受限情况

import re
import collections

# http://static.cninfo.com.cn/finalpage/2019-04-30/1206164100.PDF
# 34 页，表格右侧缺竖线，是否能识别
def extract_properties_value(pdf_json):

    # 首先定位 "小标题" 或 根据 "特征" 锁定 "目标区域"
    sub_titles = ['截至报告期末的资产权利受限情况', '截至报告期末主要资产受限情况', '截至报告期末主要资产受限情况']
    sub_title_feas = ['资产', '受限', '情况']

    properties = ['货币资金', '以公允价值计量且变动计入当期损益的金融资产', '衍生金融资产', '应收票据', '应收账款',
                  '应收帐款', '预付款项', '其他应收款', '存货', '持有持售资产', '一年内到期的非流动资产',
                  '其他流动资产', '可供出售金融资产', '持有至到期投资', '长期应收款', '长期股权投资', '投资性房地产',
                  '固定资产', '在建工程', '生产性生物投资', '油气资产', '无形资产', '开发支出', '商誉', '长期待摊费用',
                  '递延所得税资产', '其他非流动资产']
    properties = sorted(properties, key=lambda x: len(x), reverse=True)

    # 定位子标题位置
    sub_title_flag = None
    sub_title_idx = None
    for i in range(len(pdf_json)):
        obj = pdf_json[i]
        if obj['type'] == 'text':
            # 去空格
            p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
            if len(p) > 0:
                # 判断是否满足 feas
                c = 0
                p_ = p
                for fea in sub_title_feas:
                    if fea in p_:
                        idx = p_.find(fea)
                        p_ = p_[idx + 1:]
                        c += 1
                # 定位子标题，限制子标题长度
                if c == len(sub_title_feas) and len(p) < 20:
                    #print(p)
                    #print('-------------------')
                    sub_title_flag = p
                    sub_title_idx = i
                    break

    result = collections.OrderedDict()
    page_nums = []
    evidence_texts = []
    if sub_title_idx is not None:
        # 选取下文 10 段内
        for j in range(sub_title_idx + 1, sub_title_idx + 10):
            obj = pdf_json[j]
            if obj['type'] == 'text':
                # 去空格
                p = ''.join([x for x in obj['content'] if len(x.strip()) > 0])
                #print(p)
                # 观测每段最多存在一个 property
                amount_rgx = "(.*?)([0|1|2|3|4|5|6|7|8|9|.|,]{4,})(.*)"
                r = re.match(amount_rgx, p)
                if r is not None:
                    string = r.group(1)
                    property = None
                    for pro in properties:
                        if pro in string:
                            property = pro
                            break
                    if property is not None:
                        amount = r.group(2).replace(',', '')
                        if '万元' == r.group(3)[0:2]:
                            try:
                                amount = round(float(amount)*10000, 2)
                            except:
                                print('error: ', p)
                                continue
                        else:
                            try:
                                amount = round(float(amount), 2)
                            except:
                                print('error: ', p)
                                continue
                        if property not in result:
                            result[property] = amount
                            page_num = obj['page_num']
                            if page_num not in page_nums:
                                page_nums.append(page_num)
                            if p not in evidence_texts:
                                evidence_texts.append(p)

    #print('===========================')

    if len(result) > 0:
        #print(result)
        #print(page_nums)
        #print('~~~~~~~~~~~~~~~~~~~~~~~')
        return result, page_nums, evidence_texts
    else:
        return None, page_nums, evidence_texts


def extract(detail):
    knowledge = None
    pdf_json = detail
    result, page_nums, evidence_texts = extract_properties_value(pdf_json)
    if result is not None:

        lines = []
        for key, v in result.items():
            line = collections.OrderedDict()
            line['项目'] = key
            line['期末账面价值'] = v
            line['受限原因'] = ''
            lines.append(line)

        knowledge = {"type": "公司资产权利受限情况",
                     "table": [{"name": "权利受限情况",
                                "value": lines,
                                "evidence_page_number": page_nums}],
                     "text": '\n'.join(evidence_texts)
                     }
        print(knowledge)
    return knowledge




