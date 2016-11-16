# -*- coding: utf-8 -*-

import json
import re

import requests
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import AnswersItem


class Answers(object):
    def __init__(self, response):
        self.response = response
        # self.body = json.loads(response.body.decode("utf-8"))
        self.item = AnswersItem()
        self.question_url()

    def question_url(self):
        print("进入了Answer解析类：")
        print(self.response.url)

    def answer_url(self):
        pass
