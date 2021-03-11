# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Utilities for uc-crawler-ccgp."""

import time
from datetime import datetime

import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from constant import crawler
from constant import database
from schemas.crawler import CCGPBidInfoInDB
from settings import SETTINGS
from storage.ccgp_crawler import CCGP_CRAWLER_STORAGE
from uc_crawler import SS
from uc_crawler import UA
from utils.log import LOG


def get_page_num(params):
    """Get total page num according to specific keyword."""
    time.sleep(2)
    res = SS.get(crawler.URL, params=params)
    soup = BeautifulSoup(res.text, "html.parser")
    if soup.find("p", attrs={"class": "pager"}) is None:
        LOG.warning(f"{params['kw']}页数为空")
        return 0
    page_num = crawler.RE_PAGE.search(
        soup.find("p", attrs={"class": "pager"}).find("script").next)[1]
    return int(page_num)


def get_response(params):
    """Return the response of session.get."""
    sec = 1
    while True:
        time.sleep(sec)
        sec += 1
        if sec == 10:
            LOG.info(f"{params}")
            LOG.error("Unresolved Problem.\n")
            return None
        try:
            res = SS.get(crawler.URL, params=params)
        except requests.exceptions.ProxyError as exc:
            LOG.info(f"{exc}")
            LOG.info(f"{params}")
            LOG.error("Unresolved Problem.\n")
            SS.headers[crawler.SESSION_UA] = UA.ramdom
            continue
        if len(res.history) == 0:  # TODO(wangyu):wrong but useful.
            return res


async def get_one_page_data(params, page_index):
    """
    Extract page info from key word searching result.

    Page info include page_url, project_name, bid_type, issue_time, buyer,
    agency, province.
    """
    params["page_index"] = page_index
    res = get_response(params)
    if res:
        soup = BeautifulSoup(res.text, "html.parser")
        elem_bid_list = soup.find("ul", attrs={"class":
                                               "vT-srch-result-list-bid"})
        li_list = elem_bid_list.find_all("li")
        for elem_bid in li_list:
            issue_time, buyer, agency, province = elem_bid.span.text.split(
                "|")[:4]
            info_dic = {
                crawler.F_URL: elem_bid.a["href"],
                crawler.F_BID_TYPE: elem_bid.span.strong.text.split()[0],
                crawler.F_PROJECT_NAME: "".join(
                    elem_bid.find("a").text.strip()),
                crawler.F_ISSUE_NAME: issue_time.strip(),
                crawler.F_BUYER: crawler.RE_BUYER.search(buyer.strip()).group(
                    1),
                crawler.F_AGENCY: crawler.RE_AGENCY.search(
                    agency.strip()).group(1),
                crawler.F_PROVINCE: province.strip(),
                crawler.F_AMOUNT: get_total_from_url(elem_bid.a["href"]),
                crawler.F_KEYWORD: params["kw"],
                crawler.F_UPDATE_TIME: datetime.now()}
            await CCGP_CRAWLER_STORAGE.create(database.COLLECTION_NAME,
                                              CCGPBidInfoInDB(**info_dic))


async def get_all_pages_data(key_word, params):
    """Get information on all its search pages according to one keyword."""
    params["kw"] = key_word
    page_num = get_page_num(params)
    with tqdm(total=page_num) as tqdm_bar:
        for page in range(1, page_num + 1):
            await get_one_page_data(params, page)
            tqdm_bar.update()
    LOG.info(f"{key_word} finished")


def get_total_from_url(url):
    """Get the bid amount from the url."""
    res = SS.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    elem_content = soup.find("div", attrs={"class": "vF_detail_content"})
    for short_text in elem_content.find_all("p"):
        match = crawler.RE_AMOUNT.search(short_text.text)
        if match:
            return match[3]
    return None


def read_data_from_db():
    """Read data from mongo and write to xls."""
    client = pymongo.MongoClient(SETTINGS.db_mongo_uri)
    collection = client[database.DATABASE_NAME][database.COLLECTION_NAME]
    data_df = pd.DataFrame(list(collection.find()))
    date_str = datetime.now().strftime("%Y-%m-%d")
    data_df.to_excel(f"./bid_info_{date_str}.xls", sheet_name="bid_info",
                     index=None)
