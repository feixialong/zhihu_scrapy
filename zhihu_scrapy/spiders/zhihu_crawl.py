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
        'https://www.zhihu.com/people/stevenjohnson',
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
        # "https://www.zhihu.com/question/52220142",
        # "https://www.zhihu.com/question/31809134",
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
    ]

    def start_requests(self):
        cookies = tools.unfold_cookies(tools.read_cookie(settings.COOKIES_FILE))
        for url in self.start_urls:
            yield Request(
                url=url,
                headers=tools.set_headers(url),
                cookies=cookies,
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
            people_info = people.People(response).item
            per_page = 10
            followees_times_ = int(people_info["followees_num"] / per_page + 1)
            url_token = people_info["user_url"].split("/")[-1]
            cookies = tools.unfold_cookies(tools.read_cookie(settings.COOKIES_FILE))
            for i in range(followees_times_):
                params = {
                    "include": "data[*].employments,cover_url,allow_message,answer_count,articles_count,favorite_count,follower_count,gender,is_followed,message_thread_token,is_following,badge[?(type=best_answerer)].topics",
                    "per_page": per_page,
                    "offset": per_page * i
                }
                url_ = urllib.parse.urlencode(params)
                headers = settings.MORE_ANSWERS_HEADER
                headers.update({"Authorization": ""})
                yield FormRequest(
                    url="".join([settings.API_URL, "/", url_token, "/followees", "?", url_]),
                    callback=self.parse_followees,
                    headers=headers,
                    method="GET",
                    cookies=cookies
                )
            yield people_info
        elif type_ in ["followees"]:
            print("进入followees")
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
            question = questions.Questions(response).item
            pagesize = 10
            times_ = int(question["answers_num"] / pagesize + 1)
            question["answers"] = []
            for i in range(times_):
                params = {
                    "url_token": question["question_url_token"],
                    "pagesize": pagesize,
                    "offset": pagesize * i
                }
                data = {
                    "method": "next",
                    "params": json.dumps(params)
                }
                yield FormRequest(
                    url=settings.MORE_ANSWERS_URL,
                    body=urllib.parse.urlencode(data),
                    headers=settings.MORE_ANSWERS_HEADER,
                    callback=self.parse_answers,
                    method="POST"
                )
            yield question
        elif type_ in ["for_test"]:  # 用于调试
            pass
        else:
            return "ERROR"

    def parse_answers(self, response):
        for a in json.loads(response.body.decode("utf-8")).get("msg"):
            yield answers.Answers(a).item

    def parse_followees(self, response):
        print(response.url)
        print("")


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
