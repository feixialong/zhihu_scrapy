# -*- coding: utf-8 -*-

import requests

USER_INFO_FILE = "user.info"
COOKIES_FILE = "cookies"
CAPTCHA_FILE = "captcha.bmp"
IS_VERIFY = True


def read_user_info(file):
    import json
    import os
    os.chdir(os.path.split(__file__)[0])
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.loads(f.read())
        return data.get("username"), data.get("password")
    return None, None


def set_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
        "host": "www.zhihu.com",
        'Referer': 'http://www.zhihu.com/',
        'Accept-Encoding': 'gzip'
    }
    return headers


def is_tel_num(num):
    import re
    pattern = r"\d{11}"
    if len(num) == 11:
        if re.match(pattern, num) is not None:
            return True
        else:
            return False
    else:
        return False


def _url_select(username):
    if is_tel_num(username):
        return "https://www.zhihu.com/login/phone_num", "phone_num"
    else:
        return "https://www.zhihu.com/login/email", "email"


class Login():
    def __init__(self):
        import requests
        import http.cookiejar
        self.session = requests.session()
        self.session.headers = set_headers()
        self.session.verify = IS_VERIFY
        self.session.cookies = http.cookiejar.LWPCookieJar(filename=COOKIES_FILE)

    def read_cookie(self, filename=COOKIES_FILE):
        import os
        import http.cookiejar
        self.session.cookies = http.cookiejar.LWPCookieJar(filename=filename)
        if os.path.exists(filename):
            self.session.cookies.load()
            return True
        else:
            return False

    def get_xsrf(self):
        from lxml import etree
        url = "https://www.zhihu.com/"
        doc = etree.HTML(self.session.get(url).text)
        return doc.xpath('/html/body/input')[0].get("value")

    def get_url_and_postdata(self, username, password):
        url, key = _url_select(username)
        data = {
            "email": username,
            "password": password,
            "remember_me": True,
            # "captcha_type": "cn",
            "_xsrf": self.get_xsrf()
        }
        return url, data

    def get_captcha_file(self):
        import os
        import time
        if os.path.exists(CAPTCHA_FILE):
            os.remove(CAPTCHA_FILE)
        else:
            pass
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r' + t + "&type=login"
        response = self.session.get(url=captcha_url)
        with open(CAPTCHA_FILE, 'wb') as f:
            f.write(response.content)
        if os.path.exists(CAPTCHA_FILE):
            return True
        else:
            return False

    def update_postdata(self, data):
        import os
        if self.get_captcha_file():
            data["captcha"] = input("请打开{captcha_file}，输入验证码：".format(
                captcha_file=os.path.abspath(CAPTCHA_FILE)
            ))
            return data
        else:
            return False

    @staticmethod
    def is_login_succeed(responst_text):
        import json
        try:
            status = json.loads(responst_text).get("msg")
            if status in ["登陆成功", "\u767b\u5f55\u6210\u529f"]:
                print(status)
                return True
            else:
                print(status)
                return False
        except:
            return False

    def __login(self, username, password):
        url, data = self.get_url_and_postdata(username, password)
        response = self.session.post(url=url, data=data)
        while not self.is_login_succeed(response.text):
            data = self.update_postdata(data)
            response = self.session.post(url=url, data=data)
        self.session.cookies.save()
        return self.session

    def login(self, username, password):
        if self.read_cookie(COOKIES_FILE):
            return self.session
        else:
            print("cookies加载失败，请手动登录！")
            return self.__login(username, password)


if __name__ == '__main__':
    username, password = read_user_info(USER_INFO_FILE)
    session = Login().login(username, password)
