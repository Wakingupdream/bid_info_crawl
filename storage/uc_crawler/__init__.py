# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler storage initialization."""


import importlib

from uc_log import UCLog

from settings import SETTINGS


LOG = UCLog().logger


def get_instance():
    """Return a uc_crawler storage."""
    try:
        module_instance = importlib.import_module(
            f"{__name__}.{SETTINGS.db_type_scheduler.lower()}")
    except ImportError as error:
        LOG.info(repr(error))
    return module_instance.UcCrawlerStorage


UC_CRAWLER_STORAGE = get_instance()
