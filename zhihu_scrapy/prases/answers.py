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
from lxml import etree


class Answers(object):
    def __init__(self, answer):
        self.answer = etree.HTML(answer)
        self.item = AnswersItem()
        self.item["data_type"] = "answer"
        self.user_url()
        self.content()
        self.agrees_num()
        self.answer_url()
        self.question_url()
        self.last_edit_time()

    def user_url(self):
        xpath_rule = '//span[@class="author-link-line"]/a[@class="author-link"]/@href'
        cur_user_url = self.answer.xpath(xpath_rule)
        if len(cur_user_url) == 0:
            self.item["user_url"] = "匿名用户"
        else:
            self.item["user_url"] = "".join([settings.BASE_URL, cur_user_url[0]])

    def content(self):
        xpath_rule = '//div[@class="zm-editable-content clearfix"]'
        content_ = []
        for c in self.answer.xpath(xpath_rule)[0].itertext():
            content_.append(c)
        self.item["content"] = "".join(content_)

    def agrees_num(self):
        xpath_rule = '//span[@class="count"]/text()'
        agrees_num_string = self.answer.xpath(xpath_rule)[0]
        pattern = re.compile(r'\d+')
        num_ = int(re.findall(pattern, agrees_num_string)[0])
        if agrees_num_string[-1] in ["k", "K"]:
            num_ *= 1000
        self.item["agrees_num"] = num_

    def answer_url(self):
        xpath_rule = '//link[@itemprop="url"]/@href'
        cur_answer_url = self.answer.xpath(xpath_rule)[0]
        self.item["answer_url"] = "".join([settings.BASE_URL, cur_answer_url])

    def question_url(self):
        self.item["question_url"] = "/".join(self.item["answer_url"].split("/")[:-2])

    def last_edit_time(self):
        # todo 将此时间改为Unix时间戳，或转成时间格式，不要是字符串
        xpath_rule = '//div[@class="zm-meta-panel"]/a[@class="answer-date-link meta-item"]/text()'
        time_ = self.answer.xpath(xpath_rule)[0]
        self.item["last_edit_time"] = time_[4:]
