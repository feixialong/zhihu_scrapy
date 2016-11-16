# -*- coding: utf-8 -*-

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

rule_people = Rule(
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

rules = [
    rule_people,

]
