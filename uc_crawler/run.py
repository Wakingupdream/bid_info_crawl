# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler run."""


import asyncio

from constant import crawler
from uc_crawler.util import get_all_pages_data
from utils.log import LOG


# asyncio.run(connect())

if __name__ == "__main__":
    # key_word_list = crawler.KEY_WORDS
    asyncio.run(get_all_pages_data("社区", crawler.PARAMETER))
    LOG.info(f"Count of error response is {crawler.ERROR_RESPONSE_COUNT}")
