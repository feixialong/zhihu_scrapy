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
        # todo 对答案中的内容做进一步解析，当前有点赞数，用户url，评论的整体内容
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

    def answers_2(self):
        # todo 通过加载更多获取的数据未完成
        pass
