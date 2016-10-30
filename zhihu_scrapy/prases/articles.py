# -*- coding: utf-8 -*-

import json
import re

import requests
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import ArticlesItem


class Articles(object):
    def __init__(self, response):
        self.response = response
        self.item = ArticlesItem()

    def article_url(self):
        pass

