# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""The constants for crawler."""

import datetime


START_TIME = datetime.datetime.now().strftime("%Y:%m:%d")
END_TIME = datetime.datetime.now().strftime("%Y:%m:%d")
ERROR_RESPONSE_COUNT = 0
F_AGENCY = "agency"
F_AMOUNT = "amount"
F_BID_TYPE = "bid_type"
F_BUYER = "buyer"
F_ISSUE_NAME = "issue_time"
F_KEYWORD = "keyword"
F_PROJECT_NAME = "project_name"
F_PROVINCE = "province"
F_UPDATE_TIME = "update_time"
F_URL = "url"
URL = "http://search.ccgp.gov.cn/bxsearch"
KEY_WORDS = ["社区", "智能社区", "智慧社区", "商业街", "商圈", "智能商圈", "步行街",
             "景区", "智能景区", "智慧景区", "文旅", "机场", "智慧文旅"]
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
    "start_time": START_TIME,
    "end_time": END_TIME,
    "timeType": 5,  # TODO(wangyu):Set as parameter.
    "displayZone": None,
    "zoneId": None,
    "pppStatus": 0,
    "agentName": None,
}
RE_AGENCY = "代理机构：(.*)\r"
RE_AMOUNT = "(预算|成交|中标|（预算）|（成交）|（中标）)金额(（元）|（万元）)?：(.*)"
RE_BUYER = "采购人：(.*)"
RE_PAGE = "size:(.*),"
SESSION_UA = "User-Agent"
