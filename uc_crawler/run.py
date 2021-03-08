# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler run."""


from constant import crawler
from uc_crawler.util import get_all_pages_data


if __name__ == "__main__":
    key_word_list = crawler.KEY_WORDS
    get_all_pages_data("社区", crawler.PARAMETER)
