# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from scrapy.spiders import Spider


class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'https://www.zhihu.com/people/stevenjohnson',
        'https://www.zhihu.com/people/jixin',
    )

    def start_requests(self):
        from zhihu_scrapy.spiders import login
        username, password = login.read_user_info(login.USER_INFO_FILE)
        session = login.Login().login(username, password)
        for url in self.start_urls:
            yield Request(url=url, headers=session.headers, cookies=login.unfold_cookies(session.cookies))

    @staticmethod
    def url_type_select(url):
        if url.find("zhihu") == -1:
            return ""
        else:
            url_splited = url.split("/")
            url_splited.reverse()
            types = ["people", "followees", "followers", "asks", "answers", "posts", "collections", "columns", "topics", "answer", "question"]
            for i in url_splited:
                if i in types:
                    return i
                else:
                    pass
            return ""

    def parse(self, response):
        if self.url_type_select(response.url) in ["people"]:
            return self.people_item(response)

    @staticmethod
    def people_item(response):
        from zhihu_scrapy.prases import people
        return people.People(response).item

if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute()
    print("")
