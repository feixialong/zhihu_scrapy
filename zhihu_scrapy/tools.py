# -*- coding: utf-8 -*-

import os
import json
import re

import http.cookiejar

from scrapy import settings


def url_type_select(url):
    if url is None:
        raise TypeError
    else:
        if url.find("zhihu") == -1:
            return "not_zhihu"
        else:
            pass
    url_splited = url.split("/")
    length_of_url_splited = len(url_splited)
    if (length_of_url_splited == 5) and (url_splited[-2] == "people"):
        # "https://www.zhihu.com/people/hydfox"
        return "people"
    elif (length_of_url_splited == 6) and (url_splited[-1] == "followees") and (url_splited[-3] == "people"):
        # "https://www.zhihu.com/people/jixin/followees"
        return "followees"
    elif (length_of_url_splited == 6) and (url_splited[-1] == "followers") and (url_splited[-3] == "people"):
        # "https://www.zhihu.com/people/chen-fan-85/followers"
        return "followers"
    elif (length_of_url_splited == 6) and (url_splited[-1] == "top-answers") and (url_splited[-3] == "topic"):
        # "https://www.zhihu.com/topic/19559424/top-answers"
        return "topic"
    elif (length_of_url_splited == 6) and (url_splited[-2] == "columns") and (url_splited[-3] == "api"):
        # "https://zhuanlan.zhihu.com/api/columns/LaTeX"
        return "columns"
    elif (length_of_url_splited == 4) and (url_splited[2] == "zhuanlan.zhihu.com"):
        # "https://zhuanlan.zhihu.com/pythoner"  # 此类型网页未解析
        return "columns"
    elif (length_of_url_splited == 5) and (url_splited[-2] == "p") and (url_splited[-3] == "zhuanlan.zhihu.com"):
        # "https://zhuanlan.zhihu.com/p/23250032"  # 此类型网页未解析
        return "articles"
    elif (length_of_url_splited == 6) and (url_splited[2] == "zhuanlan.zhihu.com") and (url_splited[-3] == "api") and (url_splited[-2] == "posts"):
        # "https://zhuanlan.zhihu.com/api/posts/23190728"
        return "articles"
    elif (length_of_url_splited == 7) and (url_splited[2] == "zhuanlan.zhihu.com") and (url_splited[3] == "api") and (url_splited[4] == "posts") and (url_splited[-1] == "comments"):
        # https://zhuanlan.zhihu.com/api/posts/23190728/comments
        return "article_comments"
    else:
        raise TypeError("未定义网址类型，请将添加对 {url} 的识别".format(url=url))


def set_headers(url=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
        "Host": "www.zhihu.com",
        'Accept-Encoding': 'gzip',
        "Connection": "keep-alive"
    }
    if url is None:
        headers['Referer'] = 'http://www.zhihu.com'
    else:
        if url_type_select(url) in ["columns", "articles"]:
            headers.update({
                "Host": "zhuanlan.zhihu.com"
            })
        else:
            headers['Referer'] = url
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
    # cookies = http.cookiejar.LWPCookieJar(filename=filename)
    cookies = http.cookiejar.MozillaCookieJar(filename=filename)
    if os.path.exists(filename):
        cookies.load()
        return cookies
    else:
        return None


def unfold_cookies(lwp_cookie_jar):
    # todo 在保存的cookies形式更改后，此方法可能会有问题（虽然现在看似乎还可用）
    cookies_ = lwp_cookie_jar._cookies
    cookies = []
    for domain in cookies_:
        for path in cookies_[domain]:
            for cookie in cookies_[domain][path]:
                cookie = cookies_[domain][path][cookie].__dict__
                cookies.append(cookie)
    return cookies


def get_num_from_str(str_):
    pattern = re.compile(r'\d+')
    num_strs = re.findall(pattern, str_)
    return [int(s) for s in num_strs]


def dict_response_body(body):
    if type(body) == type(b''):
        return json.loads(body.encode("utf-8"))
    elif type(body) == type(''):
        return json.loads(body)
    else:
        return json.loads(body)
