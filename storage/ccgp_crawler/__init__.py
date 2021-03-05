# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler storage initialization."""


import importlib

from settings import SETTINGS
from utils.log import LOG


def get_instance():
    """Return a uc_crawler storage."""
    try:
        module_instance = importlib.import_module(
            f"{__name__}.{SETTINGS.db_type_ccgp_crawler.lower()}")
    except ImportError as error:
        LOG.error(error)
    return module_instance.CCGPBidInfoStorage


CCGP_CRAWLER_STORAGE = get_instance()
