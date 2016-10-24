# -*- coding: utf-8 -*-

import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy.items import AsksItem


class Asks(object):
    def __init__(self, response):
        self.response = response
        self.item = AsksItem
