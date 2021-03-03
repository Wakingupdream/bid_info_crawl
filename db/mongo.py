# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""Mongo DB."""

from motor.motor_asyncio import AsyncIOMotorClient

from settings import SETTINGS
from utils.log import LOG


class Database:
    """Database."""

    client: AsyncIOMotorClient = None

    @classmethod
    def connect(cls):
        """Connect to mongodb."""
        if SETTINGS.db_mongo_uri:
            cls.client = AsyncIOMotorClient(SETTINGS.db_mongo_uri)
        else:
            LOG.info("Connection failed.")

    @classmethod
    def disconnect(cls):
        """Disconnect from mongodb."""
        if cls.client:
            cls.client.close()
