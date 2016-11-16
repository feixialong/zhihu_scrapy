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
        self.question_url()
        self.question_url_token()
        self.question_name()
        self.question_desc()
        self.topics()
        self.answers_num()
        self.answers()

    def question_url(self):
        self.item["question_url"] = self.response.url

    def question_url_token(self):
        self.item["question_url_token"] = int(self.item["question_url"].split("/")[-1])

    def question_name(self):
        xpath_rule = '//h2[@class="zm-item-title"]/span/text()'
        self.item["question_name"] = self.response.selector.xpath(xpath_rule).extract_first()

    def question_desc(self):
        xpath_rule = '//div[@id="zh-question-detail"]//div/text()'
        self.item["question_desc"] = self.response.selector.xpath(xpath_rule).extract_first()

    def topics(self):
        xpath_rule = '//div[@class="zm-tag-editor-labels zg-clear"]/a/text()'
        self.item["topics"] = set([topic[1:-1] for topic in self.response.selector.xpath(xpath_rule).extract()])

    def answers_num(self):
        xpath_rule = '//*[@id="zh-question-answer-num"]/text()'
        num_string = self.response.selector.xpath(xpath_rule).extract_first()
        pattern = re.compile(r'\d+')
        self.item["answers_num"] = int(re.findall(pattern, num_string)[0])

    def answers(self):
        pagesize = 10
        times_ = int(self.item["answers_num"] / pagesize + 1)
        self.item["answers"] = []
        for i in range(times_):
            params = {
                "url_token": self.item["question_url_token"],
                "pagesize": pagesize,
                "offset": pagesize * i
            }
            data = {
                "method": "next",
                "params": json.dumps(params)
            }
            self.item["answers"].append({"post_body": data})
            # yield FormRequest(
            #     url=settings.MORE_ANSWERS_URL,
            #     body=urllib.parse.urlencode(data),
            #     headers=settings.MORE_ANSWERS_HEADER,
            #     method="POST"
            # )

    def answers_1(self):
        # todo 对答案中的内容做进一步解析，当前有点赞数，用户url，评论的整体内容（此项可在抓取后再处理，也不不改，暂不处理）
        self.item["answers"] = set()
        xpath_rule = '//div[@class="zm-item-answer  zm-item-expanded"]'
        tabs = self.response.selector.xpath(xpath_rule).extract()
        votes_num_rule = '//a[@class="more text"]/span/text()'
        user_url_rule = '//a[@class="author-link"]/@href'
        for tab in tabs:
            doc = etree.HTML(tab)
            # 点赞数，没此项说明为0
            votes_num = doc.xpath(votes_num_rule)
            if len(votes_num) == 0:
                votes_num = 0
            else:
                votes_num = votes_num[0]
            # 用户网址，没此项说明为匿名用户
            user_url = doc.xpath(user_url_rule)
            if len(user_url) == 0:
                user_url = "匿名用户"
            else:
                user_url = "".join([settings.BASE_URL, user_url[0]])

            answer = {
                "votes_num": int(votes_num),
                "user_url": user_url,
                "content": tab
            }
            self.item["answers"].update(answer)
            print("")

        def answers_more(self):
            # todo 通过加载更多获取的数据未完成
            pass
