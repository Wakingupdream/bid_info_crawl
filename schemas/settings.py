# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""The settings schema."""

from pydantic import BaseSettings

from constant import settings


class Settings(BaseSettings):
    """Setting for task scheduler."""

    # pylint: disable=too-few-public-methods
    db_type_scheduler: str = settings.DB_TYPE_MONGO
    debug: bool = True

    class Config:
        """Config for settings schema."""

        env_file = settings.ENV_FILE
        env_prefix = settings.ENV_PREFIX
