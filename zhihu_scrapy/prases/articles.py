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
        self.body = json.loads(self.response.body.decode("utf-8"))
        self.item = ArticlesItem()
        self.article_url()
        self.article_title()
        self.user_url()
        self.content()
        self.agrees_num()
        self.columns()
        self.topics()
        self.comments_url()

    def article_url(self):
        self.item["article_url"] = self.response.url

    def article_title(self):
        self.item["article_title"] = self.body.get("title")

    def user_url(self):
        self.item["user_url"] = self.body.get("author").get("profileUrl")

    def content(self):
        self.item["content"] = self.body.get("content")

    def agrees_num(self):
        self.item["agrees_num"] = self.body.get("likesCount")

    def columns(self):
        self.item["columns"] = self.body.get("column").get("slug")

    def topics(self):
        self.item["topics"] = self.body.get("topics")

    def comments_url(self):
        self.item["comments_url"] = "".join([settings.ZHUANLAN_BASE_URL, self.body.get("links").get("comments")])

