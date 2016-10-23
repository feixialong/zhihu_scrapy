# -*- coding: utf-8 -*-

import unittest
from zhihu_scrapy import settings
from zhihu_scrapy.spiders import login



class TestLogIn(unittest.TestCase):
    def setUp(self):
        self.test_login = login.Login()

    def tearDown(self):
        pass

    # @unittest.skip("")
    def test_read_user_info(self):
        files = {
            "user.info.example": ("username", "password"),
            "user": (None, None)
        }
        for file in files:
            print(file, files[file])
            self.assertEqual(login.read_user_info(file), files[file], "{file}用户信息读取错误".format(file=file))

    # @unittest.skip("")
    def test_is_tel_num(self):
        tels = {
            "12456989": False,
            "jkljgkljk": False,
            "1854268kg46": False,
            "18542689546125": False,
            "18542689546": True
        }
        for tel in tels:
            print(tel, tels[tel])
            self.assertEqual(login.is_tel_num(tel), tels[tel], "{tel}判断错误".format(tel=tel))

    def test_url_select(self):
        usernames = {
            "12456989": ("https://www.zhihu.com/login/email", "email"),
            "jkljgkljk": ("https://www.zhihu.com/login/email", "email"),
            "1854268kg46": ("https://www.zhihu.com/login/email", "email"),
            "18542689546125": ("https://www.zhihu.com/login/email", "email"),
            "18542689546": ("https://www.zhihu.com/login/phone_num", "phone_num"),
            "wumignshun@123.com": ("https://www.zhihu.com/login/email", "email")
        }
        for username in usernames:
            print(username, usernames[username])
            self.assertEqual(login._url_select(username), usernames[username],
                             "{username}判断错误".format(username=username))

    # @unittest.skip("")
    def test_get_xsrf(self):
        _xsrf = self.test_login.get_xsrf()
        self.assertEqual(len(_xsrf), 32, "_xsrf获取失败")

    def test_is_login_succeed(self):
        texts = {
            '{"msg": "登陆成功"}': True,
            '{"msg": "\u767b\u5f55\u6210\u529f"}': True,
            '{"msg": "登录过于频繁，请稍后重试"}': False,
            '{"msg": ""}': False,
            '': False,
        }
        for text in texts:
            print(text, texts[text])
            self.assertEqual(self.test_login.is_login_succeed(text), texts[text], "{text}登录状态判断错误".format(text=text))

    def test_get_url_and_postdata(self):
        username, password = login.read_user_info(settings.USER_INFO_FILE)
        url, data = self.test_login.get_url_and_postdata(username, password)
        self.assertEqual(type(url), type(""), "数据类型错误")
        self.assertEqual(type(data), type(data), " 数据类型错误")

    def test_get_captcha_file(self):
        self.assertEqual(self.test_login.get_captcha_file(), True, "获取验证码失败")


if __name__ == "__main__":
    unittest.main()

