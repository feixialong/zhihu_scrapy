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

from zhihu_scrapy.prases import columns
from zhihu_scrapy.prases import column_articles
from zhihu_scrapy.prases import column_followers
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
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]
    session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)

    start_urls = [
        "https://www.zhihu.com",
        'https://www.zhihu.com/people/stevenjohnson',
        "https://www.zhihu.com/people/wang-you-28",  # 新主页
        "https://www.zhihu.com/people/patrickluo/",
        'https://www.zhihu.com/people/jixin',
        'https://www.zhihu.com/people/chen-li-jie-75',
        "https://www.zhihu.com/people/hydfox",
        # "https://www.zhihu.com/people/jixin/followees",
        # "https://www.zhihu.com/people/mei-ying-0829/followees",
        # "https://www.zhihu.com/people/shuaizhu/followees",
        # "https://www.zhihu.com/people/chen-fan-85/followers",
        # "https://zhuanlan.zhihu.com/pythoner",  # 此种网址未进行解析，获取到此种网络后，应转成下方的网址形式
        # "https://zhuanlan.zhihu.com/api/columns/pythoner",
        # "https://zhuanlan.zhihu.com/api/columns/LaTeX",
        # "https://www.zhihu.com/topic/19559424/top-answers",
        # "https://zhuanlan.zhihu.com/p/22947665",
        # "https://zhuanlan.zhihu.com/p/23250032",
        # "https://zhuanlan.zhihu.com/api/posts/23190728",
        "https://www.zhihu.com/question/52220142",
        "https://www.zhihu.com/question/31809134",
        "https://www.zhihu.com/question/19581624",
        "https://www.zhihu.com/question/24565276",
        # "https://www.zhihu.com/node/QuestionAnswerListV2"
    ]

    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    "https://www.zhihu.com/people/.+",
                    "https://www.zhihu.com/.+",
                    "https://zhuanlan.zhihu.com/api/columns/.+",
                    "https://www.zhihu.com/topic/.+",
                    "https://zhuanlan.zhihu.com/p/.+",
                    "https://zhuanlan.zhihu.com/.+",
                    "https://www.zhihu.com/question/\d+",
                    "http://www.zhihu.com/people/.+",
                    "http://www.zhihu.com/.+",
                    "http://zhuanlan.zhihu.com/api/columns/.+",
                    "http://www.zhihu.com/topic/.+",
                    "http://zhuanlan.zhihu.com/p/.+",
                    "http://zhuanlan.zhihu.com/.+",
                    "http://www.zhihu.com/question/\d+"
                ],
                deny=[
                    "https://www.zhihu.com/logout",
                    "https://zhuanlan.zhihu.com/write",
                    "https://www.zhihu.com/question/invited",
                    "https://www.zhihu.com/question/following",
                    # "https://www.zhihu.com/*",  # 不允许追踪任何链接，用于调试
                ],
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
        new_links = []
        for link in links:
            type_ = tools.url_type_select(link.url)
            if type_ in ["articles_"]:
                # 对 "https://zhuanlan.zhihu.com/p/23250032" 此类网址的处理
                article_url_token = link.url.split("/")[-1]
                link_url = "".join(["https://zhuanlan.zhihu.com/api/posts/", article_url_token])
                link.url = link_url
                new_links.append(link)
            elif type_ in ["columns"]:
                # 对 "https://zhuanlan.zhihu.com/pythoner" 此类网址的处理
                article_url_token = link.url.split("/")[-1]
                link_url = "".join(["https://zhuanlan.zhihu.com/api/columns/", article_url_token])
                link.url = link_url
                new_links.append(link)
            elif type_ in ["single_answer"]:
                link.url = link.url.split("answer")[0]
                new_links.append(link)
            elif type_ in ["people_home", "people_questions", "people_answers", "people_articles", "people_collections",
                           "topic", "columns_api", "articles", "questions"]:
                new_links.append(link)
            else:
                pass
        for link in new_links:
            # 去除网址末尾的"/"
            if link.url[-1] == "/":
                link.url = link.url[:-1]
            else:
                pass
        return new_links

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
        print("开始解析: {url}".format(url=response.url))
        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            yield response.request
        type_ = tools.url_type_select(response.url)
        if type_ in ["not_zhihu"]:
            pass
        elif type_ in ["home"]:
            pass
        elif type_ in ["questions"]:
            # ---- 以下为对问题信息的抓取 ----
            question_info = questions.Questions(response).item
            yield question_info

            # ---- 以下为对该问题下的答案的抓取 ----
            # pagesize = 10
            # times_ = int(question_info["answers_num"] / pagesize + 1)
            # for i in range(times_):
            #     params = {
            #         "url_token": question_info["question_url_token"],
            #         "pagesize": pagesize,
            #         "offset": pagesize * i
            #     }
            #     data = {
            #         "method": "next",
            #         "params": json.dumps(params)
            #     }
            #     yield FormRequest(
            #         url=settings.MORE_ANSWERS_URL,
            #         body=urllib.parse.urlencode(data),
            #         headers=tools.set_headers(question_info["question_url"]),
            #         callback=self.parse_answers,
            #         method="POST"
            #     )

        elif type_ in ["columns_api"]:
            # todo columns要抓取的网址与内容均待进一步讨论
            # ---- 以下为对专栏信息的抓取 ----
            columns_info = columns.Columns(response).item
            yield columns_info

            # ---- 以下为对专栏中关注者的抓取 ----
            # todo 仅能抓取，但是没法与对应的专栏关联起来；同时耗费太多请求次数，对后续分析又没多大帮助，故将其注释，爬取时先不请求
            # limit = 20
            # offset = 0
            # times_ = int(columns_info["followers_num"] / limit + 1)
            # column_followers_api_url = "".join([columns_info["api_url"], "/followers"])
            # for i in range(times_):
            #     params = {
            #         "limit": limit,
            #         "offset": offset
            #     }
            #     offset += limit
            #     yield FormRequest(
            #         url="".join([column_followers_api_url, "?", urllib.parse.urlencode(params)]),
            #         headers=settings.MORE_ANSWERS_HEADER,
            #         callback=self.parse_column_followers,
            #         method="GET"
            #     )

            # -----  以下为对专栏中的文章的抓取 ----
            # https://zhuanlan.zhihu.com/api/columns/pythoner/posts?limit=20
            limit = 20
            offset = 0
            times_ = int(columns_info["articles_num"] / limit + 1)
            column_articles_api_url = "".join([columns_info["api_url"], "/posts"])
            for i in range(times_):
                params = {
                    "limit": limit,
                    "offset": offset
                }
                offset += limit
                yield FormRequest(
                    url="".join([column_articles_api_url, "?", urllib.parse.urlencode(params)]),
                    headers=settings.MORE_ANSWERS_HEADER,
                    callback=self.parse_column_articles,
                    method="GET"
                )

        elif type_ in ["articles"]:
            # ---- 以下为对普通文章的抓取 ----
            body = json.loads(response.body.decode("utf-8"))
            yield column_articles.ColumnArticles(body).item

        elif type_ in ["people_home"]:
            # ---- 以下为对个人信息的抓取 ----
            people_info = people.People(response).item
            yield people_info

            # ---- 以下对该人关注的用户的抓取， 未完成----
            # todo 对该人关注的用户的抓取未完成
            # offset = 20
            # times_ = int(people_info["followees_num"] / offset + 1)
            # for i in range(times_):
            #     params = {
            #         "hash_id": people_info["hash_id"],
            #         "order_by": "created",
            #         "offset": offset * i
            #     }
            #     data = {
            #         "method": "next",
            #         "params": json.dumps(params),
            #         # "_xsrf": people_info["_xsrf"]
            #     }
            #     body = urllib.parse.urlencode(data)
            #     yield FormRequest(
            #         url=settings.MORE_FOLLOWERS_URL,
            #         body=urllib.parse.urlencode(data),
            #         headers=settings.MORE_ANSWERS_HEADER,
            #         callback=self.parse_people_followers,
            #         method="POST",
            #         cookies=tools.unfold_cookies(tools.read_cookie(settings.COOKIES_FILE))
            #     )

        elif type_ in ["for_test"]:  # 用于调试
            pass
        else:
            return "ERROR"

    def parse_answers(self, response):
        for a in json.loads(response.body.decode("utf-8")).get("msg"):
            yield answers.Answers(a).item

    def parse_column_articles(self, response):
        bodys = json.loads(response.body.decode("utf-8"))
        for body in bodys:
            yield column_articles.ColumnArticles(body).item

    def parse_column_followers(self, response):
        bodys = json.loads(response.body.decode("utf-8"))
        for body in bodys:
            yield column_followers.ColumnFollowers(body).item

    def parse_people_followers(self, response):
        print(response.url)
        print("")


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute("scrapy crawl zhihu_crawl".split())
    print("")
