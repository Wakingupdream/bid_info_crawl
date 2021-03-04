# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Utilities for uc-crawler-ccgp."""

import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm

from constant import crawler
from utils.log import LOG


def get_page_num(params):  # TODO:注意调用的时候参数及位置,params 要添加key_word
    """Get total page num according to specific keyword."""
    ua_l = UserAgent()
    ss_l = requests.session()
    ss_l.headers["User-Agent"] = ua_l.random
    params_l = params
    url_l = crawler.URL
    res_l = ss_l.get(url_l, params=params_l)
    soup_l = BeautifulSoup(res_l.text, "html.parser")
    if soup_l.find("p", attrs={"class": "pager"}) is None:
        LOG.info(f"{params['kw']}页数为空")
        sys.exit()
    page_num = re.search("size:(.*),",
                         soup_l.find("p", attrs={"class": "pager"}).find(
                             "script").next)[1]
    return int(page_num)


def re_connect(elem_bid_list, ss_l, params_l, page_index, sec=1):
    """Reconnect when the page is not loaded because the visit is too fast."""
    if elem_bid_list:
        return elem_bid_list
    if sec == 5:
        ua_l = UserAgent()
        ss_l = requests.session()
        ss_l.headers["User-Agent"] = ua_l.random
        sec = 1
    res_l = ss_l.get(crawler.URL, params=params_l)
    time.sleep(sec)
    LOG.info(res_l, page_index)
    soup = BeautifulSoup(res_l.text, "html.parser")
    elem_bid_list = soup.find("ul", attrs={"class": "vT-srch-result-list-bid"})
    return re_connect(elem_bid_list, ss_l, params_l, page_index, sec + 1)


def get_one_page_data(ua_l, ss_l, params, page_index):  # TODO:注意调用的时候参数及位置
    """
    Extract page info from key word searching result.

    Page info include page_url, project_name, bid_type, issue_time, buyer,
    agency, province.
    """
    info_dic = {}
    for name in crawler.INFO_NAME:
        info_dic[name] = []

    params_l = params
    params_l["page_index"] = page_index
    ss_l.headers["User-Agent"] = ua_l.random
    url = crawler.URL

    res_l = ss_l.get(url, params=params_l)
    LOG.info(res_l, page_index)
    soup = BeautifulSoup(res_l.text, "html.parser")
    elem_bid_list = soup.find("ul", attrs={"class": "vT-srch-result-list-bid"})
    if elem_bid_list is None:
        elem_bid_list = re_connect(elem_bid_list, ss_l, params_l, page_index,
                                   sec=2)
    li_list = elem_bid_list.find_all("li")
    try:
        for elem_bid in li_list:
            info_dic["page_url"].append(elem_bid.a["href"])
            info_dic["bid_type"].append(elem_bid.span.strong.text.split())
            info_dic["project_name"].append(
                "".join(elem_bid.find_all("a")[0].text.strip()))
            i_b_a_p = elem_bid.span.text.split("|")[:4]
            info_dic["issue_time"].append(i_b_a_p[0].strip())
            info_dic["buyer"].append(
                re.search("采购人：(.*)", i_b_a_p[1].strip()).group(1))
            info_dic["agency"].append(
                re.search("代理机构：(.*)\r", i_b_a_p[2].strip()).group(1))
            info_dic["province"].append(i_b_a_p[3].strip())
    except ValueError:
        LOG.error("li_list is None.")
    return info_dic


def get_all_pages_data(key_word, params):
    """Get information on all its search pages according to one keyword."""
    page_num = get_page_num(key_word)
    # res = {"url": [], "type": [], "header": [], "time": [], "buyer": [],
    #        "agency": [], "province": []}
    info_dic = {}
    for name in crawler.INFO_NAME:
        info_dic[name] = []
    with tqdm(total=page_num) as tqdm_bar:
        for page in range(1, page_num + 1):
            ua_l = UserAgent()
            ss_l = requests.session()
            params_l = params
            params_l["kw"] = key_word
            one_page_data = get_one_page_data(ua_l, ss_l, params_l, page)
            for key in one_page_data:
                info_dic[key] += one_page_data[key]
        tqdm_bar.update()
    # TODO: write to db
    LOG.info(f"{key_word} finished")


def get_total_from_url(url):
    """Get the bid amount from the url."""
    ua_l = UserAgent()
    ss_l = requests.session()
    ss_l.headers["User-Agent"] = ua_l.random
    res_l = ss_l.get(url)
    time.sleep(1)
    soup = BeautifulSoup(res_l.content, "html.parser")
    for short_text in soup.find("div",
                                attrs={"class": "vF_detail_content"}) \
            .find_all("p"):
        match = re.search(r"(预算|成交|中标|（预算）|（成交）|（中标）)金额：(.*)",
                          short_text.text)
        if match:
            return match[2]
    return None
