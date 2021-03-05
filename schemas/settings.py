# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""The settings schema."""

from pydantic import BaseSettings

from constant import settings


class Settings(BaseSettings):
    """Setting for CCGP Crawler."""

    # pylint: disable=too-few-public-methods
    db_mongo_uri: str = None
    db_type_ccgp_crawler: str = settings.DB_TYPE_MONGO
    debug: bool = True

    class Config:
        """Config for settings schema."""

        env_file = settings.ENV_FILE
        env_prefix = settings.ENV_PREFIX
