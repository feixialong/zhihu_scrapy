# -*- coding: utf-8 -*-


from scrapy import Request
from scrapy.spiders import Spider

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.prases import followees
from zhihu_scrapy.prases import people
from zhihu_scrapy.spiders import login


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


class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        'https://www.zhihu.com/people/stevenjohnson',
        # 'https://www.zhihu.com/people/jixin',
        # 'https://www.zhihu.com/people/chen-li-jie-75',
        # "https://www.zhihu.com/people/hydfox",
        # "https://www.zhihu.com/people/jixin/followees"
        # "https://www.zhihu.com/people/mei-ying-0829/followees",
        # "https://www.zhihu.com/people/shuaizhu/followees"
    ]

    def start_requests(self):
        session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)
        for url in self.start_urls:
            yield Request(
                url=url,
                headers=settings.DEDAULT_HEADERS,
                cookies=tools.unfold_cookies(session.cookies)
            )

    def parse(self, response):  # 通过parse()分发解析去向
        _type = url_type_select(response.url)
        if _type in ["people"]:
            return people.People(response).item
        elif _type in ["followees"]:
            return followees.Followees(response).item


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute()
    print("")
