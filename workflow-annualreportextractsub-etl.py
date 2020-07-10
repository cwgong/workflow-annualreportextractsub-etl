# -*- coding: UTF-8 -*-

# service通用配置，调用extract_service.py，使用TornadoScheduler调度任务

import sys

sys.path.append('./service')

# 自定义版本
from _version import __version__

# python
import io
import json

# tornado
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import apscheduler.events
from apscheduler.schedulers.background import BackgroundScheduler

# 进程间共享一个job store会出错，需要存在不同的表里，即每次都在db中新建一个table
# sql_alchemy_job_store = SQLAlchemyJobStore(url='mysql://analyse:GemanticYes!@10.0.0.20:3306/apscheduler',
#                                            tablename='annual_report_extract_jobs')
# job_stores = {'mysql': sql_alchemy_job_store}
# sched = TornadoScheduler(jobstores=job_stores)
# sched = TornadoScheduler()
back_sched = BackgroundScheduler()

import service.text.extract_tax_service as extract_tax_service
import service.text.extract_branch_service as extract_branch_service
import service.text.extract_copyright_service as extract_copyright_service
import service.text.extract_innovate_service as extract_innovate_service
import service.text.extract_main_channel_service as extract_main_channel_service
import service.text.extract_main_production_service as extract_main_production_service
import service.text.extract_market_hold_service as extract_market_hold_service
import service.text.extract_market_scale_service as extract_market_scale_service
import service.text.extract_property_scale_service as extract_property_scale_service
import service.text.extract_rank_service as extract_rank_service
import service.text.extract_sale_mode_service as extract_sale_mode_service
import service.text.extract_trust_service as extract_trust_service
import service.text.extract_user_count_service as extract_user_count_service
import service.text.extract_competitive_edge_service as extract_competitive_edge_service
import service.text.extract_market_rank_service as extract_market_rank_service
import service.text.extract_corporate_culture_service as extract_corporate_culture_service
import service.text.extract_technique_trend_service as extract_technique_trend_service

import service.text.extract_develop_strategy_service as extract_develop_strategy_service
import service.text.extract_industry_position_service as extract_industry_position_service
import service.text.extract_industry_layout_service as extract_industry_layout_service
import service.text.extract_company_industry_trend_service as extract_company_industry_trend_service

import service.table.extract_engineering_service as extract_engineering_service
import service.table.extract_insurance_service as extract_insurance_service
import service.table.extract_media_service as extract_media_service
import service.table.extract_real_property_service as extract_real_property_service
import service.table.extract_user_foundation_service as extract_user_foundation_service
import service.table.extract_capacity as extract_capacity_service
import service.text.extract_rd_plan_service as extract_rd_plan_service
import service.text.extract_capacity_plan_service as extract_capacity_plan_service
import service.table.extract_right_restrict_money_service as extract_right_restrict_money_service
import service.table.extract_5customers_proportion_service as extract_5customers_proportion_service
import service.table.extract_5supplyers_proportion_service as extract_5supplyers_proportion_service
import service.text.extract_project_research_plan_service as extract_project_research_plan_service
import service.text.extract_capacity_extention_plan_service as extract_capacity_extention_plan_service
import service.table.extract_business_reputation_service as extract_business_reputation_service
import service.text.extract_sales_network_service as extract_sales_network_service
import service.text.extract_industry_status_service as extract_industry_status_service
import service.text.extract_creative_marketing_service as extract_creative_marketing_service
import service.table.extract_patent_service as extract_patent_service
import service.text.extract_sale_mode_all_service as extract_sale_mode_all_service
import service.table.extract_product_function_service as extract_product_function_service

# const
# version
VERSION = "0.5"
START_AT = ''  # 默认跑最近一天
END_AT = ''  # 默认跑最近一天
TIME_FIELD_UPDATE = 'updateAt'  # 定时任务使用
TIME_FIELD_PUB = 'pubDateAt'  # debug使用
DEBUG_START_AT = '1483200000000'  # 2017-01-01
DEBUG_END_AT = '1584028800000'  # 2020-03-13


@back_sched.scheduled_job('cron', id='1', name='tax_free',
                          second='0', minute='1', hour='3', day='*', month='*', day_of_week='*')
def extract_tax_free():
    # print("start")
    extract_tax_service.extract_free(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='2', name='vat',
                          second='0', minute='2', hour='3', day='*', month='*', day_of_week='*')
