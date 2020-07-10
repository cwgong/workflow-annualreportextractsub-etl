# -*- coding: UTF-8 -*-
# 专利、著作权
'''
[{"name":"拥有专利数量",

"value":"",

"evidence_page_number":[int]},

{"name":"拥有著作权数量",

"value":"",

"evidence_page_number":[int]},

{"name":"拥有专利数量表",

"value":[{"专利类型":"",

"专利数量":""}],

"evidence_page_number":[int]}]
'''

import logging
import model.utils as utils
import re


def extract(text_list, text_page_list):

    # patent_content_list = []
    patent_page_list = []
    # patent_page_set = set()
    text = ''
    model_utility_patent = ''
    design_patent = ''
    invention_patent = ''
    copyright = ''
    patent = ''

    for i in range(len(text_list)):
        # item_type = text_list[i].get('type')
        # content = text_list[i].get('content')
        # page = text_list[i].get('page_num')
        para = text_list[i]
        page = text_page_list[i]
        para = para.strip()

        if not utils.text_valid(para):
            continue
        if is_num_add_content(para):
            model_utility_patent,design_patent,invention_patent,patent,copyright = extract_knowledge(para)  #循环遍历整篇文章，取第一个作为知识存进去
            patent_page_list.append(page)
            text = para
            break

    if patent == '' and copyright == '':
        return None
    if model_utility_patent == '' and design_patent == '' and invention_patent == '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)

        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [],
                  "evidence_page_number": []}]
    elif model_utility_patent == '' and design_patent == '' and invention_patent != '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "发明专利",
                             "专利数量": invention_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent == '' and design_patent != '' and invention_patent == '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "外观专利",
                             "专利数量": design_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent != '' and design_patent == '' and invention_patent == '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "实用新型专利",
                             "专利数量": model_utility_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent != '' and design_patent == '' and invention_patent != '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "发明专利",
                             "专利数量": invention_patent}, {"专利类型": "实用新型专利",
                                                         "专利数量": model_utility_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent != '' and design_patent != '' and invention_patent == '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "实用新型专利",
                             "专利数量": model_utility_patent}, {"专利类型": "外观专利",
                                                                "专利数量": design_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent == '' and design_patent != '' and invention_patent != '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "发明专利",
                             "专利数量": invention_patent},{"专利类型": "外观专利",
                                                             "专利数量": design_patent}],
                  "evidence_page_number": patent_page_list}]
    elif model_utility_patent != '' and design_patent != '' and invention_patent != '':
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "发明专利",
                             "专利数量": invention_patent}, {"专利类型": "实用新型专利",
                                                         "专利数量": model_utility_patent}, {"专利类型": "外观专利",
                                                                                         "专利数量": design_patent}],
                  "evidence_page_number": patent_page_list}]
    else:
        if patent == '':
            patent = None
        elif patent.isdigit() == False:
            patent = None
        else:
            patent = int(patent)

        if copyright == '':
            copyright = None
        elif copyright.isdigit() == False:
            copyright = None
        else:
            copyright = int(copyright)

        if model_utility_patent == '':
            model_utility_patent = None
        elif model_utility_patent.isdigit() == False:
            model_utility_patent = None
        else:
            model_utility_patent = int(model_utility_patent)

        if design_patent == '':
            design_patent = None
        elif design_patent.isdigit() == False:
            design_patent = None
        else:
            design_patent = int(design_patent)

        if invention_patent == '':
            invention_patent = None
        elif invention_patent.isdigit() == False:
            invention_patent = None
        else:
            invention_patent = int(invention_patent)
        table = [{'name': '拥有专利数量',
                  'value': patent,
                  'evidence_page_number': patent_page_list
                  }, {"name": "拥有著作权数量",
                      "value": copyright,
                      "evidence_page_number": patent_page_list},
                 {"name": "拥有专利数量表",
                  "value": [{"专利类型": "发明专利",
                             "专利数量": invention_patent}, {"专利类型": "实用新型专利",
                                                         "专利数量": model_utility_patent}, {"专利类型": "外观专利",
                                                                                         "专利数量": design_patent}],
                  "evidence_page_number": patent_page_list}]
    knowledge = {"type": "公司专利与著作权情况",
                 "table": table,
                "text": text
                 }

    return knowledge


