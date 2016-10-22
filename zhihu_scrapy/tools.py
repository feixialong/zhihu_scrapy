# -*- coding: utf-8 -*-


def set_headers(url=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
        "Host": "www.zhihu.com",
        'Accept-Encoding': 'gzip'
    }
    if url is None:
        headers['Referer'] = 'http://www.zhihu.com/'
    else:
        headers['Referer'] = url
    return headers


if __name__ == '__main__':
    pass