def extract_vat():
    # print("start")
    extract_tax_service.extract_vat(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='3', name='bank_branch',
                          second='0', minute='3', hour='3', day='*', month='*', day_of_week='*')
def extract_bank_branch():
    # print("start")
    extract_branch_service.extract_bank(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='4', name='security_branch',
                          second='0', minute='4', hour='3', day='*', month='*', day_of_week='*')
def extract_security_branch():
    # print("start")
    extract_branch_service.extract_security(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='5', name='copyright',
                          second='0', minute='5', hour='3', day='*', month='*', day_of_week='*')
def extract_copyright():
    # print("start")
    extract_copyright_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='6', name='innovate',
                          second='0', minute='6', hour='3', day='*', month='*', day_of_week='*')
def extract_innovate():
    # print("start")
    extract_innovate_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='7', name='main_channel',
                          second='0', minute='7', hour='3', day='*', month='*', day_of_week='*')
def extract_main_channel():
    # print("start")
    extract_main_channel_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='8', name='main_production',
                          second='0', minute='8', hour='3', day='*', month='*', day_of_week='*')
def extract_main_production():
    # print("start")
    extract_main_production_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='9', name='market_hold',
                          second='0', minute='9', hour='3', day='*', month='*', day_of_week='*')
def extract_market_hold():
    # print("start")
    extract_market_hold_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='10', name='market_scale',
                          second='0', minute='10', hour='3', day='*', month='*', day_of_week='*')
def extract_market_scale():
    # print("start")
    extract_market_scale_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='11', name='property_scale',
                          second='0', minute='11', hour='3', day='*', month='*', day_of_week='*')
def extract_property_scale():
    # print("start")
    extract_property_scale_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='12', name='rank',
                          second='0', minute='12', hour='3', day='*', month='*', day_of_week='*')
def extract_rank():
    # print("start")
    extract_rank_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='13', name='sale_mode',
                          second='0', minute='13', hour='3', day='*', month='*', day_of_week='*')
def extract_sale_mode():
    # print("start")
    extract_sale_mode_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='14', name='trust',
                          second='0', minute='14', hour='3', day='*', month='*', day_of_week='*')
def extract_trust():
    # print("start")
    extract_trust_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='15', name='user_count',
                          second='0', minute='15', hour='3', day='*', month='*', day_of_week='*')
def extract_user_count():
    # print("start")
    extract_user_count_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='16', name='engineering',
                          second='0', minute='16', hour='3', day='*', month='*', day_of_week='*')
def extract_engineering():
    # print("start")
    extract_engineering_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='17', name='insurance',
                          second='0', minute='17', hour='3', day='*', month='*', day_of_week='*')
def extract_insurance():
    # print("start")
    extract_insurance_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='18', name='media',
                          second='0', minute='18', hour='3', day='*', month='*', day_of_week='*')
def extract_media():
    # print("start")
    extract_media_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='19', name='real_property',
                          second='0', minute='19', hour='3', day='*', month='*', day_of_week='*')
def extract_real_property():
    # print("start")
    extract_real_property_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='20', name='user_foundation',
                          second='0', minute='20', hour='3', day='*', month='*', day_of_week='*')
def extract_user_foundation():
    # print("start")
    extract_user_foundation_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='21', name='competitive_edge',
                          second='0', minute='21', hour='3', day='*', month='*', day_of_week='*')
def extract_competitive_edge():
    # print("start")
    extract_competitive_edge_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='22', name='market_rank',
                          second='0', minute='22', hour='3', day='*', month='*', day_of_week='*')
def extract_market_rank():
    # print("start")
    extract_market_rank_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='23', name='develop_strategy',
                          second='40', minute='24', hour='14', day='*', month='*', day_of_week='*')
def extract_develop_strategy():
    # print("start")
    extract_develop_strategy_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='24', name='industry_position',
                          second='20', minute='47', hour='10', day='*', month='*', day_of_week='*')
def extract_industry_position():
    # print("start")
    extract_industry_position_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='29', name='industry_layout',
                          second='0', minute='10', hour='18', day='*', month='*', day_of_week='*')
def extract_industry_layout():
    # print("start")
    extract_industry_layout_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='30', name='company_industry_trend',
                          second='30', minute='16', hour='14', day='*', month='*', day_of_week='*')
