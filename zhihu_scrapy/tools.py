# -*- coding: utf-8 -*-

import os
import json
import re

import http.cookiejar

from scrapy import settings


def url_type_select(url):
    if url is not None:
        if url.find("zhihu") == -1:
            return ""
        else:
            url_splited = url.split("/")
            url_splited.reverse()
            types = [
                "people",
                "followees",
                "followers",
                "asks",
                "answers",
                "posts",
                "collections",
                "columns",
                "topic",
                "answer",
                "question"
            ]
            for i in url_splited:
                if i in types:
                    return i
                else:
                    pass
            return "columns"

def set_headers(url=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
        "Host": "www.zhihu.com",
        'Accept-Encoding': 'gzip',
        "Connection": "keep-alive"
    }
    if url is None:
        headers['Referer'] = 'http://www.zhihu.com/'
    else:
        headers['Referer'] = url
    if url_type_select(url) in ["columns"]:
        headers.update({
            "Host": "zhuanlan.zhihu.com"
        })
    return headers


def read_user_info(file):
    os.chdir(os.path.split(__file__)[0])  # 避免单元测试不通过
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.loads(f.read())
        return data.get("username"), data.get("password")
    return None, None


def is_tel_num(num):
    pattern = r"\d{11}"
    if len(num) == 11:
        if re.match(pattern, num) is not None:
            return True
        else:
            return False
    else:
        return False


def url_select(username):
    if is_tel_num(username):
        return "https://www.zhihu.com/login/phone_num", "phone_num"
    else:
        return "https://www.zhihu.com/login/email", "email"


def read_cookie(filename):
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    cookies = http.cookiejar.LWPCookieJar(filename=filename)
    if os.path.exists(filename):
        cookies.load()
        return cookies
    else:
        return None


def unfold_cookies(lwp_cookie_jar):
    _cookies = lwp_cookie_jar._cookies
    cookies = []
    for domain in _cookies:
        for path in _cookies[domain]:
            for cookie in _cookies[domain][path]:
                cookie = _cookies[domain][path][cookie].__dict__
                cookies.append(cookie)
    return cookies


def get_num_from_str(str_):
    pattern = re.compile(r'\d+')
    num_strs = re.findall(pattern, str_)
    return [int(s) for s in num_strs]


def dict_response_body(body):
    if type(body) == type(b''):
        return json.loads(body.encode("utf-8"))
    elif type(body)  == type(''):
        return json.loads(body)
    else:
        return json.loads(body)

