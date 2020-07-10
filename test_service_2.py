# -*- coding: UTF-8 -*-

# 运行etl，测试运行情况，检查运行结果

import requests
import json

job_url = 'http://localhost:31001/job/'
scheduler_url = 'http://localhost:31001/scheduler/'
run_url = 'http://localhost:31001/run'

DEBUG_START_AT = '1546272000000'  # 2019-01-01
DEBUG_END_AT = '1584892800000'  # 2020-03-23


def requests_get(url, params):
    response = requests.get(url, params=params)
    # response.encoding = "utf-8"
    print(response.status_code)
    print(response.text)
    return response.text


def add_job_1():
    url = job_url + 'add'
    param = {"timeField": "",
             "startAt": "",
             "endAt": "",
             "knowledgeType": "",
             "jobId": "1",
             "jobName": "dayTask",
             "timeInterval": 86400}
    result = requests_get(url, param)
    # print("1")
    # print(result)


def add_job_2():
    url = job_url + 'add'
    param = {"timeField": "2",
             "jobId": "2",
             "jobName": "22",
             "timeInterval": 5}
    result = requests_get(url, param)
    # print("2")
    # print(result)


def start():
    url = scheduler_url + 'start'
    param = {}
    result = requests_get(url, param)
    print("start")
    print(result)


def stop():
    url = scheduler_url + 'shutdown'
    param = {}
    result = requests_get(url, param)
    print("shutdown")
    print(result)


# [{"job_id": "1", "job_name": "11", "next_run_time": "2020-01-10 17:07:21"},
# {"job_id": "2", "job_name": "22", "next_run_time": "2020-01-10 17:07:23"}]
def query():
    url = job_url + 'query'
    param = {}
    result = requests_get(url, param)
    print("query")
    json_result = json.loads(result)
    print(json_result[0])  # {'job_id': '1', 'job_name': '11', 'next_run_time': '2020-01-14 10:45:56'}


def run(knowledge_type):
    param = {"startAt": DEBUG_START_AT,
             "endAt": DEBUG_END_AT,
             "timeField": "pubAt",
             "knowledgeType": knowledge_type}
    result = requests_get(run_url, param)
    print("run")


if __name__ == "__main__":
    # add_job_1()
    # add_job_2()
    # start()
    # query()
    # stop()
    # run("公司竞争优势")
    run("公司市场排名")
    # print(type('123'))

