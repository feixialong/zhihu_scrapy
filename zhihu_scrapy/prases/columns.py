# -*- coding: utf-8 -*-

import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import ColumnsItem


class Columns(object):
    def __init__(self, response):
        self.response = response
        self.item = ColumnsItem()
        self.column_url()
        self.followers_num()

    def column_url(self):
        self.item["column_url"] = self.response.url

    def followers_num(self):
        xpath_rule = '//a[@class="ng-binding ng-scope"]/text()'
        num_str = self.response.selector.xpath(xpath_rule).extract_first()
        # todo Bug待解
        a = tools.get_num_from_str(num_str)[0]
        print("")
        return a
