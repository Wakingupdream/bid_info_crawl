# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Database initialization."""

import importlib

from constant.settings import DB_TYPE_MONGO
from settings import SETTINGS


DB_SET = {
    SETTINGS.db_type_ccgp_crawler.lower(),
}


async def connect():
    """DB connect."""
    if DB_TYPE_MONGO.lower() in DB_SET:
        module_instance = importlib.import_module(
            f"{__name__}.{DB_TYPE_MONGO.lower()}")
        await module_instance.Database.connect()


async def disconnect():
    """DB disconnect."""
    if DB_TYPE_MONGO.lower() in DB_SET:
        module_instance = importlib.import_module(
            f"{__name__}.{DB_TYPE_MONGO.lower()}")
        await module_instance.Database.disconnect()
