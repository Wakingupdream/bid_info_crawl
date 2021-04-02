# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""The constants for crawler."""

import datetime
import re


ERROR_RESPONSE_COUNT = 0
F_AGENCY = "agency"
F_AGENCY_CH = "代理机构"
F_AMOUNT = "amount"
F_AMOUNT_CH = "成交金额"
F_BID_TYPE = "bid_type"
F_BID_TYPE_CH = "中标类型"
F_BUYER = "buyer"
F_BUYER_CH = "采购人"
F_ISSUE_TIME = "issue_time"
F_ISSUE_TIME_CH = "发布时间"
F_KEYWORD = "keyword"
F_KEYWORD_CH = "关键词"
F_PROJECT_NAME = "project_name"
F_PROJECT_NAME_CH = "项目名称"
F_PROVINCE = "province"
F_PROVINCE_CH = "省份"
F_UPDATE_TIME = "update_time"
F_UPDATE_TIME_CH = "更新时间"
F_URL = "url"
F_URL_CH = "网页链接"
KEY_WORDS = ["社区", "智能社区", "智慧社区", "商业街", "商圈", "智能商圈", "步行街", "景区", "智能景区",
             "智慧景区", "文旅", "机场", "智慧文旅"]
PARAMETER = {
    "searchtype": 1,
    "page_index": 1,
    "bidSort": 0,
    "buyerName": None,
    "projectId": None,
    "pinMu": 0,
    "bidType": 0,
    "dbselect": "bidx",
    "kw": None,
    "start_time": datetime.datetime.now().strftime("%Y:%m:%d"),
    "end_time": datetime.datetime.now().strftime("%Y:%m:%d"),
    "timeType": 2,
    "displayZone": None,
    "zoneId": None,
    "pppStatus": 0,
    "agentName": None,
}
RE_AGENCY = re.compile("代理机构：(.*)\r")
RE_AMOUNT = re.compile("(预算|成交|中标|（预算）|（成交）|（中标）)金额(（元）|（万元）)?"
                       "：(.*)")
RE_BUYER = re.compile("采购人：(.*)")
RE_PAGE = re.compile("size:(.*),")
SESSION_UA = "User-Agent"
URL = "http://search.ccgp.gov.cn/bxsearch"
