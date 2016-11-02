# -*- coding: utf-8 -*-

from lxml import etree
from zhihu_scrapy import settings
from zhihu_scrapy.items import QuestionsItem


class Questions(object):
    def __init__(self, response):
        self.response = response
        self.item = QuestionsItem()
        self.question_url()
        self.question_name()
        self.topics()
        self.answers_1()

    def question_url(self):
        self.item["question_url"] = self.response.url

    def question_name(self):
        xpath_rule = '//h2[@class="zm-item-title"]/span/text()'
        self.item["question_name"] = self.response.selector.xpath(xpath_rule).extract_first()

    def topics(self):
        xpath_rule = '//div[@class="zm-tag-editor-labels zg-clear"]/a/text()'
        self.item["topics"] = set([topic[1:-1] for topic in self.response.selector.xpath(xpath_rule).extract()])

    def answers_1(self):
        self.item["answers"] = set()
        xpath_rule = '//div[@class="zm-item-answer  zm-item-expanded"]'
        self.item["answers"].update(self.response.selector.xpath(xpath_rule).extract())

    def answers_2(self):
        # todo 通过加载更多获取的数据未完成
        pass