def extract_company_industry_trend():
    # print("start")
    extract_company_industry_trend_service.extract(start_at=START_AT, end_at=END_AT,
                                                   time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='25', name='market_hold_all',
                          second='0', minute='25', hour='3', day='*', month='*', day_of_week='*')
def extract_market_hold_all():
    # print("start")
    extract_market_hold_service.extract_all(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='26', name='corporate_culture',
                          second='0', minute='26', hour='3', day='*', month='*', day_of_week='*')
def extract_corporate_culture():
    # print("start")
    extract_corporate_culture_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='27', name='technique_trend',
                          second='0', minute='27', hour='3', day='*', month='*', day_of_week='*')
def extract_technique_trend():
    # print("start")
    extract_technique_trend_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='28', name='market_hold_trend',
                          second='0', minute='28', hour='3', day='*', month='*', day_of_week='*')
def extract_market_hold_trend():
    # print("start")
    extract_market_hold_service.extract_trend(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='31', name='capacity',
                          second='0', minute='31', hour='3', day='*', month='*', day_of_week='*')
def extract_capacity():
    # print("start")
    extract_capacity_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='32', name='rd_plan',
                          second='0', minute='32', hour='3', day='*', month='*', day_of_week='*')
def extract_rd_plan():
    # print("start")
    extract_rd_plan_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='33', name='capacity_plan',
                          second='0', minute='33', hour='4', day='*', month='*', day_of_week='*')
def extract_capacity_plan():
    # print("start")
    extract_capacity_plan_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='34', name='right_restrict_money',
                          second='0', minute='34', hour='4', day='*', month='*', day_of_week='*')
def extract_right_restrict_money():
    # print("start")
    extract_right_restrict_money_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='35', name='5customers_proportion',
                          second='0', minute='35', hour='4', day='*', month='*', day_of_week='*')
def extract_5customers_proportion():
    # print("start")
    extract_5customers_proportion_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='36', name='5supplyers_proportion',
                          second='0', minute='36', hour='4', day='*', month='*', day_of_week='*')
def extract_5supplyers_proportion():
    # print("start")
    extract_5supplyers_proportion_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='37', name='project_research_plan',
                          second='0', minute='37', hour='4', day='*', month='*', day_of_week='*')
def extract_extract_project_research_plan():
    # print("start")
    extract_project_research_plan_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='38', name='capacity_extention_plan',
                          second='0', minute='38', hour='4', day='*', month='*', day_of_week='*')
def extract_capacity_extention_plan():
    # print("start")
    extract_capacity_extention_plan_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='39', name='business_reputation',
                          second='0', minute='39', hour='4', day='*', month='*', day_of_week='*')
def extract_business_reputation():
    # print("start")
    extract_business_reputation_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='40', name='sales_network',
                          second='0', minute='40', hour='4', day='*', month='*', day_of_week='*')
def extract_sales_network():
    # print("start")
    extract_sales_network_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='41', name='industry_status',
                          second='0', minute='41', hour='4', day='*', month='*', day_of_week='*')
def extract_industry_status():
    # print("start")
    extract_industry_status_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='42', name='creative_marketing',
                          second='0', minute='42', hour='4', day='*', month='*', day_of_week='*')
def extract_creative_marketing():
    # print("start")
    extract_creative_marketing_service.extract(start_at=START_AT, end_at=END_AT,
                                               time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='43', name='patent',
                          second='10', minute='43', hour='4', day='*', month='*', day_of_week='*')
def extract_patent():
    # print("start")
    extract_patent_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='44', name='sale_mode_all',
                          second='15', minute='44', hour='4', day='*', month='*', day_of_week='*')
def extract_sale_mode_all():
    # print("start")
    extract_sale_mode_all_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


@back_sched.scheduled_job('cron', id='45', name='product_function',
                          second='15', minute='45', hour='4', day='*', month='*', day_of_week='*')
def extract_product_function():
    # print("start")
    extract_product_function_service.extract(start_at=START_AT, end_at=END_AT, time_field=TIME_FIELD_UPDATE)


