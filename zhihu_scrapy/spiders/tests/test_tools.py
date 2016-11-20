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
            "https://www.zhihu.com/people/hydfox": "people_home",
            "https://www.zhihu.com/people/jixin/followees": "people_followees",
            "https://www.zhihu.com/people/chen-fan-85/followers": "people_followers",
            "https://www.zhihu.com/people/stevenjohnson/asks": "people_questions",
            "https://www.zhihu.com/people/stevenjohnson/answers": "people_answers",
            "https://www.zhihu.com/people/stevenjohnson/posts": "people_articles",
            "https://www.zhihu.com/people/stevenjohnson/collections": "people_collections"

        }
        for url in urls:
            self.assertEqual(urls[url], tools.url_type_select(url), "{url}判断错误".format(url=url))


if __name__ == "__main__":
    unittest.main()
