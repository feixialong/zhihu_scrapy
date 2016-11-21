# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from zhihu_scrapy import db
from zhihu_scrapy import tools


class ZhihuScrapyPipeline(object):
    def __init__(self):
        self.zhihu = db.MyMongoDB("localhost", 27017).use_db("zhihu")
        self.questions = self.zhihu["questions"]
        self.answers = self.zhihu["answers"]
        self.people = self.zhihu["people"]
        self.articles = self.zhihu["articles"]
        # self.saved_urls = self.zhihu["saved_urls"]

    def process_item(self, item, spider):
        data_type = tools.data_type_select(item)
        if data_type in ["question"]:
            if not self.questions.find_one({"question_url": item["question_url"]}):
                self.questions.insert(item)
        elif data_type in ["answer"]:
            if not self.answers.find_one({"answer_url": item["answer_url"]}):
                self.answers.insert(item)
        elif data_type in ["people"]:
            if not self.people.find_one({"user_url": item["user_url"]}):
                self.people.insert(item)
        elif data_type in ["article"]:
            if not self.articles.find_one({"article_url": item["article_url"]}):
                self.articles.insert(item)
        return item


if __name__ == "__main__":
    zhihu_pipeline = ZhihuScrapyPipeline()
