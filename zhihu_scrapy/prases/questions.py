# -*- coding: utf-8 -*-

import re
import json
import urllib.parse
from lxml import etree
from zhihu_scrapy import settings
from zhihu_scrapy.items import QuestionsItem
import zhihu_scrapy
from scrapy import Request
from scrapy.http import FormRequest

class Questions(object):
    def __init__(self, response):
        self.response = response
        self.item = QuestionsItem()
        self.item["data_type"] = "question"
        self.question_url()
        self.question_url_token()
        self.question_title()
        self.question_desc()
        self.topics()
        self.answers_num()

    def question_url(self):
        self.item["question_url"] = self.response.url

    def question_url_token(self):
        self.item["question_url_token"] = int(self.item["question_url"].split("/")[-1])

    def question_title(self):
        xpath_rule = '//h2[@class="zm-item-title"]/span/text()'
        self.item["question_title"] = self.response.selector.xpath(xpath_rule).extract_first()

    def question_desc(self):
        xpath_rule = '//div[@id="zh-question-detail"]//div/text()'
        self.item["question_desc"] = self.response.selector.xpath(xpath_rule).extract_first()

    def topics(self):
        xpath_rule = '//div[@class="zm-tag-editor-labels zg-clear"]/a/text()'
        self.item["topics"] = [topic[1:-1] for topic in self.response.selector.xpath(xpath_rule).extract()]

    def answers_num(self):
        xpath_rule = '//*[@id="zh-question-answer-num"]/text()'
        num_string = self.response.selector.xpath(xpath_rule).extract_first()
        if num_string is None:
            self.item["answers_num"] = 0
        else:
            pattern = re.compile(r'\d+')
            self.item["answers_num"] = int(re.findall(pattern, num_string)[0])
