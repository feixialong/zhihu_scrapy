# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request, FormRequest

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
        'https://www.zhihu.com/people/stevenjohnson',
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
        # "https://www.zhihu.com/topic/19559424/top-answers",
    ]

    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "https://www.zhihu.com/people/stevenjohnson",
                ],
                # deny=[
                #     "https://www.zhihu.com/people/stevenjohnson/*",
                # ]
            ),
            # todo 使用Rule时，请求应带cookies的问题未解决
            callback="parse_select"
        ),

    ]

    def start_requests(self):
        session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)
        for url in self.start_urls:
            yield Request(
                url=url,
                headers=tools.set_headers(url),
                cookies=tools.unfold_cookies(session.cookies)
            )

    @staticmethod
    def parse_select(response):
        with open("1.html", 'wb') as f:
            f.write(response.body)
        type_ = tools.url_type_select(response.url)
        if type_ in ["not_zhihu"]:
            pass
        elif type_ in ["people"]:
            return people.People(response)
        elif type_ in ["followees"]:
            return followees.Followees(response)
        elif type_ in ["followers"]:
            return followers.Followers(response)
        elif type_ in ["asks"]:
            # todo asks的解析未完成
            return asks.Asks(response)
        elif type_ in ["columns"]:
            # todo columns要抓取的网址与内容均待进一步讨论
            return columns.Columns(response)
        elif type_ in ["topic"]:
            return topics.Topics(response)


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
