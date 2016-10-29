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
                # allow=[
                #     "https://www.zhihu.com/people/stevenjohnson",
                # ],
                deny=[
                    " https://www.zhihu.com/logout",
                ]
            ),
            # todo 使用Rule时，请求应带cookies的问题未解决
            process_links="process_links_",  # 传入links列表
            process_request="process_request_",  # 传入request，每次一个
            callback="callback_",  # 传入response

        ),

    ]

    session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)

    def start_requests(self):
        for url in self.start_urls:
            yield self.get_response_from_url(url)

    def get_response_from_url(self, url):
        print("请求{url}中...".format(url=url))
        return Request(
            url=url,
            headers=tools.set_headers(url),
            cookies=tools.unfold_cookies(self.session.cookies)
        )

    def process_links_(self, links):
        """
        在Rule()获取到了各种links列表后，用此方法对其进行处理，
        :param links: Rule()获取到的links列表
        :return: 经过中间处理后的links列表
        """
        print("运行到了process_links_")
        print(links)
        print("")
        return links

    def process_request_(self, request):
        """
        在Rule()获取到的request，用此方法对其进行处理，
        :param requests: Rule()获取到的request，每次只传入一个
        :return: 经过中间处理后的request，每次只返回一个
        """
        request.headers = tools.set_headers(request.url)
        request.cookies = self.session.cookies
        print("运行到了process_request")
        a = request
        print(a)
        print("")
        return a

    def callback_(self, response):
        print("运行到了callback_")
        a = response
        print(response)
        print("")
        return response

    def parse_start_url(self, response):
        with open("1.html", 'wb') as f:
            f.write(response.body)
        type_ = tools.url_type_select(response.url)
        if type_ in ["not_zhihu"]:
            pass
        elif type_ in ["people"]:
            return people.People(response).item
        elif type_ in ["followees"]:
            return followees.Followees(response).item
        elif type_ in ["followers"]:
            return followers.Followers(response).item
        elif type_ in ["asks"]:
            # todo asks的解析未完成
            return asks.Asks(response).item
        elif type_ in ["columns"]:
            # todo columns要抓取的网址与内容均待进一步讨论
            return columns.Columns(response).item
        elif type_ in ["topic"]:
            return topics.Topics(response).item


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
