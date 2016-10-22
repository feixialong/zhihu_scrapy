# -*- coding: utf-8 -*-

from zhihu_scrapy import settings
from zhihu_scrapy.items import PeopleItem


class People(object):
    def __init__(self, response):
        self.response = response
        self.item = PeopleItem()
        self.user_url()
        self.avatar_url()
        self.user_name()
        self.gender()
        self.company()
        self.job()
        self.location()
        self.school()
        self.major()
        self.business()
        self.desc()
        self.agrees_num()
        self.thanks_num()
        self.ext()
        self.follow_info()
        self.lives_num()
        self.columns_topics_num()
        self.visited_num()

    def user_url(self):
        xpath_rule = '//a[@class="item home first active"]/@href'
        cur_user_url = self.response.selector.xpath(xpath_rule).extract_first()
        if cur_user_url is None:
            self.item["user_url"] = self.response.url
        else:
            self.item["user_url"] = "".join([settings.PRE_URL, cur_user_url])

    def avatar_url(self):
        xpath_rule = '//*[@class="body clearfix"]//*[@class="Avatar Avatar--l"]/@src'
        _avatar_url = self.response.selector.xpath(xpath_rule).extract_first()
        self.item["avatar_url"] = "".join([_avatar_url[:-6], _avatar_url[-4:]])

    def user_name(self):
        xpath_rule = '//*[@class="body clearfix"]//*[@class="name"]/text()'
        self.item["user_name"] = self.response.selector.xpath(xpath_rule).extract_first()

    def gender(self):
        xpath_rule = '//i[@class="icon icon-profile-male"]'
        if len(self.response.selector.xpath(xpath_rule).extract()) == 1:
            self.item["gender"] = "boy"
        else:
            self.item["gender"] = "girl"

    def company(self):
        xpath_rule = '//span[@class="employment item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["company"] = ""
        else:
            self.item["company"] = a

    def job(self):
        xpath_rule = '//span[@class="position item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["job"] = ""
        else:
            self.item["job"] = a

    def location(self):
        xpath_rule = '//span[@class="location item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["location"] = ""
        else:
            self.item["location"] = a

    def school(self):
        xpath_rule = '//span[@class="education item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["school"] = ""
        else:
            self.item["school"] = a

    def major(self):
        xpath_rule = '//span[@class="education-extra item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["major"] = ""
        else:self.item["major"] = a

    def business(self):
        xpath_rule = '//span[@class="business item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["business"] = ""
        else:
            self.item["business"] = a

    def desc(self):
        xpath_rule = '//div[@class="bio ellipsis"]/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["desc"] = ""
        else:
            self.item["desc"] = a

    def agrees_num(self):
        xpath_rule = '//span[@class="zm-profile-header-user-agree"]/strong/text()'
        self.item["agrees_num"] = int(self.response.selector.xpath(xpath_rule).extract_first())

    def thanks_num(self):
        xpath_rule = '//span[@class="zm-profile-header-user-thanks"]/strong/text()'
        self.item["thanks_num"] = int(self.response.selector.xpath(xpath_rule).extract_first())

    def ext(self):
        xpath_rule = '//div[@class="profile-navbar clearfix"]/a/span[@class="num"]/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        self.item["asks_num"] = int(a[0])
        self.item["answers_num"] = int(a[1])
        self.item["articles_num"] = int(a[2])
        self.item["collections_num"] = int(a[3])
        self.item["edit_num"] = int(a[4])

    def follow_info(self):
        xpath_rule = '//div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        self.item["followees_num"] = int(a[0])
        self.item["followers_num"] = int(a[1])

    def lives_num(self):
        import re
        xpath_rule = '//div[@class="zm-profile-side-section-title lives"]/a/strong/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["lives_num"] = 0
        else:
            pattern = re.compile(r'\d+')
            num = re.findall(pattern, a)
            self.item["lives_num"] = int(num[0])

    def columns_topics_num(self):
        import re
        xpath_rule = '//div[@class="zm-profile-side-section-title"]/a/strong/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        if len(a) == 2:
            cn, tn = a[0], a[1]
            pattern = re.compile(r'\d+')
            _columns_num = re.findall(pattern, cn)
            _topics_num = re.findall(pattern, tn)
            self.item["topics_num"] = int(_topics_num[0])
            self.item["columns_num"] = int(_columns_num[0])
        elif len(a) == 1:
            pattern = re.compile(r'\d+')
            num = re.findall(pattern, a[0])
            if a[0][-2:] in ["话题"]:
                self.item["topics_num"] = int(num[0])
                self.item["columns_num"] = 0
            else:
                self.item["topics_num"] = 0
                self.item["columns_num"] = int(num[0])
        else:
            self.item["topics_num"] = 0
            self.item["columns_num"] = 0

    def visited_num(self):
        xpath_rule = '//div[@class="zm-side-section-inner"]//span[@class="zg-gray-normal"]/strong/text()'
        visited_num = self.response.selector.xpath(xpath_rule).extract_first()
        if visited_num is None:
            self.item["visited_num"] = 0
        else:
            self.item["visited_num"] = int(visited_num)




