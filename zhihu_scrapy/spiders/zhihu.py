# -*- coding: utf-8 -*-

import json

from scrapy import Request
from scrapy.spiders import Spider

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.prases import followees
from zhihu_scrapy.prases import people
from zhihu_scrapy.spiders import login


class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        # 'https://www.zhihu.com/people/stevenjohnson',
        # 'https://www.zhihu.com/people/jixin',
        # 'https://www.zhihu.com/people/chen-li-jie-75',
        # "https://www.zhihu.com/people/hydfox",
        # "https://www.zhihu.com/people/jixin/followees"
        # "https://www.zhihu.com/people/mei-ying-0829/followees",
        "https://www.zhihu.com/people/shuaizhu/followees"
    ]

    def start_requests(self):
        username, password = login.read_user_info(login.USER_INFO_FILE)
        session = login.Login().login(username, password)
        for url in self.start_urls:
            yield Request(url=url,
                          headers=session.headers,
                          cookies=login.unfold_cookies(session.cookies)
                          # callback=self.parse_people
                          )

    @classmethod
    def url_type_select(cls, url):
        if url.find("zhihu") == -1:
            return ""
        else:
            url_splited = url.split("/")
            url_splited.reverse()
            types = ["people", "followees", "followers", "asks", "answers", "posts", "collections", "columns", "topics",
                     "answer", "question"]
            for i in url_splited:
                if i in types:
                    return i
                else:
                    pass
            return ""

    def parse(self, response):  # 通过parse()分发解析去向
        _type = self.url_type_select(response.url)
        if _type in ["people"]:
            return self.parse_people(response)
        elif _type in ["followees"]:
            return self.parse_followees(response)

    @classmethod
    def parse_people(cls, response):
        people_info = people.People(response).item
        yield people_info
        followee_url = "".join([people_info["user_url"], settings.FOLLOWEE_URL_SUF])
        yield Request(
            url=followee_url,
            headers=tools.set_headers(followee_url)
        )

    @classmethod
    def parse_followees(cls, response):
        followees_info = followees.Followees(response).item
        yield followees_info

if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute()
    print("")
