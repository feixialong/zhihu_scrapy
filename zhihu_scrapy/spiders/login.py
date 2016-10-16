# -*- coding: utf-8 -*-

import requests

USER_INFO_FILE = "user.info"


def read_userinfo(file):
    import json
    with open(file, 'r') as f:
        data = json.loads(f.read())
    return data.get("username"), data.get("password")


def is_tel_num(username):
    import re
    pattern = r"\d{11}"
    if len(username) == 11:
        if re.match(pattern, username) is not None:
            return True
    else:
        return False


def choose_url(username):
    if is_tel_num(username):
        return "https://www.zhihu.com/login/phone_num"
    else:
        return "https://www.zhihu.com/login/email"


def set_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
        "host": "www.zhihu.com"
    }
    return headers


class Login(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = choose_url(username)
        self.session = self.__set_section()
        self.response = None

    def choose_url(self):
        if is_tel_num(self.username):
            return "https://www.zhihu.com/login/phone_num"
        else:
            return "https://www.zhihu.com/login/email"

    @staticmethod
    def __set_section():
        session = requests.session()
        session.headers = set_headers()
        return session

    def get_xsrf(self):
        from lxml import etree
        response = self.session.get(self.url)
        print(response.text)
        doc = etree.HTML(response.text)
        return doc.xpath('//*[@id="sign-form-1"]/input[2]')[0].get("value")


if __name__ == '__main__':
    username, password = read_userinfo(USER_INFO_FILE)
    login = Login(username, password)
    print(login.url)
    print(login.get_xsrf())



