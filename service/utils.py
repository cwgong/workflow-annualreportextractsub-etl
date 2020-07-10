# -*- coding: UTF-8 -*-
import requests
import json
import hashlib
import logging
import datetime
import time
import get_data as db

mongo_pdf_url = 'http://datacenter-doc-service:31001/notice?page=true&parseStatus=1&infoTypes=01030101,01030140'
indu_url = 'http://semantic-datacenter-service:31001/hc/indus/'
entity_url = 'http://kb-doc-service:31001/dict/search/synonym?dictTypeId=9&name='
es_save_text_url = 'http://index-kb-service:31001/knowledge'
mongo_save_table_url = 'http://structured-knowledge-service:31001/knowledge/structured/python/save'
mongo_save_candidate_url = "http://kb-doc-service:31001/knowledge/candidate"


def request_pdf_always(start_at, end_at, time_field, extract_method):
    logging.info('开始查询数据')
    if type(start_at) == str and len(start_at) == 0:
        start_at = int(time.time()) * 1000 - 24 * 3600 * 1000
    if type(end_at) == str and len(end_at) == 0:
        end_at = start_at + 24 * 3600 * 1000
    if len(time_field) == 0:
        time_field = 'updateAt'

    data = db.get_extra_news_info(start_at, end_at, time_field)
    data_list = []
    count = 0
    begin = datetime.datetime.now()
    for x in data:
        data_list.append(x)
        count += 1
        if len(data_list) >= 10:
            end = datetime.datetime.now()
            cost_time = end - begin
            logging.info('download cost time: ' + str(cost_time))
            handle_data_list(data_list, extract_method)
            data_list.clear()
            begin = datetime.datetime.now()
            count = 0
    if len(data_list) > 0:
        end = datetime.datetime.now()
        cost_time = end - begin
        logging.info('download cost time: ' + str(cost_time))
        handle_data_list(data_list, extract_method)
    logging.info('加载数据完毕')


def handle_data_list(data_list, extract_method):
    # print(len(data_list))
    logging.info("get annual report count: %d" % len(data_list))
    if len(data_list) == 0:
        logging.info("无年报数据可抽取")
        return

    # print('start processing')
    for i in range(len(data_list)):
        item = data_list[i]
        title = item.get('annTitle')
        # print(i)
        parse_status = item.get('parseStatus')
        if parse_status != '1':
            logging.info('parse not finish: ' + item.get('secCode') + ' title: ' + title)
            continue

        if '摘要' in title or '已取消' in title:
            logging.info('摘要 or 已取消, continue')
            continue

        mar_type = item.get('marType')
        sec_code = item.get('secCode')

        if len(mar_type) == 0 or len(sec_code) == 0:
            logging.info('mar type or sec code is empty')
            continue
        induhc2 = request_induhc2(mar_type, sec_code)
        if len(induhc2) == 0:
            logging.info('cannot get induhc2: ' + mar_type + sec_code)  # B股
            continue

        sec_name = item.get('secName')
        if ' ' in sec_name:
            sec_name = sec_name.replace(' ', '')
        if len(sec_name) == 0:
            logging.info('sec mane is empty')
        entity_id = request_entity_id(sec_name)
        if len(entity_id) == 0:
            logging.info('cannot get entity_id, sec_name: ' + sec_name)
            continue

        detail = item.get('detail')
        # 1.抽取
        # logging.info('extracting...' + title + item.get('annUrl'))
        text_knowledges, table_knowledges = extract_method(detail=detail, induhc2=induhc2, sec_name=sec_name, title=title)

        if len(text_knowledges) == 0 and len(table_knowledges) == 0:
            # logging.info('no extract result, id:' + str(item.get('id') + ',name:' + sec_name + ',code:' + sec_code))
            continue
        # 2.包装、保存
        # print('package and save...')
        if len(text_knowledges) > 0:
            text_param_list, text_candidate_param_list = package_text_knowledge(item, entity_id, text_knowledges)
            text_save_result = save_text(text_param_list)
            candidate_save_result = save_text_candidate(text_candidate_param_list)
            logging.info('save text true %d, save candidate code %d' % (text_save_result, candidate_save_result))
            # logging.info(text_param_list)
            # logging.info(text_candidate_param_list)
        if len(table_knowledges) > 0:
            table_param_list = package_table_knowledge(item, entity_id, table_knowledges)
            table_save_result = save_table(table_param_list)
            logging.info('save table true %d' % table_save_result)
            # logging.info(table_param_list)


def request_induhc2(marType, secCode):
    url = indu_url + marType + '/' + secCode
    response = requests.get(url)
    response = response.json()
    data_dict = response.get('data')
    if data_dict is None:
        return ''
    induHc2 = data_dict.get('induHc2')
    return induHc2


