# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler run."""


import asyncio

from constant import crawler
from db import connect
from uc_crawler.util import get_all_pages_data


async def main():
    """Statistics of all keywords."""
    await connect()
    for keyword in crawler.KEY_WORDS:
        await get_all_pages_data(keyword, crawler.PARAMETER)


if __name__ == "__main__":
    asyncio.run(main())