def is_num_add_content(para):
    para = para.replace('[','').replace(']','').replace('【','').replace('】','')
    para = para.replace('项', '').replace('个', '').replace('件', '')
    para = para.strip()
    rgx_1 = re.compile(r'\d+{}'.format("专利"))
    rgx_2 = re.compile(r'{}\d+'.format("专利"))
    rgx_3 = re.compile(r'{}\d+'.format("著作权"))
    rgx_4 = re.compile(r'\d+{}'.format("著作权"))
    rgx_5 = re.compile(r'{}\d+'.format("软件著作权"))
    rgx_6 = re.compile(r'\d+{}'.format("软件著作权"))
    rgx_7 = re.compile(r'\d+{}'.format("实用新型专利"))
    rgx_8 = re.compile(r'{}\d+'.format("实用新型专利"))
    rgx_9 = re.compile(r'\d+{}'.format("外观专利"))
    rgx_10 = re.compile(r'{}\d+'.format("外观专利"))
    rgx_11 = re.compile(r'\d+{}'.format("发明专利"))
    rgx_12 = re.compile(r'{}\d+'.format("发明专利"))

    result_1 = rgx_1.search(para)
    result_2 = rgx_2.search(para)
    result_3 = rgx_3.search(para)
    result_4 = rgx_4.search(para)
    result_5 = rgx_5.search(para)
    result_6 = rgx_6.search(para)
    result_7 = rgx_7.search(para)
    result_8 = rgx_8.search(para)
    result_9 = rgx_9.search(para)
    result_10 = rgx_10.search(para)
    result_11 = rgx_11.search(para)
    result_12 = rgx_12.search(para)

    if result_1 or result_2 or result_3 or result_4 or result_5 or result_6 or result_7 or result_8 or result_9 or result_10 or result_11 or result_12 is not None:
        return True
    else:
        return False


def extract_knowledge(para):
    model_utility_patent = ''
    design_patent = ''
    invention_patent = ''
    copyright = ''
    patent = ''

    para = para.replace('[', '').replace(']', '').replace('【', '').replace('】', '')
    para = para.replace('项', '').replace('个', '').replace('件', '')
    para = para.strip()
    rgx_1 = re.compile(r'(\d+)({})'.format("专利"))
    rgx_2 = re.compile(r'({})(\d+)'.format("专利"))
    rgx_3 = re.compile(r'({})(\d+)'.format("著作权"))
    rgx_4 = re.compile(r'(\d+)({})'.format("著作权"))
    rgx_5 = re.compile(r'({})(\d+)'.format("软件著作权"))
    rgx_6 = re.compile(r'(\d+)({})'.format("软件著作权"))
    rgx_7 = re.compile(r'(\d+)({})'.format("实用新型专利"))
    rgx_8 = re.compile(r'({})(\d+)'.format("实用新型专利"))
    rgx_9 = re.compile(r'(\d+)({})'.format("外观专利"))
    rgx_10 = re.compile(r'({})(\d+)'.format("外观专利"))
    rgx_11 = re.compile(r'(\d+)({})'.format("发明专利"))
    rgx_12 = re.compile(r'({})(\d+)'.format("发明专利"))

    result_1 = rgx_7.search(para)
    if result_1 is None:
        result_1 = rgx_8.search(para)
        if result_1 is not None:
            model_utility_patent = result_1.group(2)
    else:
        model_utility_patent = result_1.group(1)
    if result_1 is not None:
        para = para.replace('实用新型专利','')

    result_2 = rgx_9.search(para)
    if result_2 is None:
        result_2 = rgx_10.search(para)
        if result_2 is not None:
            design_patent = result_2.group(2)
    else:
        design_patent = result_2.group(1)
    if result_2 is not None:
        para = para.replace('外观专利','')

    result_3 = rgx_11.search(para)
    if result_3 is None:
        result_3 = rgx_12.search(para)
        if result_3 is not None:
            invention_patent = result_3.group(2)
    else:
        invention_patent = result_3.group(1)
    if result_3 is not None:
        para.replace('发明专利','')

    result_4 = rgx_1.search(para)
    if result_4 is None:
        result_4 = rgx_2.search(para)
        if result_4 is not None:
            patent = result_4.group(2)
    else:
        patent = result_4.group(1)

    result_5 = rgx_4.search(para)
    if result_5 is None:
        result_5 = rgx_3.search(para)
        if result_5 is not None:
            copyright = result_5.group(2)
        if result_5 is None:
            result_5 = rgx_6.search(para)
            if result_5 is not None:
                copyright = result_5.group(2)
            if result_5 is None:
                result_5 = rgx_5.search(para)
                if result_5 is not None:
                    copyright = result_5.group(1)
    else:
        copyright = result_5.group(1)

    return model_utility_patent,design_patent,invention_patent,patent,copyright

if __name__ == "__main__":
    s = "公司拥有【2651】项实用新型专利 "
    extract_knowledge(s)