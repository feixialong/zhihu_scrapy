# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PeopleItem(scrapy.Item):
    user_url = scrapy.Field()
    avatar_url = scrapy.Field()
    user_name = scrapy.Field()
    gender = scrapy.Field()
    company = scrapy.Field()
    job = scrapy.Field()
    location = scrapy.Field()
    school = scrapy.Field()
    major = scrapy.Field()
    business = scrapy.Field()
    desc = scrapy.Field()
    agrees_num = scrapy.Field()
    thanks_num = scrapy.Field()
    asks_num = scrapy.Field()
    answers_num = scrapy.Field()
    articles_num = scrapy.Field()
    collections_num = scrapy.Field()
    edit_num = scrapy.Field()
    followed_others_num = scrapy.Field()
    be_followed_num = scrapy.Field()
    lives_num = scrapy.Field()
    topics_num = scrapy.Field()
    columns_num = scrapy.Field()
    visited_num = scrapy.Field()

