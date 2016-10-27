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
        self.author()
        self.followers_num()
        self.topics()
        self.articles()
        self.followers()

    def get_xsrf(self):
        return self.response.selector.xpath("")

    def column_url(self):
        self.item["column_url"] = settings.COLUMNS_BASE_URL + self.body.get("url")

    def api_url(self):
        self.item["api_url"] = settings.COLUMNS_BASE_URL + self.body.get('href')

    def column_name(self):
        self.item["column_name"] = self.body.get("name")

    def column_desc(self):
        self.item["column_desc"] = self.body.get("intro")

    def author(self):
        self.item["user_url"] = self.body.get("creator").get("profileUrl")

    def followers_num(self):
        self.item["followers_num"] = int(self.body.get("followersCount"))

    def topics(self):
        topics_ = []
        for topic in self.body.get("postTopics"):
            topics_.append(topic.get("name"))
        self.item["topics"] = set(topics_)

    def articles(self):
        LIMIT = 20
        offset = 0
        articles = []
        url = "".join([self.item["api_url"], "/posts"])
        session = requests.session()
        session.headers = {
            "Connection": "keep-alive"
        }
        params = {
            "limit": LIMIT,
            "offset": offset
        }
        response = json.loads(session.get(url,
                                          params=params
                                          ).text)

        while len(response) >= LIMIT:
            for i in response:
                articles.append("".join([settings.COLUMNS_BASE_URL, i.get("url")]))
            offset += LIMIT
            params = {
                "limit": LIMIT,
                "offset": offset
            }
            response = json.loads(session.get(url,
                                              params=params
                                              ).text)
        self.item["articles"] = set(articles)

    def followers(self):
        LIMIT = 20
        offset = 0
        followers = []
        url = "".join([self.item["api_url"], "/followers"])
        session = requests.session()
        session.headers = {
            "Connection": "keep-alive"
        }
        params = {
            "limit": LIMIT,
            "offset": offset
        }
        response = json.loads(session.get(url,
                                          params=params
                                          ).text)
        print("")
        while len(response) >= LIMIT:
            for i in response:
                followers.append(i.get("profileUrl"))
            offset += LIMIT
            params = {
                "limit": LIMIT,
                "offset": offset
            }
            response = json.loads(session.get(url,
                                              params=params
                                              ).text)
        self.item["followers"] = set(followers)


