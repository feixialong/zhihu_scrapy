# -*- coding: utf-8 -*-


from scrapy import Request
from scrapy.spiders import Spider

from zhihu_scrapy import settings
from zhihu_scrapy import tools
from zhihu_scrapy.prases import asks
from zhihu_scrapy.prases import columns
from zhihu_scrapy.prases import followees
from zhihu_scrapy.prases import followers
from zhihu_scrapy.prases import people
from zhihu_scrapy.prases import topics
from zhihu_scrapy.spiders import login


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
        # "https://www.zhihu.com/people/shuaizhu/followees",
        # "https://www.zhihu.com/people/chen-fan-85/followers",
        # "https://zhuanlan.zhihu.com/pythoner"
        # "https://zhuanlan.zhihu.com/api/columns/pythoner"
        # "https://zhuanlan.zhihu.com/api/columns/LaTeX"
        # "https://www.zhihu.com/topic/19559424/top-answers"
    ]

    def start_requests(self):
        session = login.Login().login(settings.USER_INFO_FILE, settings.PASSWORD)
        for url in self.start_urls:
            yield Request(
                url=url,
                headers=tools.set_headers(url),
                cookies=tools.unfold_cookies(session.cookies),
                # meta={}zhuanlan.zhihu.com
            )

    def parse(self, response):  # 通过parse()分发解析去向
        type_ = tools.url_type_select(response.url)
        if type_ in ["people"]:
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
            # elif type_ in ["topic_next"]:
            #     return topics.TopicsNext(response).item


if __name__ == "__main__":
    from scrapy.cmdline import execute

    execute()
    print("")
