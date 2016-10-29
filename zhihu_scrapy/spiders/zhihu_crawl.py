# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from zhihu_scrapy.prases import asks
from zhihu_scrapy.prases import columns
from zhihu_scrapy.prases import followees
from zhihu_scrapy.prases import followers
from zhihu_scrapy.prases import people
from zhihu_scrapy.prases import topics

from zhihu_scrapy.spiders import login
from zhihu_scrapy import tools
from zhihu_scrapy import settings


class ZhihuSpider(CrawlSpider):
    name = "zhihu_crawl"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        # 'https://www.zhihu.com/people/stevenjohnson',
        # 'https://www.zhihu.com/people/jixin',
        # 'https://www.zhihu.com/people/chen-li-jie-75',
        # "https://www.zhihu.com/people/hydfox",
        # "https://www.zhihu.com/people/jixin/followees",
        # "https://www.zhihu.com/people/mei-ying-0829/followees",
        # "https://www.zhihu.com/people/shuaizhu/followees",
        # "https://www.zhihu.com/people/chen-fan-85/followers",
        # "https://zhuanlan.zhihu.com/pythoner",
        # "https://zhuanlan.zhihu.com/api/columns/pythoner",
        # "https://zhuanlan.zhihu.com/api/columns/LaTeX",
        "https://www.zhihu.com/topic/19559424/top-answers",
    ]

    rules = [
        Rule(LinkExtractor(
            allow=("https://www.zhihu.com/people/stevenjohnson",),
            deny=("https://www.zhihu.com/people/stevenjohnson/*")),
            follow=False
        )
    ]

    @classmethod
    def url_type_select(cls, url):
        if url is not None:
            if url.find("zhihu") == -1:
                return ""
            else:
                url_splited = url.split("/")
                url_splited.reverse()
                types = [
                    "people",
                    "followees",
                    "followers",
                    "asks",
                    "answers",
                    "posts",
                    "collections",
                    "columns",
                    "topic",
                    "answer",
                    "question"
                ]
                for i in url_splited:
                    if i in types:
                        return i
                    else:
                        pass
                return "columns"

    def start_requests(self):
        session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)
        for url in self.start_urls:
            yield Request(
                url=url,
                headers=tools.set_headers(url),
                cookies=tools.unfold_cookies(session.cookies),
                callback=self.method_select
            )

    def method_select(self, response):
        type_ = self.url_type_select(response.url)
        if type_ in ["people"]:
            return self.parse_people(response)
        elif type_ in ["followees"]:
            return self.parse_followees(response)
        elif type_ in ["followers"]:
            return self.parse_followers(response)
        elif type_ in ["asks"]:
            # todo asks的解析未完成
            return self.parse_asks(response)
        elif type_ in ["columns"]:
            # todo columns要抓取的网址与内容均待进一步讨论
            return self.parse_columns(response)
        elif type_ in ["topic"]:
            return self.parse_topics(response)

    def parse_people(self, response):
        people_ = people.People(response)
        print(people_.item)

    def parse_followees(self, response):
        followees_ = followees.Followees(response)
        print(followees_.item)

    def parse_followers(self, response):
        followers_ = followers.Followers(response)
        print(followers_.item)

    def parse_asks(self, response):
        asks_ = asks.Asks(response)
        print(asks_.item)

    def parse_columns(self, response):
        columns_ = columns.Columns(response)
        print(columns_.item)

    def parse_topics(self, response):
        topics_ = topics.Topics(response)
        print(topics_.item)


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
