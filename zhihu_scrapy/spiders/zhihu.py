# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'https://www.zhihu.com/',
    )

    def start_requests(self):
        from zhihu_scrapy.spiders import login
        username, password = login.read_user_info(login.USER_INFO_FILE)
        session = login.Login().login(username, password)
        yield Request(url=self.start_urls[0], headers=session.headers, cookies=login.unfold_cookies(session.cookies))

    def parse(self, response):
        print(response.url)
        print("")


if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute()
