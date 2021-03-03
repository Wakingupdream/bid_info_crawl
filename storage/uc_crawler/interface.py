# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Uc Crawler storage interface."""

from abc import ABC
from abc import abstractmethod


class UcCrawlerStorageInterface(ABC):
    """Uc crawler storage interface."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    @abstractmethod
    async def create(db_collection, create_model):
        """Create one task scheduler interface."""
