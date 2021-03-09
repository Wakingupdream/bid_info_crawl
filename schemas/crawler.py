# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Crawler schema."""

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from constant import description


class CCGPBidInfoInDB(BaseModel):
    """Schema of CCGP bid info."""

    agency: str = Field(None, description=description.AGENCY)
    amount: str = Field(None, description=description.AMOUNT)
    buyer: str = Field(None, description=description.BUYER)
    bid_type: str = Field(None, description=description.BID_TYPE)
    issue_time: str = Field(None, description=description.ISSUE_TIME)
    keyword: str = Field(None, description=description.KEYWORD)
    project_name: str = Field(None, description=description.PROJECT_NAME)
    province: str = Field(None, description=description.PROVINCE)
    update_time: str = Field(None, description=description.UPDATE_TIME)
    url: HttpUrl = Field(..., description=description.URL)
