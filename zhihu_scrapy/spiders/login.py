# -*- coding: utf-8 -*-

import requests

USER_INFO_FILE = "user.info"
COOKIES_FILE = "cookies"
CAPTCHA_FILE = "captcha.jpg"
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
        "host": "www.zhihu.com"
    }
    return headers


def init_section():
    session = requests.session()
    session.headers = set_headers()
    session.verify = IS_VERIFY
    return session


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


def is_login_succeed(responst_text):
    import json
    try:
        status = json.loads(responst_text).get("msg")
    except:
        return False
    if status in ["登陆成功"]:
        return True
    elif status in ["登录过于频繁，请稍后重试", "email 对应的账户不存在", "验证码会话无效 :("]:
        return False
    else:
        return False


def get_xsrf():
    from lxml import etree
    url = "https://www.zhihu.com/"
    session = init_section()
    doc = etree.HTML(session.get(url).text)
    return doc.xpath('/html/body/input')[0].get("value")


def get_url_and_postdata(username, password):
    url, key = _url_select(username)
    data = {
        key: username,
        "password": password,
        "remember_me": True,
        "captcha_type": "cn",
        "_xsrf": get_xsrf()
    }
    return url, data


def get_captcha_file():
    import os
    import time
    if os.path.exists(CAPTCHA_FILE):
        os.remove(CAPTCHA_FILE)
    else:
        pass
    t = str(int(time.time() * 1000))
    session = init_section()
    captcha_url = 'http://www.zhihu.com/captcha.gif?r' + t + "&type=login"
    response = session.get(url=captcha_url)
    with open(CAPTCHA_FILE, 'wb') as f:
        f.write(response.content)
    if os.path.exists(CAPTCHA_FILE):
        return True
    else:
        return False


def try_to_open_captcha_file(file):
    try:
        from PIL import Image
        Image.open(file)
    except:
        pass


def update_postdata(data):
    import os
    if get_captcha_file():
        try_to_open_captcha_file(CAPTCHA_FILE)
        data["captcha"] = input("请打开{captcha_file}，输入验证码".format(
            captcha_file=os.path.abspath(CAPTCHA_FILE)
        ))
        return data
    else:
        return False


def login(username, password):
    import json
    import http.cookiejar
    session = init_section()
    session.cookies = http.cookiejar.LWPCookieJar(filename=COOKIES_FILE)
    url, data = get_url_and_postdata(username, password)
    response = session.post(url=url, data=json.dumps(data))
    while not is_login_succeed(response.text):
        update_postdata(data)
        response = session.post(url=url, data=json.dumps(data))
        print(json.loads(response.text).get("msg"))
    session.cookies.save()
    return session


if __name__ == '__main__':
    username, password = read_user_info(USER_INFO_FILE)
    print(login(username, password))
