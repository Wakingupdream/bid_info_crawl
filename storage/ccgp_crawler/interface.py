# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""CCGP Crawler storage interface."""

from abc import ABC
from abc import abstractmethod


class CCGPBidInfoStorageInterface(ABC):
    """CCGP bid info storage interface."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    @abstractmethod
    async def create(db_collection, create_model):
        """Create one CCGP bid info storage interface."""
