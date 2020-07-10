# -*- coding: UTF-8 -*-

import re
import json
import requests


# 删除序号
def delete_index(text):
    text = re.sub(r'^（[0-9]{1,2}）', '', text)  # 替换（1）
    text = re.sub(r'^[0-9]{1,2}）', '', text)  # 替换1）
    text = re.sub(r'^[0-9]{1,2}、', '', text)  # 替换1、
    text = re.sub(r'^[0-9]{1,2}\.', '', text)  # 替换1.
    text = re.sub(r'^[0-9]{1,2}．', '', text)  # 替换1．
    text = re.sub(r'^\([0-9]{1,2}\)', '', text)  # 替换(1)
    text = re.sub(r'^（[一二三四五六七八九十]+）', '', text)  # 替换（一）
    text = re.sub(r'^[一二三四五六七八九十]+、', '', text)  # 替换一、
    text = re.sub(r'^\([一二三四五六七八九十]+\)', '', text)  # 替换(一)
    text = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+', '', text)  # 替换①
    return text


# 判断是否为标题
def is_title(text):
    if '。' in text:
        return -1
    if text.endswith('；'):
        return -1

    rule_list = [r'^（[0-9]{1,2}）',  # （1）
                 r'^[0-9]{1,2}）',  # 1）
                 r'^[0-9]{1,2}、',  # 1、
                 r'^[0-9]{1,2}\.',  # 1.
                 r'^[0-9]{1,2}．',  # 1．
                 r'^\([0-9]{1,2}\)',  # (1)
                 r'^（[一二三四五六七八九十]+）',  # （一）
                 r'^[一二三四五六七八九十]+、',  # 一、
                 r'^\([一二三四五六七八九十]+\)',  # (一)
                 r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+']  # ①

    text = text.strip('\t').strip()
    for i in range(len(rule_list)):
        pattern = re.compile(rule_list[i])
        result = pattern.findall(text)
        if len(result) != 0:
            return i
    return -1


# 标题等级
def title_level(text):
    text = text.strip()
    if '。' in text:
        return -1
    if text.endswith('；'):
        return -1

    level1_list = [
        r'^[一二三四五六七八九十]+、',  # 一、
    ]

    level2_list = [
        r'^（[一二三四五六七八九十]+）',  # （一）
        r'^\([一二三四五六七八九十]+\)',  # (一)
    ]

    level3_list = [
        r'^[0-9]{1,2}、',  # 1、
        r'^[0-9]{1,2}\.',  # 1.
        r'^[0-9]{1,2}．',  # 1．
    ]

    level4_list = [
        r'^（[0-9]{1,2}）',  # （1）
        r'^[0-9]{1,2}）',  # 1）
    ]

    level5_list = [
        r'^[①②③④⑤⑥⑦⑧⑨⑩⑪]+']  # ①

    levels = [level5_list, level4_list, level3_list, level2_list, level1_list]

    text = text.strip('\t').strip()
    for i in range(len(levels)):
        rule_list = levels[i]
        for j in range(len(rule_list)):
            pattern = re.compile(rule_list[j])
            result = pattern.findall(text)
            if len(result) != 0:
                return i
    return -1


def text_valid(para):
    para = para.strip()
    if not para:
        return False
    if "√适用" in para:
        return False
    if '具体内容详见' in para:
        return False
    if para.startswith('详见本报告'):
        return False
    return True


def extract_number(text):
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(text)
    return result


def contain_number(text):
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(text)
    return len(result) != 0


def contain_all_number(text):
    pattern = re.compile(r'\d+')  # 查找数字
    result1 = pattern.findall(text)
    pattern = re.compile(r'[一二三四五六七八九十]+')
    result2 = pattern.findall(text)
    pattern = re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩⑪]+')
    result3 = pattern.findall(text)
    return len(result1) != 0 or len(result2) != 0 or len(result3) != 0


def remove_duplicate_item(item_list):
    new_list = []
    for i in range(len(item_list)):
        item = item_list[i]
        if item in new_list:
            continue
        else:
            new_list.append(item)
    return new_list


# 删除key_word所在句，逗号分隔
def delete_half_sentence(text, key_word):
    sentence_list = text.split('，')
    new_sentence_list = []
    for sentence in sentence_list:
        if key_word in sentence:
            continue
        new_sentence_list.append(sentence)
    return_text = '，'.join(new_sentence_list)
    return return_text


# 删除key_word后所有，逗号分隔
def delete_suffix(text, key_word):
    sentence_list = text.split('，')
    new_sentence_list = []
    for sentence in sentence_list:
        if key_word in sentence:
            break
        new_sentence_list.append(sentence)
    return_text = '，'.join(new_sentence_list)
    return return_text


def get_table_line(row):
    row_string = ''
    for item in row:
        if item is not None:
            row_string += item + ' '
    row_string = row_string.replace('\n', '')
    return row_string


def split_sentence(sen):
    nlp_url = 'http://hanlp-nlp-service:31001/hanlp/segment/segment'
    try:
        cut_sen = dict()
        cut_sen['content'] = sen
        cut_sen['customDicEnable'] = True
        data = json.dumps(cut_sen).encode("UTF-8")
        cut_response = requests.post(nlp_url, data=data, headers={'Connection': 'close'})
        cut_response_json = cut_response.json()
        return cut_response_json['data']
    except Exception as e:
        print("Exception: {}".format(e))
        print("hanlp-nlp-service error")
        print("sentence: {}".format(sen))
        return []


def get_striped(string):
    return ''.join([x for x in string if len(x.strip()) > 0])


def has_unit(text):
    return '吨' in text or 'kk' in text or 'KK' in text or '辆' in text or '件' in text or '支' in text \
           or '盒' in text or 'kg' in text or '片' in text or '台' in text or '千瓦时' in text or '只' in text \
           or '升' in text or '瓦' in text or '公里' in text or '瓶' in text or '立方米' in text or '公斤' in text \
           or '毫升' in text or '份' in text or '艘' in text or '套' in text or '个' in text or '粒' in text or '米' in text \
           or '平方米' in text or '英尺' in text or '条' in text or '册' in text or 'GW' in text


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
