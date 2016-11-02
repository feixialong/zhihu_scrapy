# -*- coding: utf-8 -*-

import unittest
from zhihu_scrapy import settings

from zhihu_scrapy import tools


class TestLogin(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_type_select(self):
        urls = {
            "https://www.zhihu.com/topic/19559424/top-answers": "topic",
            "https://www.zhihu.com/people/jixin": "people",
            "https://www.zhihu.com/people/jixin/followees": "followees",
            "https://www.zhihu.com/people/chen-fan-85/followers": "followers",
            # "https://zhuanlan.zhihu.com/pythoner": "columns",
            "https://zhuanlan.zhihu.com/api/columns/pythoner": "columns",
            "https://zhuanlan.zhihu.com/p/22947665": "articles",
            "https://zhuanlan.zhihu.com/api/posts/23190728/comments": "article_comments"

        }
        for url in urls:
            self.assertEqual(tools.url_type_select(url), urls[url], "{url}判断错误".format(url=url))


if __name__ == "__main__":
    unittest.main()
