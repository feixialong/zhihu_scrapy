# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from scrapy.spiders import Spider

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.spiders import login
from zhihu_scrapy.prases import people


class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'https://www.zhihu.com/people/stevenjohnson',
        'https://www.zhihu.com/people/jixin',
        'https://www.zhihu.com/people/chen-li-jie-75',
        "https://www.zhihu.com/people/hydfox"
    )

    def start_requests(self):
        username, password = login.read_user_info(login.USER_INFO_FILE)
        session = login.Login().login(username, password)
        for url in self.start_urls:
            yield Request(url=url,
                          headers=session.headers,
                          cookies=login.unfold_cookies(session.cookies),
                          callback=self.parse_people
                          )

    @staticmethod
    def url_type_select(url):
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

    def parse_people(self, response):
        if self.url_type_select(response.url) not in ["people"]:
            return
        else:
            people_info = people.People(response).item
            yield people_info
            followed_others_url = "".join([people_info["user_url"], settings.FOLLOWED_OTHERS_URL_SUF])
            yield Request(
                url=followed_others_url,
                headers=tools.set_headers(followed_others_url),
                callback=self.parse_followed_others
            )

    def parse_followed_others(self, response):
        pass


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute()
    print("")
