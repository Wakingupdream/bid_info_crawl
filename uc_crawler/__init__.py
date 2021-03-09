# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""UC_Crawler for ccgp."""


import requests
from fake_useragent import UserAgent

from constant import crawler


UA = UserAgent()
SS = requests.session()
SS.headers[crawler.SESSION_UA] = UA.random
