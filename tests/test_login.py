# -*- coding: utf-8 -*-

import unittest
from zhihu_scrapy.spiders import login


class TestLogIn(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("")
    def test_read_userinfo(self):
        files = {
            "user.info.example": ("username", "password"),
            "user": (None, None)
        }
        for file in files:
            self.assertEqual(login.read_userinfo(file), files[file], "用户信息读取错误")

    @unittest.skip("")
    def test_is_tel_num(self):
        tels = {
            "12456989": False,
            "jkljgkljk": False,
            "1854268kg46": False,
            "18542689546125": False,
            "18542689546": True
        }
        for tel in tels:
            self.failUnlessEqual(login.is_tel_num(tel), tels[tel], "{tel}判断错误".format(tel=tel))


if __name__ == "__main__":
    unittest.main()
