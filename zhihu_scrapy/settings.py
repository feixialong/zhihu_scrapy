# -*- coding: utf-8 -*-

import os
from zhihu_scrapy import tools

# Scrapy settings for zhihu_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihu_scrapy'

SPIDER_MODULES = ['zhihu_scrapy.spiders']
NEWSPIDER_MODULE = 'zhihu_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'zhihu_scrapy (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIE_DEBUG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
#     "Host": "www.zhihu.com",
#     'Accept-Encoding': 'gzip',
#     "Connection": "keep-alive",
#     "Referer": "http://www.zhihu.com"
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zhihu_scrapy.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'zhihu_scrapy.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhihu_scrapy.pipelines.ZhihuScrapyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


# 以下为各网址后缀
FOLLOWEE_URL_SUF = "/followees"
BASE_URL = "https://www.zhihu.com"
ZHUANLAN_BASE_URL = "https://zhuanlan.zhihu.com"
MORE_ANSWERS_URL = "https://www.zhihu.com/node/QuestionAnswerListV2"
MORE_FOLLOWERS_URL = "https://www.zhihu.com/node/ProfileFolloweesListV2"
API_URL = "https://www.zhihu.com/api/v4/members"
MORE_ANSWERS_HEADER = {
    "Content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Connection": "keep-alive",
    'Accept-Encoding': 'gzip',
}


# 登录相关
DIR = os.path.split(os.path.abspath(__file__))[0]
USER_INFO_FILE = os.path.join(DIR, "spiders/", "user.info")
USER_NAME, PASSWORD = tools.read_user_info(USER_INFO_FILE)
COOKIES_FILE = os.path.join(DIR, "spiders/", "cookies")
CAPTCHA_FILE = os.path.join(DIR, "spiders/", "captcha.bmp")
IS_VERIFY = True

DEDAULT_HEADERS = tools.set_headers()
