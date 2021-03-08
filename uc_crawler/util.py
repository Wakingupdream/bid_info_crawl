# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Utilities for uc-crawler-ccgp."""

import re
import sys
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

from constant import crawler
from uc_crawler import SS
from utils.log import LOG


def get_page_num(params):
    """Get total page num according to specific keyword."""
    res = SS.get(crawler.URL, params=params)
    soup = BeautifulSoup(res.text, "html.parser")
    if soup.find("p", attrs={"class": "pager"}) is None:
        LOG.warning(f"{params['kw']}页数为空")
        sys.exit()
    page_num = re.search("size:(.*),",
                         soup.find("p", attrs={"class": "pager"}).find(
                             "script").next)[1]
    return int(page_num)


def re_connect(elem_bid_list, params, page_index, sec=1):
    """Reconnect when the page is not loaded because the visit is too fast."""
    if elem_bid_list:
        return elem_bid_list
    if sec == 5:
        sec = 1
    res = SS.get(crawler.URL, params=params)
    time.sleep(sec)
    LOG.info(res, page_index)
    soup = BeautifulSoup(res.text, "html.parser")
    elem_bid_list = soup.find("ul", attrs={"class": "vT-srch-result-list-bid"})
    return re_connect(elem_bid_list, params, page_index, sec + 1)


def get_one_page_data(params, page_index):
    """
    Extract page info from key word searching result.

    Page info include page_url, project_name, bid_type, issue_time, buyer,
    agency, province.
    """
    info_dic = {}
    for name in crawler.INFO_NAME:
        info_dic[name] = []

    params["page_index"] = page_index
    res = SS.get(crawler.URL, params=params)
    LOG.info(res, page_index)
    soup = BeautifulSoup(res.text, "html.parser")
    elem_bid_list = soup.find("ul", attrs={"class": "vT-srch-result-list-bid"})
    if elem_bid_list is None:
        elem_bid_list = re_connect(elem_bid_list, params, page_index,
                                   sec=2)
    li_list = elem_bid_list.find_all("li")
    try:
        for elem_bid in li_list:
            info_dic["page_url"].append(elem_bid.a["href"])
            info_dic["bid_type"].append(elem_bid.span.strong.text.split())
            info_dic["project_name"].append(
                "".join(elem_bid.find("a").text.strip()))
            issue_time, buyer, agency, province = elem_bid.span.text.split(
                "|")[:4]
            info_dic["issue_time"].append(issue_time.strip())
            info_dic["buyer"].append(
                re.search("采购人：(.*)", buyer.strip()).group(1))
            info_dic["agency"].append(
                re.search("代理机构：(.*)\r", agency.strip()).group(1))
            info_dic["province"].append(province.strip())
    except ValueError:
        LOG.error("li_list is None.")
    return info_dic


def get_all_pages_data(key_word, params):
    """Get information on all its search pages according to one keyword."""
    params["kw"] = key_word
    page_num = get_page_num(params)
    info_dic = {}
    for name in crawler.INFO_NAME:
        info_dic[name] = []
    with tqdm(total=page_num) as tqdm_bar:
        for page in range(1, page_num + 1):
            one_page_data = get_one_page_data(params, page)
            for key in one_page_data:
                info_dic[key] += one_page_data[key]
        tqdm_bar.update()
    # TODO: write to db
    LOG.info(f"{key_word} finished")


def get_total_from_url(url):
    """Get the bid amount from the url."""
    res = SS.get(url)
    time.sleep(1)
    soup = BeautifulSoup(res.content, "html.parser")
    for short_text in soup.find("div",
                                attrs={"class": "vF_detail_content"}) \
            .find_all("p"):
        match = re.search(r"(预算|成交|中标|（预算）|（成交）|（中标）)金额：(.*)",
                          short_text.text)
        if match:
            return match[2]
    return None
