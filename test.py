# -*- coding: UTF-8 -*-

# 简单测试接口

import requests
import json
import hashlib

save_es_text_url = "http://index-knowledge-service:31001/knowledge"
save_mongo_texts_url = "http://kb-doc-service:31001/knowledge/candidate"
query_code_id_url = "http://kb-doc-service:31001/dict/search/synonym?dictTypeId=11"

mongo_pdf_url = 'http://datacenter-doc-service:31001/notice?cp=1&page=true&ps=2&parseStatus=1&infoTypes=01030101,01030140'


def post(url, data):
    response = requests.post(url, data=json.dumps(data))
    response = response.json()
    print(response)
    data_list = response.get("data")
    return data_list


def get(url):
    print(url)
    response = requests.get(url)
    response = response.json()
    # print(response)
    data_list = response.get("data")
    return data_list


def get_entity_id(stock_name):
    url = query_code_id_url + "&name=" + stock_name
    result_list = get(url)
    result = result_list[0]
    entity_id = result.get("dictId")
    return entity_id


# {"text_id": 1206124772,
# "sec_code": "002076",
# "mar_type": "sz",
# "sec_name": "雪 莱 特",
# "pub_date": 1556294400000,
# "ann_title": "雪 莱 特：2018年年度报告",
# "info_type": "01010503||010112||010114||01030101",
# "ann_url": "http://static.cninfo.com.cn/finalpage/2019-04-27/1206124772.PDF",
# "INDU_SW3": "LED",
# "INDU_SW2": "光学光电子",
# "INDU_SW1": "电子",
# "INDU_HC1": "制造、流通、综合类",
# "INDU_HC2": "制造、流通、综合类"}

def save_es_mongo_text():
    data = {}
    entity_id = get_entity_id("雪莱特")
    data["entityLeftId"] = entity_id
    data["publishAt"] = 1556294400000
    data["title"] = "雪 莱 特：2018年年度报告"
    data["textUrl"] = "http://static.cninfo.com.cn/finalpage/2019-04-27/1206124772.PDF"
    data["evidenceId"] = "1206124772"
    data["knowledgeType"] = "增值税率"
    data["text"] = "增值税\n纳税依据:动产租赁服务，销售不动产，转让土地\n税率:17%、、16%、6%；11%、10%"
    data["entityLeftTypeId"] = "11"
    data["dataSource"] = "年报"
    data["descriptionMode"] = "文字"
    data["kbSource"] = "知识抽取"
    data["kbType"] = "0"
    data["pages"] = ["159"]

    _id = "增值税率" + entity_id + "1206124772"
    _id = hashlib.md5(_id.encode('utf8')).hexdigest().replace('-', '')  # 32位
    data["id"] = _id

    print(data)
    result1 = post(save_es_text_url, [data])
    print(result1)

    mongo_data = {}
    mongo_data["entityLeftId"] = entity_id
    mongo_data["id"] = _id
    mongo_data["knowledgeType"] = "增值税率"
    mongo_data["text"] = "增值税\n纳税依据:动产租赁服务，销售不动产，转让土地\n税率:17%、、16%、6%；11%、10%"
    mongo_data["textCandidate"] = ["增值税\n纳税依据:动产租赁服务，销售不动产，转让土地\n税率:17%、、16%、6%；11%、10%"]

    print(mongo_data)
    result2 = post(save_mongo_texts_url, [mongo_data])
    print(result2)


if __name__ == '__main__':
    save_es_mongo_text()

