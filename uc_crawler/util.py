# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Utilities for uc-crawler-ccgp."""

import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from constant import crawler
from schemas.crawler import CCGPBidInfoInDB
from storage.ccgp_crawler import CCGP_CRAWLER_STORAGE
from uc_crawler import SS
from uc_crawler import UA
from utils.log import LOG


def get_page_num(params):
    """Get total page num according to specific keyword."""
    res = SS.get(crawler.URL, params=params)
    soup = BeautifulSoup(res.text, "html.parser")
    if soup.find("p", attrs={"class": "pager"}) is None:
        LOG.warning(f"{params['kw']}页数为空")
        sys.exit()
    page_num = re.search(crawler.RE_PAGE,
                         soup.find("p", attrs={"class": "pager"}).find(
                             "script").next)[1]
    return int(page_num)


def get_response(params):
    """Return the response of session.get ."""
    sec = 1
    while True:
        if sec == 10:
            LOG.error("Unresolved Problem.\n")
            return None
        time.sleep(sec)
        try:
            res = SS.get(crawler.URL, params=params)
        except requests.exceptions.ProxyError:
            SS.headers[crawler.SESSION_UA] = UA.ramdom
            continue
        if len(res.history) == 0:  # todo: Wrong.
            return res
        sec += 1


def get_one_page_data(params, page_index):
    """
    Extract page info from key word searching result.

    Page info include page_url, project_name, bid_type, issue_time, buyer,
    agency, province.
    """
    params["page_index"] = page_index
    res = get_response(params)
    if res is None:
        crawler.ERROR_RESPONSE_COUNT += 1
        sys.exit()  # todo: improvement
    soup = BeautifulSoup(res.text, "html.parser")
    elem_bid_list = soup.find("ul", attrs={"class": "vT-srch-result-list-bid"})
    li_list = elem_bid_list.find_all("li")
    try:
        for elem_bid in li_list:
            issue_time, buyer, agency, province = elem_bid.span.text.split(
                "|")[:4]
            info_dic = {"url": elem_bid.a["href"],
                        "bid_type": elem_bid.span.strong.text.split(),
                        "project_name": "".join(
                            elem_bid.find("a").text.strip()),
                        "issue_time": issue_time.strip(),
                        "buyer": re.search(crawler.RE_BUYER,
                                           buyer.strip()).group(1),
                        "agency": re.search(crawler.RE_AGENCY,
                                            agency.strip()).group(1),
                        "province": province.strip(),
                        "amount": get_total_from_url(elem_bid.a["href"]),
                        "keyword": params["kw"]}
            CCGP_CRAWLER_STORAGE.create("TEST_collection",
                                        CCGPBidInfoInDB(**info_dic))
    except ValueError:
        LOG.error("li_list is None.")


def get_all_pages_data(key_word, params):
    """Get information on all its search pages according to one keyword."""
    params["kw"] = key_word
    page_num = get_page_num(params)
    with tqdm(total=page_num) as tqdm_bar:
        for page in range(1, page_num + 1):
            get_one_page_data(params, page)
            tqdm_bar.update()
    LOG.info(f"{key_word} finished")


def get_total_from_url(url):
    """Get the bid amount from the url."""
    time.sleep(1)
    res = SS.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    elem_content = soup.find("div", attrs={"class": "vF_detail_content"})
    for short_text in elem_content.find_all("p"):
        match = re.search(crawler.RE_AMOUNT, short_text.text)
        if match:
            return match[3]
    return None
