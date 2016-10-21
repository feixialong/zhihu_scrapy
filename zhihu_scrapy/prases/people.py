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
        self.item["company"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def job(self):
        xpath_rule = '//span[@class="position item"]/a/text()'
        self.item["job"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def location(self):
        xpath_rule = '//span[@class="location item"]/a/text()'
        self.item["location"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def school(self):
        xpath_rule = '//span[@class="education item"]/a/text()'
        self.item["school"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def major(self):
        xpath_rule = '//span[@class="education-extra item"]/a/text()'
        self.item["major"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def business(self):
        xpath_rule = '//span[@class="business item"]/a/text()'
        self.item["business"] = self.response.selector.xpath(xpath_rule).extract()[0]

    def desc(self):
        xpath_rule = '//div[@class="bio ellipsis"]/text()'
        self.item["desc"] = self.response.selector.xpath(xpath_rule).extract()[0]

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
        a = self.response.selector.xpath(xpath_rule).extract()[0]
        pattern = re.compile(r'\d+')
        num = re.findall(pattern, a)
        self.item["lives_num"] = int(num[0])

    def columns_topics_num(self):
        import re
        xpath_rule = '//div[@class="zm-profile-side-section-title"]/a/strong/text()'
        cn, tn = self.response.selector.xpath(xpath_rule).extract()
        pattern = re.compile(r'\d+')
        _columns_num = re.findall(pattern, cn)
        _topics_num = re.findall(pattern, tn)
        self.item["topics_num"] = int(_topics_num[0])
        self.item["columns_num"] = int(_columns_num[0])

    def visited_num(self):
        xpath_rule = '//div[@class="zm-side-section-inner"]//span[@class="zg-gray-normal"]/strong/text()'
        visited_num = self.response.selector.xpath(xpath_rule).extract()[0]
        self.item["visited_num"] = int(visited_num)



