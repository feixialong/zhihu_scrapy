# -*- coding: utf-8 -*-

import json
import re

import requests
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import ColumnsItem


class Columns(object):
    def __init__(self, response):
        self.response = response
        self.body = json.loads(response.body.decode("utf-8"))
        self.item = ColumnsItem()
        self.column_url()
        self.api_url()
        self.column_name()
        self.column_desc()
        self.user_url()
        self.articles_num()
        self.followers_num()
        self.topics()

    def column_url(self):
        self.item["column_url"] = settings.ZHUANLAN_BASE_URL + self.body.get("url")

    def api_url(self):
        self.item["api_url"] = settings.ZHUANLAN_BASE_URL + self.body.get('href')

    def column_name(self):
        self.item["column_name"] = self.body.get("name")

    def column_desc(self):
        self.item["column_desc"] = self.body.get("intro")

    def user_url(self):
        self.item["user_url"] = self.body.get("creator").get("profileUrl")

    def articles_num(self):
        self.item["articles_num"] = self.body.get("postsCount")

    def followers_num(self):
        self.item["followers_num"] = int(self.body.get("followersCount"))

    def topics(self):
        topics_ = []
        for topic in self.body.get("postTopics"):
            topics_.append(topic.get("name"))
        self.item["topics"] = set(topics_)