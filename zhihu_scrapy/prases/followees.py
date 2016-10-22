# -*- coding: utf-8 -*-

import json
import re
from urllib.parse import urlencode

import scrapy
from scrapy import Request

from zhihu_scrapy import settings
from zhihu_scrapy.items import FolloweesItem
import requests

from zhihu_scrapy import tools
from zhihu_scrapy.spiders import login


class Followees(object):
    def __init__(self, response):
        self.offset = 0
        self.response = response
        self.item = FolloweesItem()
        self.cur_user_url()
        self.total_num()
        # self.followees_1()
        self.followees_2()

    def cur_user_url(self):
        xpath_rule = '//a[@class="item home first "]/@href'
        cur_user_url = self.response.selector.xpath(xpath_rule).extract_first()
        self.item["user_url"] = "".join([settings.PRE_URL, cur_user_url])

    def total_num(self):
        xpath_rule = '//span[@class="zm-profile-section-name"]/text()'
        total_ = self.response.selector.xpath(xpath_rule).extract_first()
        pattern = re.compile(r'\d+')
        total = re.findall(pattern, total_)
        self.item["total_num"] = int(total[0])

    def followees_1(self):
        xpath_rule = '//a[@class="zg-link author-link"]/@href'
        followee_urls = self.response.selector.xpath(xpath_rule).extract()
        self.item["followees"] = set(followee_urls)

    def followees_2(self):
        xpath_rule = '//*[@id="zh-profile-follows-list"]//div/@data-init'
        data_init = self.response.selector.xpath(xpath_rule).extract_first()
        data_init = json.loads(data_init)

        _xsrf_xpath_rule = '//input[@name="_xsrf"]/@value'
        _xsrf = self.response.selector.xpath(_xsrf_xpath_rule).extract_first()

        params = data_init["params"]
        params["offset"] = 40
        print(params, type(params))
        params = json.dumps(params)
        data = {
            "method": "next",
            "params": params,
            "_xsrf": _xsrf
        }
        print(data)
        print("\n" * 2)
        headers = tools.set_headers(self.response.url)
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["X-Xsrftoken"] = _xsrf
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["Origin"] = "https://www.zhihu.com"
        headers["Accept"] = "*/*"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"

        print(headers)
        url = "https://www.zhihu.com/node/ProfileFolloweesListV2"
        session = requests.session()
        session.cookies = login.read_cookie()
        session.headers = headers
        data = json.dumps(data)

        print("")
        r = session.post(url, data=data)



if __name__ == "__main__":
    psss