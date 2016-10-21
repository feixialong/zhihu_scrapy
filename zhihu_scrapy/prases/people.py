# -*- coding: utf-8 -*-


class People(object):
    def __init__(self, response):
        self.response = response
        self.item = self.init_item()
        # self.user_url()
        # self.avatar_url()
        # self.user_name()
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
        self.followe_info()
        self.lives_num()
        self.columns_topics_num()
        self.visited_num()

    @staticmethod
    def init_item():
        from zhihu_scrapy.items import ZhihuScrapyItem
        return ZhihuScrapyItem()

    def user_url(self):
        self.item["user_url"] = self.response.url

    def avatar_url(self):
        xpath_rule = '//*[@class="body clearfix"]//*[@class="Avatar Avatar--l"]/@src'
        _avatar_url = self.response.selector.xpath(xpath_rule).extract()[0]
        self.item["avatar_url"] = "".join([_avatar_url[:-6], _avatar_url[-4:]])

    def user_name(self):
        xpath_rule = '//*[@class="body clearfix"]//*[@class="name"]/text()'
        self.item["user_name"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def company(self):
        xpath_rule = '//span[@class="employment item"]/a/text()'
        try:
            self.item["company"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["company"] = ""

    def job(self):
        xpath_rule = '//span[@class="position item"]/a/text()'
        try:
            self.item["job"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["job"] = ""

    def location(self):
        xpath_rule = '//span[@class="location item"]/a/text()'
        try:
            self.item["location"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["location"] = ""

    def school(self):
        xpath_rule = '//span[@class="education item"]/a/text()'
        try:
            self.item["school"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["school"] = ""

    def major(self):
        xpath_rule = '//span[@class="education-extra item"]/a/text()'
        try:
            self.item["major"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["major"] = ""

    def business(self):
        xpath_rule = '//span[@class="business item"]/a/text()'
        try:
            self.item["business"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["business"] = ""

    def desc(self):
        xpath_rule = '//div[@class="bio ellipsis"]/text()'
        try:
            self.item["desc"] = self.response.selector.xpath(xpath_rule).extract()[0]
        except:
            self.item["desc"] = ""

    def agrees_num(self):
        xpath_rule = '//span[@class="zm-profile-header-user-agree"]/strong/text()'
        self.item["agrees_num"] = int(self.response.selector.xpath(xpath_rule).extract()[0])

    def thanks_num(self):
        xpath_rule = '//span[@class="zm-profile-header-user-thanks"]/strong/text()'
        self.item["thanks_num"] = int(self.response.selector.xpath(xpath_rule).extract()[0])

    def ext(self):
        xpath_rule = '//div[@class="profile-navbar clearfix"]/a/span[@class="num"]/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        self.item["asks_num"] = int(a[0])
        self.item["answers_num"] = int(a[1])
        self.item["articles_num"] = int(a[2])
        self.item["collections_num"] = int(a[3])
        self.item["edit_num"] = int(a[4])

    def followe_info(self):
        xpath_rule = '//div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()'
        a = self.response.selector.xpath(xpath_rule).extract()
        self.item["followed_others_num"] = int(a[0])
        self.item["be_followed_num"] = int(a[1])

    def lives_num(self):
        import re
        xpath_rule = '//div[@class="zm-profile-side-section-title lives"]/a/strong/text()'
        try:
            a = self.response.selector.xpath(xpath_rule).extract()[0]
            pattern = re.compile(r'\d+')
            num = re.findall(pattern, a)
            self.item["lives_num"] = int(num[0])
        except:
            self.item["lives_num"] = 0

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
        try:
            visited_num = self.response.selector.xpath(xpath_rule).extract()[0]
            self.item["visited_num"] = int(visited_num)
        except:
            self.item["visited_num"] = 0



