# -*- coding: utf-8 -*-

from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.items import TopicsItem


class Topics(object):
    def __init__(self, response):
        self.response = response
        self.item = TopicsItem()
        self.item["top_answers"] = set()
        self.topic_url()
        self.followers_num()
        self.top_answers()

    def topic_url(self):
        self.item["topic_url"] = self.response.url

    def followers_num(self):
        xpath_rule = '//div[@class="zm-topic-side-followers-info"]//strong/text()'
        self.item["followers_num"] = int(self.response.selector.xpath(xpath_rule).extract_first())

    def top_answers(self):
        answers_xpath_rule = '//div[@itemprop="question"][@data-type="Answer"]//link/@href'
        answers_url = ["".join([settings.BASE_URL, answer_url])
                       for answer_url in self.response.selector.xpath(answers_xpath_rule).extract()]
        self.item["top_answers"].update(answers_url)
        next_page_url_xpath_rule = '//div[@class="zm-invite-pager"]/span/a/@href'
        next_page_url = "".join([
            self.item["topic_url"],
            self.response.selector.xpath(next_page_url_xpath_rule).extract()[-1]
        ])


