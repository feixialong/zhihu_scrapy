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
    followees_num = scrapy.Field()
    followers_num = scrapy.Field()
    lives_num = scrapy.Field()
    topics_num = scrapy.Field()
    columns_num = scrapy.Field()
    visited_num = scrapy.Field()


class FolloweesItem(scrapy.Item):
    user_url = scrapy.Field()
    total_num = scrapy.Field()
    followees = scrapy.Field()
    followees_2 = scrapy.Field()


class FollowersItem(scrapy.Item):
    user_url = scrapy.Field()
    total_num = scrapy.Field()
    followers = scrapy.Field()
    followers_2 = scrapy.Field()


class AsksItem(scrapy.Item):
    user_url = scrapy.Field()
    total_num = scrapy.Field()
    followers = scrapy.Field()
    followers_2 = scrapy.Field()


class ColumnsItem(scrapy.Item):
    user_url = scrapy.Field()
    column_url = scrapy.Field()
    api_url = scrapy.Field()
    column_name = scrapy.Field()
    followers_num = scrapy.Field()
    articles = scrapy.Field()
    followers = scrapy.Field()
    topics = scrapy.Field()
    column_desc = scrapy.Field()
    followers = scrapy.Field()


class TopicsItem(scrapy.Item):
    topic_url = scrapy.Field()
    followers_num = scrapy.Field()
    top_answers = scrapy.Field()
    # followers = scrapy.Field()
    next_page_url = scrapy.Field()


class TopicsNextItem(scrapy.Item):
    topic_url = scrapy.Field()
    followers_num = scrapy.Field()
    top_answers = scrapy.Field()
    # followers = scrapy.Field()
    next_page_url = scrapy.Field()


class ArticlesItem(scrapy.Item):
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    user_url = scrapy.Field()
    content = scrapy.Field()
    agrees_num = scrapy.Field()
    columns = scrapy.Field()
    topics = scrapy.Field()
    comments_url = scrapy.Field()


class QuestionsItem(scrapy.Item):
    question_url = scrapy.Field()
    question_title = scrapy.Field()
    question_desc = scrapy.Field()
    topics = scrapy.Field()
    answers_num = scrapy.Field()
    question_url_token = scrapy.Field()
    answers = scrapy.Field()


class AnswersItem(scrapy.Item):
    user_url = scrapy.Field()
    content = scrapy.Field()
    agrees_num = scrapy.Field()
    answer_url = scrapy.Field()
    question_url = scrapy.Field()
    last_edit_time = scrapy.Field()
    topics = scrapy.Field()
    comments = scrapy.Field()
