# -*- coding: utf-8 -*-

import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy.items import FollowersItem


class Followers(object):
    def __init__(self, response):
        self.offset = 0
        self.response = response
        self.item = FollowersItem()
        self.cur_user_url()
        self.total_num()
        self.followers_1()

    def cur_user_url(self):
        xpath_rule = '//a[@class="item home first "]/@href'
        cur_user_url = self.response.selector.xpath(xpath_rule).extract_first()
        self.item["user_url"] = "".join([settings.BASE_URL, cur_user_url])

    def total_num(self):
        xpath_rule = '//span[@class="zm-profile-section-name"]/text()'
        total_ = self.response.selector.xpath(xpath_rule).extract_first()
        pattern = re.compile(r'\d+')
        total = re.findall(pattern, total_)
        self.item["total_num"] = int(total[0])

    def followers_1(self):
        xpath_rule = '//a[@class="zg-link author-link"]/@href'
        follower_urls = self.response.selector.xpath(xpath_rule).extract()
        self.item["followers"] = set(follower_urls)