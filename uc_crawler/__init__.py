# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""UC_Crawler for ccgp."""
import requests
from fake_useragent import UserAgent


UA = UserAgent()
SS = requests.session()  # Named in logical order, not alphabetically.
SS.headers["User-Agent"] = UA.random
