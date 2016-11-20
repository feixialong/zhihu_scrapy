# -*- coding: utf-8 -*-

import json
import re

import requests
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import ColumnArticlesItem


class ColumnArticles(object):
    def __init__(self, body):
        self.body = body
        self.item = ColumnArticlesItem()
        self.item["data_type"] = "article"
        self.article_url()
        self.article_title()
        self.user_url()
        self.content()
        self.agrees_num()
        self.comments_url()
        self.published_time()
        self.href_url()

    def article_url(self):
        self.item["article_url"] = "".join([settings.ZHUANLAN_BASE_URL, self.body.get("url")])

    def article_title(self):
        self.item["article_title"] = self.body.get("title")

    def user_url(self):
        self.item["user_url"] = self.body.get("author").get("profileUrl")

    def content(self):
        self.item["content"] = self.body.get("content")

    def agrees_num(self):
        self.item["agrees_num"] = self.body.get("likesCount")

    def comments_url(self):
        self.item["comments_url"] = "".join([settings.ZHUANLAN_BASE_URL, self.body.get("links").get("comments")])

    def published_time(self):
        self.item["published_time"] = self.body.get("publishedTime")

    def href_url(self):
        self.item["href_url"] = "".join([settings.ZHUANLAN_BASE_URL, self.body.get("href")])
