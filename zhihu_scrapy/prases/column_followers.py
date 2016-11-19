# -*- coding: utf-8 -*-

import json
import re

import requests
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import ColumnFollowersItem


class ColumnFollowers(object):
    def __init__(self, body):
        self.body = body
        self.item = ColumnFollowersItem()
        self.user_url()

    def user_url(self):
        self.item["user_url"] = self.body.get("profileUrl")
