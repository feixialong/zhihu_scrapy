# -*- coding: utf-8 -*-

import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy.items import ColumnsItem


class Columns(object):
    def __init__(self, response):
        self.response = response
        self.item = ColumnsItem

    def column_url(self):
        self.item["column_url"] = ""