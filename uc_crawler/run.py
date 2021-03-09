# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler run."""


import asyncio

from constant import crawler
from uc_crawler.util import get_all_pages_data


if __name__ == "__main__":
    asyncio.run(get_all_pages_data("智慧文旅", crawler.PARAMETER))
