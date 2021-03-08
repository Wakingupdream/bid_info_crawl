# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""The constants for crawler."""

import datetime


START_TIME = datetime.datetime.now().strftime("%Y:%m:%d")
END_TIME = datetime.datetime.now().strftime("%Y:%m:%d")
ERROR_RESPONSE_COUNT = 0
INFO_NAME = ["page_url", "project_name", "bid_type", "issue_time", "buyer",
             "agency", "province"]
URL = "http://search.ccgp.gov.cn/bxsearch"
KEY_WORDS = ["社区", "智能社区", "智慧社区", "商业街", "商圈", "智能商圈", "步行街",
             "景区", "智能景区", "智慧景区", "文旅", "机场", "智慧文旅"]
PARAMETER = params_l = {
    "searchtype": 1,
    "page_index": 1,
    "bidSort": 0,
    "buyerName": None,
    "projectId": None,
    "pinMu": 0,
    "bidType": 0,
    "dbselect": "bidx",
    "kw": None,
    "start_time": START_TIME,  # TODO(wangyu/crawl_code):Maybe need modify.
    "end_time": END_TIME,
    "timeType": 5,
    "displayZone": None,
    "zoneId": None,
    "pppStatus": 0,
    "agentName": None,
}