class RunExtractHandler(tornado.web.RequestHandler):
    # input: {'startAt':1521648000000,'endAt':1521648000000,'timeField':updateAt,'knowledgeType':'公司税收优惠'}
    def get(self):
        logging.info("run extract by get")
        try:
            start_at = self.get_query_argument('startAt')
        except Exception as e:
            logging.exception(e)
            start_at = ''
        try:
            end_at = self.get_query_argument('endAt')
        except Exception as e:
            logging.exception(e)
            end_at = ''
        try:
            time_field = self.get_query_argument('timeField')
        except Exception as e:
            logging.exception(e)
            time_field = ''
        try:
            knowledge_type = self.get_query_argument('knowledgeType')
        except Exception as e:
            logging.exception(e)
            knowledge_type = ''
        if knowledge_type == '公司税收优惠':
            extract_tax_service.extract_free(start_at=start_at, end_at=end_at, time_field=time_field)
        elif knowledge_type == '公司增值税率':
            extract_tax_service.extract_vat(start_at, end_at, time_field)
        elif knowledge_type == '公司主要产品':
            extract_main_production_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司排名':
            extract_rank_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主要渠道(工程)':
            extract_main_channel_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司营销模式(技术,制造)':
            extract_sale_mode_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司市场规模(技术)':
            extract_market_scale_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司市场占有率(技术)':
            extract_market_hold_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司营业网点(银行)':
            extract_branch_service.extract_bank(start_at, end_at, time_field)
        elif knowledge_type == '公司客户数量(银行)':
            extract_user_count_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司信托项目数量及资产规模(信托)':
            extract_trust_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司分支机构(证券,保险)':
            extract_branch_service.extract_security(start_at, end_at, time_field)
        elif knowledge_type == '公司创新能力(证券)':
            extract_innovate_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主动管理资产规模(证券)':
            extract_property_scale_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司专利数量及金额(计算机)':
            extract_copyright_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司工程类项目金额(工程)':
            extract_engineering_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司保险类续保率(保险)':
            extract_insurance_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司客户基础(证券)':
            extract_user_foundation_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司著作权期末余额(传媒)':
            extract_media_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司房地产指标(房地产)':
            extract_real_property_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司竞争优势':
            extract_competitive_edge_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司市场排名':
            extract_market_rank_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司发展战略':
            extract_develop_strategy_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司行业地位':
            extract_industry_position_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司产业链布局':
            extract_industry_layout_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司所属行业发展趋势':
            extract_company_industry_trend_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司市场占有率':
            extract_market_hold_service.extract_all(start_at, end_at, time_field)
        elif knowledge_type == '公司企业文化特征':
            extract_corporate_culture_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主营产品技术趋势':
            extract_technique_trend_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司市场占有率变化趋势':
            extract_market_hold_service.extract_trend(start_at, end_at, time_field)
        elif knowledge_type == '公司研发规划':
            extract_rd_plan_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司产能规划':
            extract_capacity_plan_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主要产品产能产销情况':
            extract_capacity_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司资产权利受限情况':
            extract_right_restrict_money_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司前五大客户关联情况':
            extract_5customers_proportion_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司前五大供应商关联情况':
            extract_5supplyers_proportion_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司研发规划及进展':
            extract_project_research_plan_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司产能扩张规划及进展':
            extract_capacity_extention_plan_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司商誉来源与商誉减值来源情况':
            extract_business_reputation_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司销售网络':
            extract_sales_network_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主要产品的技术先进性及可替代性':
            extract_industry_status_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司创意-新媒体-数字营销':
            extract_creative_marketing_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司专利与著作权情况':
            extract_patent_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司销售模式':
            extract_sale_mode_all_service.extract(start_at, end_at, time_field)
        elif knowledge_type == '公司主要产品的服务用途及功能情况':
            extract_product_function_service.extract(start_at, end_at, time_field)
        else:
            logging.info('knowledge type not recognized: ' + knowledge_type)
            self.write('knowledge type not recognized: ' + knowledge_type)
            return
        logging.info(
            "finish to run extract: " + knowledge_type + " start at: " + start_at + " end at: " + end_at + " time field: " + time_field)
        self.write(
            "finish to run extract: " + knowledge_type + " start at: " + start_at + " end at: " + end_at + " time field: " + time_field)


class PauseJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobId':'dayTask'}
    def get(self):
        try:
            logging.info("pause job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.pause_job(job_id)
            self.write("pause job: %s" % job_id)
        except Exception as e:
            logging.exception(e)


class ResumeJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobId':'dayTask'}
    def get(self):
        try:
            logging.info("resume job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.resume_job(job_id)
            self.write("resume job: %s" % job_id)
        except Exception as e:
            logging.exception(e)


class RemoveJobHandler(tornado.web.RequestHandler):
    # 接口输入 {'jobName':'dayTask'}
    def get(self):
        try:
            logging.info("remove job by get")
            job_id = self.get_query_argument('jobId')

            back_sched.remove_job(job_id)
            self.write("remove job: %s" % 2)
        except Exception as e:
            logging.exception(e)


class RemoveAllJobsHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("remove all jobs by get")
        back_sched.remove_all_jobs()
        self.write("remove all jobs")


class QueryJobsHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("query jobs by get")
        jobs = back_sched.get_jobs()
        job_info_list = []
        for job in jobs:
            time = job.next_run_time
            time_string = time.strftime("%Y-%m-%d %H:%M:%S")
            job_info = {"job_id": job.id,
                        "job_name": job.name,
                        "next_run_time": time_string}
            job_info_list.append(job_info)
        result_json = json.dumps(job_info_list, ensure_ascii=False)
        self.write(result_json)
        logging.info('query jobs by get finished!')


class ModifyJobHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("modify job by get")
        job_id = self.get_query_argument('jobId')
        job_name = self.get_query_argument('jobName')
        max_instances = self.get_query_argument('maxInstances')
        back_sched.modify_job(job_id, name=job_name, max_instances=max_instances)
        self.write('modify job: ' + job_id + ', new name: ' + job_name + ', new max instances: ' + max_instances)
        logging.info('modify job by get finished!')


class RescheduleJobHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("reschedule job by get")
        job_id = self.get_query_argument('jobId')
        seconds = self.get_query_argument('seconds')
        back_sched.reschedule_job(job_id=job_id, trigger='interval', seconds=seconds)
        logging.info("reschedule job by get finished!")


class StartHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.start()
        result = back_sched.running
        self.write("start scheduler: %s" % result)


class ShutdownSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.shutdown()
        self.write("shutdown scheduler")


class PauseSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.pause()
        self.write("pause scheduler")


class ResumeSchedHandler(tornado.web.RequestHandler):
    def get(self):
        back_sched.resume()
        self.write("resume scheduler")


class Application(tornado.web.Application):

    def __init__(self, config):
        handlers = [
            # run
            (r"/run", RunExtractHandler),
            # scheduler
            (r"/scheduler/start", StartHandler),
            (r"/scheduler/shutdown", ShutdownSchedHandler),
            (r"/scheduler/pause", PauseSchedHandler),
            (r"/scheduler/resume", ResumeSchedHandler),
            # job
            (r"/job/pause", PauseJobHandler),
            (r"/job/resume", ResumeJobHandler),
            (r"/job/remove_one", RemoveJobHandler),
            (r"/job/remove_all", RemoveAllJobsHandler),
            (r"/job/query", QueryJobsHandler),
            (r"/job/modify", ModifyJobHandler),
            (r"/job/rechedule", RescheduleJobHandler),
        ]
        settings = dict(
            debug=bool(config['debug']),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def job_exception_listener(event):
    if event.exception:
        logging.critical("crashed job id: " + event.job_id)
    else:
        logging.info('The job worked :' + event.job_id)


def job_missed_listener(event):
    logging.critical("The job missed: " + event.job_id)


def job_max_instances_listener(event):
    logging.info("The job reached max executing instances : " + event.job_id)


def init_apscheduler():
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    back_sched.add_listener(job_exception_listener,
                            apscheduler.events.EVENT_JOB_ERROR | apscheduler.events.EVENT_JOB_EXECUTED)
    back_sched.add_listener(job_missed_listener, apscheduler.events.EVENT_JOB_MISSED)
    back_sched.add_listener(job_max_instances_listener, apscheduler.events.EVENT_JOB_MAX_INSTANCES)


# config
def parse_conf_file(config_file):
    config = {}
    with io.open(config_file, 'r', encoding='utf8') as f:
        config = json.load(f)
    return config


def main(argv):
    if sys.version_info < (3,):
        reload(sys)
        sys.setdefaultencoding("utf-8")

    if VERSION != __version__:
        print("version error!")
        logging.info("version error!")
        exit(-1)

    if len(argv) < 3:
        print('arg error.')
        exit(-2)

    config = parse_conf_file(argv[1])
    tornado.options.parse_config_file(config['log_config_file'])

    logging.info("Server Inititial ... ")

    app = Application(config)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(config['port'])
    server.start(config['process_num'])

    init_apscheduler()
    back_sched.start()

    logging.info("Server Inititial Success! ")
    print("Server Inititial Success! ")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(sys.argv)
