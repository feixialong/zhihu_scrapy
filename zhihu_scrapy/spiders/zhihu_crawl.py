# -*- coding: utf-8 -*-

import json
import requests
import urllib.parse
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.http import FormRequest

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from zhihu_scrapy.prases import answers
from zhihu_scrapy.prases import articles
from zhihu_scrapy.prases import columns
from zhihu_scrapy.prases import followees
from zhihu_scrapy.prases import followers
from zhihu_scrapy.prases import people
from zhihu_scrapy.prases import questions
from zhihu_scrapy.prases import topics

from zhihu_scrapy.spiders import login
from zhihu_scrapy import tools
from zhihu_scrapy import settings


class ZhihuSpider(CrawlSpider):
    name = "zhihu_crawl"
    allowed_domains = ["zhihu.com"]
    session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)

    start_urls = [
        # 'https://www.zhihu.com/people/stevenjohnson',
        # 'https://www.zhihu.com/people/jixin',
        # 'https://www.zhihu.com/people/chen-li-jie-75',
        # "https://www.zhihu.com/people/hydfox",
        # "https://www.zhihu.com/people/jixin/followees",
        # "https://www.zhihu.com/people/mei-ying-0829/followees",
        # "https://www.zhihu.com/people/shuaizhu/followees",
        # "https://www.zhihu.com/people/chen-fan-85/followers",
        # "https://zhuanlan.zhihu.com/pythoner",  # 此种网址未进行解析
        # "https://zhuanlan.zhihu.com/api/columns/pythoner",
        # "https://zhuanlan.zhihu.com/api/columns/LaTeX",
        # "https://www.zhihu.com/topic/19559424/top-answers",
        # "https://zhuanlan.zhihu.com/p/22947665",
        # "https://zhuanlan.zhihu.com/p/23250032",
        # "https://zhuanlan.zhihu.com/api/posts/23190728",
        "https://www.zhihu.com/question/52220142"
        # "https://www.zhihu.com/node/QuestionAnswerListV2"
    ]

    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "https://www.zhihu.com/people/.+",
                    "https://zhuanlan.zhihu.com/api/columns/.+",
                    "https://www.zhihu.com/topic/.+",
                    "https://zhuanlan.zhihu.com/p/*",
                ],
                deny=[
                    "https://www.zhihu.com/logout",
                    "https://www.zhihu.com/*",  # 不允许追踪任何链接，用于调试
                ]
            ),
            process_links="process_links_",  # 传入links列表，返回links列表
            process_request="process_request_",  # 传入Request，每次一个，返回Request，每次一个
            callback="parse_start_url",  # 传入response，返回经过parse的item
        ),

        # Rule(
        #     LinkExtractor(
        #         allow=[
        #             "https://www.zhihu.com/node/QuestionAnswerListV2"
        #         ],
        #         deny=[
        #             "https://www.zhihu.com/*"
        #         ]
        #     ),
        #     process_links="process_links_",  # 传入links列表，返回links列表
        #     process_request="process_request_",  # 传入Request，每次一个，返回Request，每次一个
        #     callback="get_answers" ,  # 传入response，返回经过parse的item
        # )

    ]

    def start_requests(self):
        for url in self.start_urls:
            if tools.url_type_select(url) in ["answers"]:
                # todo 答案请求的参数设置，每个答案返回给解析处后的处理方式
                params = {
                    "url_token": 47871877,
                    "pagesize": 10,
                    "offset": 10
                }
                url = "https://www.zhihu.com/node/QuestionAnswerListV2"

                data = {
                    "method": "next",
                    "params": json.dumps(params),  # 这样做能得到正确的返回结果
                }
                yield FormRequest(
                    url=url,
                    body=urllib.parse.urlencode(data),
                    headers=settings.MORE_ANSWERS_HEADER,
                    method="POST",
                )
            else:
                yield Request(
                    url=url,
                    headers=tools.set_headers(url),
                    # cookies=tools.unfold_cookies(self.session.cookies),
                    cookies=tools.unfold_cookies(tools.read_cookie(settings.COOKIES_FILE)),
                    meta={'cookiejar': 1}
                )

    def process_links_(self, links):
        """
        在Rule()获取到了各种links列表后，用此方法对其进行处理，
        :param links: Rule()获取到的links列表
        :return: 经过中间处理后的links列表
        """
        # todo 对links还未处理，会出现错误，待将每个信息的parse完成后再对此部分进行更新
        return links

    def process_request_(self, request):
        """
        在Rule()获取到的request，用此方法对其进行处理，
        :param request: Rule()获取到的request，每次只传入一个
        :return: 经过中间处理后的request，每次只返回一个
        """
        request = request.replace(**{"cookies": tools.unfold_cookies(self.session.cookies)})
        request = request.replace(**{"headers": tools.set_headers(request.url)})
        return request

    def parse_start_url(self, response):
        type_ = tools.url_type_select(response.url)
        if type_ in ["not_zhihu"]:
            pass
        elif type_ in ["people"]:
            return people.People(response).item
        elif type_ in ["followees"]:
            return followees.Followees(response).item
        elif type_ in ["followers"]:
            return followers.Followers(response).item
        elif type_ in ["columns"]:
            # todo columns要抓取的网址与内容均待进一步讨论
            return columns.Columns(response).item
        elif type_ in ["topic"]:
            return topics.Topics(response).item
        elif type_ in ["articles"]:
            return articles.Articles(response).item
        elif type_ in ["questions"]:
            return questions.Questions(response).item
        elif type_ in ["answers"]:
            return answers.Answers(response).item
        elif type_ in ["for_test"]:  # 用于调试
            pass
        else:
            return "ERROR"


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
