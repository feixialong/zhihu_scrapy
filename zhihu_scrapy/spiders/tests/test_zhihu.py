# -*- coding: utf-8 -*-

import unittest
from zhihu_scrapy.spiders import zhihu
from scrapy import cmdline


class TestZhihu(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_type_select(self):
        self.test_zhihu = zhihu.ZhihuSpider()
        urls = {
            "https://www.zhihu.com/people/jixin/followees": "followees",
            "https://www.zhihu.com/people/jixin/followers": "followers",
            "https://www.zhihu.com/people/jixin/asks": "asks",
            "https://www.zhihu.com/people/jixin/answers": "answers",
            "https://www.zhihu.com/people/jixin/posts": "posts",
            "https://www.zhihu.com/people/jixin/collections": "collections",
            "https://www.zhihu.com/people/jixin/columns/followed": "columns",
            "https://www.zhihu.com/people/jixin/topics": "topics",
            "https://www.zhihu.com/people/jixin": "people",
            "https://www.zhihu.com/question/36546814/answer/84509117": "answer",
            "https://www.zhihu.com/question/36546814": "question",
            "https://www.baidu.com": ""
        }
        for url in urls:
            self.assertEqual(self.test_zhihu.url_type_select(url), urls[url],
                             "{url}判断错误".format(url=url))

    def test_people(self):
        try:
            cmdline.execute("scrapy crawl test_people".split())
        except SystemExit:
            print("Succeed!")

    def test_followees(self):
        try:
            cmdline.execute("scrapy crawl test_followees".split())
        except SystemExit:
            print("Succeed!")


class TestPeople(zhihu.ZhihuSpider):
    name = "test_people"
    start_urls = [
        'https://www.zhihu.com/people/stevenjohnson',
        'https://www.zhihu.com/people/jixin',
        'https://www.zhihu.com/people/jasinyip',
        'https://www.zhihu.com/people/tnttnt',
        'https://www.zhihu.com/people/hydfox'
    ]


class TestFollowees(zhihu.ZhihuSpider):
    name = "test_followees"
    start_urls = [
        # "https://www.zhihu.com/people/jixin/followees",
        "https://www.zhihu.com/people/mei-ying-0829/followees"
    ]


if __name__ == "__main__":
    unittest.main()
