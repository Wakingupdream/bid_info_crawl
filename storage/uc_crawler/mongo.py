# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Mongo implements of Uc crawler storage."""

from constant import database
from db.mongo import Database
from schemas.crawler import Crawler
from storage.uc_crawler.interface import UcCrawlerStorageInterface


DATABASE_NAME = database.DATABASE_NAME


class UcCrawlerStorage(UcCrawlerStorageInterface):
    """UC Crawler storage."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    async def create(db_collection, create_model: Crawler):
        """Create one crawler."""
        input_model = create_model.dict(exclude_none=True)
        await Database.client[DATABASE_NAME][db_collection].insert_one(
            input_model)
