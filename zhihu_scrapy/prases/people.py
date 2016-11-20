# -*- coding: utf-8 -*-

from zhihu_scrapy import settings
from zhihu_scrapy.items import PeopleItem
import re


class People(object):
    def __init__(self, response):
        self.response = response
        self.item = PeopleItem()
        self.item["data_type"] = "people"
        self.new = self.is_new()
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
        self.is_best_answerer()
        self.is_identity()
        self.hash_id()
        self._xsrf()

    def is_new(self):
        xpath_rule = '//div[@id="ProfileHeader"]'
        result = self.response.selector.xpath(xpath_rule).extract_first()
        # 不为None则为新的主页，为None则为旧主页
        if result:
            return True
        else:
            return False

    def user_url(self):
        if self.new is True:
            self.item["user_url"] = self.response.url
        else:
            xpath_rule = '//a[@class="item home first active"]/@href'
            cur_user_url = self.response.selector.xpath(xpath_rule).extract_first()
            if cur_user_url is None:
                self.item["user_url"] = self.response.url
            else:
                self.item["user_url"] = "".join([settings.BASE_URL, cur_user_url])

    def avatar_url(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-main"]//img/@src'
            _avatar_url = self.response.selector.xpath(xpath_rule).extract_first()
            self.item["avatar_url"] = "".join([_avatar_url[:-7], _avatar_url[-4:]])
        else:
            xpath_rule = '//*[@class="Avatar Avatar--l"]/@src'
            _avatar_url = self.response.selector.xpath(xpath_rule).extract_first()
            self.item["avatar_url"] = "".join([_avatar_url[:-6], _avatar_url[-4:]])

    def user_name(self):
        if self.new is True:
            xpath_rule = '//span[@class="ProfileHeader-name"]/text()'
            self.item["user_name"] = self.response.selector.xpath(xpath_rule).extract_first()
        else:
            xpath_rule = '//*[@class="body clearfix"]//*[@class="name"]/text()'
            self.item["user_name"] = self.response.selector.xpath(xpath_rule).extract_first()

    def gender(self):
        if self.new is True:
            xpath_rule = '//*[@class="Icon Icon--male"]'
        else:
            xpath_rule = '//i[@class="icon icon-profile-male"]'

        if len(self.response.selector.xpath(xpath_rule).extract()) == 1:
            self.item["gender"] = "boy"
        else:
            self.item["gender"] = "girl"

    def company(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][2]/text()[1]'
        else:
            xpath_rule = '//span[@class="employment item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["company"] = ""
        else:
            self.item["company"] = a

    def job(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][2]/text()[2]'
            a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                self.item["job"] = ""
            else:
                self.item["job"] = a
        else:
            xpath_rule = '//span[@class="position item"]/a/text()'
            a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                # 同样是旧版的个人主页，不同人的xpath_rule不同，真尼玛坑
                xpath_rule = '//span[@class="position item"]/text()'
                a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                self.item["job"] = ""
            else:
                self.item["job"] = a

    def location(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][1]/text()[1]'
        else:
            xpath_rule = '//span[@class="location item"]/a/text()'

        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["location"] = ""
        else:
            self.item["location"] = a

    def school(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][3]/text()[1]'
        else:
            xpath_rule = '//span[@class="education item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["school"] = ""
        else:
            self.item["school"] = a

    def major(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][3]/text()[2]'
        else:
            xpath_rule = '//span[@class="education-extra item"]/a/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["major"] = ""
        else:self.item["major"] = a

    def business(self):
        if self.new is True:
            xpath_rule = '//div[@class="ProfileHeader-info"]/div[@class="ProfileHeader-infoItem"][1]/text()[2]'
            a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                self.item["business"] = ""
            else:
                self.item["business"] = a
        else:
            xpath_rule = '//span[@class="business item"]/a/text()'
            a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                # 同样是旧版的个人主页，不同人的xpath_rule不同，真尼玛坑
                xpath_rule = '//span[@class="business item"]/text()'
                a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                self.item["business"] = ""
            else:
                self.item["business"] = a

    def desc(self):
        if self.new is True:
            xpath_rule = '//span[@class="RichText ProfileHeader-headline"]/text()'
        else:
            xpath_rule = '//div[@class="bio ellipsis"]/text()'
        a = self.response.selector.xpath(xpath_rule).extract_first()
        if a is None:
            self.item["desc"] = ""
        else:
            self.item["desc"] = a

    def agrees_num(self):
        if self.new is True:
            xpath_rule = '//div[@class="IconGraf"]/text()'
            results = self.response.selector.xpath(xpath_rule).extract()
            self.item["agrees_num"] = 0
            for result in results:
                if not (result.find("赞同") == -1):
                    pattern = re.compile(r'\d+')
                    self.item["agrees_num"] = int(re.findall(pattern, result)[0])
        else:
            xpath_rule = '//span[@class="zm-profile-header-user-agree"]/strong/text()'
            self.item["agrees_num"] = int(self.response.selector.xpath(xpath_rule).extract_first())

    def thanks_num(self):
        if self.new is True:
            xpath_rule = '//div[@class="Profile-sideColumnItemValue"]/text()'
            results = self.response.selector.xpath(xpath_rule).extract()
            self.item["thanks_num"] = 0
            for result in results:
                if not (result.find("感谢") == -1):
                    pattern = re.compile(r'\d+')
                    self.item["thanks_num"] = int(re.findall(pattern, result)[0])
        else:
            xpath_rule = '//span[@class="zm-profile-header-user-thanks"]/strong/text()'
            self.item["thanks_num"] = int(self.response.selector.xpath(xpath_rule).extract_first())

    def ext(self):
        if self.new is True:
            xpath_rule = '//ul[@class="Tabs ProfileMain-tabs"]/li/a/span[@class="Tabs-meta"]/text()'
            a = self.response.selector.xpath(xpath_rule).extract()
            self.item["answers_num"] = int(a[0])
            self.item["articles_num"] = int(a[1])
            self.item["asks_num"] = int(a[2])
            self.item["collections_num"] = int(a[3])

            xpath_rule = '//div[@class="IconGraf"]/text()'
            results = self.response.selector.xpath(xpath_rule).extract()
            self.item["public_edit_num"] = 0
            for result in results:
                if not (result.find("编辑") == -1):
                    pattern = re.compile(r'\d+')
                    self.item["public_edit_num"] = int(re.findall(pattern, result)[0])
        else:
            xpath_rule = '//div[@class="profile-navbar clearfix"]/a/span[@class="num"]/text()'
            a = self.response.selector.xpath(xpath_rule).extract()
            self.item["asks_num"] = int(a[0])
            self.item["answers_num"] = int(a[1])
            self.item["articles_num"] = int(a[2])
            self.item["collections_num"] = int(a[3])
            self.item["public_edit_num"] = int(a[4])

    def follow_info(self):
        if self.new is True:
            xpath_rule = '//div[@class="Profile-followStatusValue"]/text()'
        else:
            xpath_rule = '//div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        self.item["followees_num"] = int(a[0])
        self.item["followers_num"] = int(a[1])

    def lives_num(self):
        if self.new is True:
            xpath_rule = '//a[@class="Profile-lightItem"]/span[@class="Profile-lightItemValue"]/text()'
            a = self.response.selector.xpath(xpath_rule).extract()
            self.item["lives_num"] = int(a[0])
        else:
            xpath_rule = '//div[@class="zm-profile-side-section-title lives"]/a/strong/text()'
            a = self.response.selector.xpath(xpath_rule).extract_first()
            if a is None:
                self.item["lives_num"] = 0
            else:
                pattern = re.compile(r'\d+')
                num = re.findall(pattern, a)
                self.item["lives_num"] = int(num[0])

    def columns_topics_num(self):
        if self.new is True:
            xpath_rule = '//a[@class="Profile-lightItem"]/span[@class="Profile-lightItemValue"]/text()'
            a = self.response.selector.xpath(xpath_rule).extract()
            self.item["topics_num"] = int(a[1])
            self.item["columns_num"] = int(a[2])
        else:
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
        if self.new is True:
            pass
        else:
            xpath_rule = '//div[@class="zm-side-section-inner"]//span[@class="zg-gray-normal"]/strong/text()'
            visited_num = self.response.selector.xpath(xpath_rule).extract_first()
            if visited_num is None:
                self.item["visited_num"] = 0
            else:
                self.item["visited_num"] = int(visited_num)

    def is_best_answerer(self):
        if self.new is True:
            xpath_rule = '//div[@class="IconGraf"]/text()'
            results = self.response.selector.xpath(xpath_rule).extract()
            self.item["is_best_answerer"] = False
            for result in results:
                if not (result.find("优秀") == -1):
                    self.item["is_best_answerer"] = True
        else:
            xpath_rule = '//*[@class="icon icon-badge-best_answerer"]'
            results = self.response.selector.xpath(xpath_rule).extract()
            if results:
                self.item["is_best_answerer"] = True

    def is_identity(self):
        if self.new is True:
            xpath_rule = '//div[@class="IconGraf"]/text()'
            results = self.response.selector.xpath(xpath_rule).extract()
            self.item["is_identity"] = False
            for result in results:
                if not (result.find("认证") == -1):
                    self.item["is_identity"] = True
        else:
            xpath_rule = '//*[@class="icon icon-badge-identity"]'
            results = self.response.selector.xpath(xpath_rule).extract()
            if results:
                self.item["is_identity"] = True

    def hash_id(self):
        xpath_rule = '//div[@class="zm-profile-header-op-btns clearfix"]/button/@data-id'
        self.item["hash_id"] = self.response.selector.xpath(xpath_rule).extract_first()

    def _xsrf(self):
        xpath_rule = '//input[@name="_xsrf"]/@value'
        self.item["_xsrf"] = self.response.selector.xpath(xpath_rule).extract_first()