def request_entity_id(sec_name):
    b_name = strQ2B(sec_name)
    url = entity_url + b_name
    response = requests.get(url)
    response = response.json()
    data = response.get('data')
    if data is None:
        # logging.info('cannot get entity id name: ' + sec_name)
        return ''
    data_list = data.get('list')
    if len(data_list) == 0:
        return ''
    result = data_list[0]
    entity_id = result.get("dictId")
    return entity_id


def save_text(param_list):
    url = es_save_text_url
    response = requests.post(url, data=json.dumps(param_list))
    response = response.json()
    # print(response)
    data = response.get("data")
    return data


def save_text_candidate(param_list):
    url = mongo_save_candidate_url
    response = requests.post(url, data=json.dumps(param_list))
    response = response.json()
    # print(response)
    message = response.get("message")
    code = message.get('code')
    # logging.info('mongo save response code %d' % code)
    return code


def save_table(param_list):
    url = mongo_save_table_url
    response = requests.post(url, data=json.dumps(param_list))
    response = response.json()
    # print(response)
    data = response.get("data")
    return data


def package_text_knowledge(pdf_item, entity_id, text_knowledges):
    evidence_id = str(pdf_item.get('textid'))
    param = {'entityLeftId': entity_id,
             'entityLeftTypeId': '9',
             'publishAt': pdf_item.get('pubDateAt'),
             'title': pdf_item.get('annTitle'),
             'textUrl': pdf_item.get('annUrl'),
             'evidenceId': evidence_id,
             'dataSource': pdf_item.get('annGroup'),
             'descriptionMode': '文字',
             'kbSource': '知识抽取',
             'kbType': '0'}
    candidate_param = {'entityId': entity_id}
    param_list = []
    candidate_param_list = []
    for knowledge in text_knowledges:
        new_param = param.copy()
        knowledge_type = knowledge.get('type')
        text = knowledge.get('text')
        if len(text) == 0:
            print('knowledge length = 0')
            print(knowledge)
            continue
        page = knowledge.get('page')
        new_param['knowledgeType'] = knowledge_type
        new_param['text'] = text
        new_param['pages'] = page
        _id = knowledge_type + entity_id + evidence_id
        _id = hashlib.md5(_id.encode('utf8')).hexdigest().replace('-', '')  # 32位
        new_param["id"] = _id
        param_list.append(new_param)

        _id_candidate = knowledge_type + entity_id + evidence_id + 'candidate'
        _id_candidate = hashlib.md5(_id_candidate.encode('utf8')).hexdigest().replace('-', '')  # 32位
        new_candidate_param = candidate_param.copy()
        new_candidate_param['knowledgeType'] = knowledge_type
        new_candidate_param['knowledgeId'] = _id
        new_candidate_param['text'] = text
        new_candidate_param['textCandidate'] = knowledge.get('candidate')
        new_candidate_param["id"] = _id_candidate
        candidate_param_list.append(new_candidate_param)

    return param_list, candidate_param_list


def package_table_knowledge(pdf_item, entity_id, table_knowledges):
    evidence_id = str(pdf_item.get('textid'))
    param = {'entityId': entity_id,
             'entityType': '9',
             'evidencePublishDate': pdf_item.get('pubDateAt'),
             'evidenceTitle': pdf_item.get('annTitle'),
             'evidenceUrl': pdf_item.get('annUrl'),
             'evidenceId': evidence_id,
             'evidenceType': pdf_item.get('annGroup'),
             'knowledgeSourceType': '机器抽取'}
    param_list = []
    for knowledge in table_knowledges:
        new_param = param.copy()
        knowledge_type = knowledge.get('type')
        table = knowledge.get('table')
        new_param['knowledgeType'] = knowledge_type
        new_param['knowledge'] = table
        # 针对只能抽取段落的结构化数据，需要运营手动填写到表哥中
        if 'text' in knowledge.keys():
            new_param['evidenceText'] = knowledge.get('text')

        _id = knowledge_type + entity_id + evidence_id
        _id = hashlib.md5(_id.encode('utf8')).hexdigest().replace('-', '')  # 32位
        new_param["id"] = _id
        param_list.append(new_param)
    return param_list


def parse_detail(detail):
    text_list = []
    text_page_list = []
    table_list = []
    table_page_list = []
    for item in detail:
        page_num = item.get('page_num')
        item_type = item.get('type')
        content = item.get('content')
        if item_type == 'text':
            text_list.append(content)
            text_page_list.append(page_num)
        elif item_type == 'table':
            table_list.append(content)
            table_page_list.append(page_num)
    return text_list, text_page_list, table_list, table_page_list


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:                              # 全角空格直接转换
            inside_code = 32
        elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring