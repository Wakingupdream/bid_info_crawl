# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Mongo implements of CCGP crawler storage."""

from constant import database
from db.mongo import Database
from schemas.crawler import CCGPBidInfoInDB
from storage.ccgp_crawler.interface import CCGPBidInfoStorageInterface


DATABASE_NAME = database.DATABASE_NAME


class CCGPBidInfoStorage(CCGPBidInfoStorageInterface):
    """Implement storage of CCGP bid info."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    def create(db_collection, create_model: CCGPBidInfoInDB):
        """Create a CCPG bid info entry."""
        input_model = create_model.dict(exclude_none=True)
        Database.client[DATABASE_NAME][db_collection].insert_one(
            input_model)
