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
            self.questions.update({"question_url": item["question_url"]}, {"$set": item})
            # self.questions.insert(item)
        elif data_type in ["answer"]:
            self.questions.update({"answer_url": item["answer_url"]}, {"$set": item})
            # self.answers.insert(item)
        elif data_type in ["people"]:
            self.questions.update({"user_url": item["user_url"]}, {"$set": item})
            # self.people.insert(item)
        elif data_type in ["article"]:
            self.questions.update({"article_url": item["article_url"]}, {"$set": item})
            # self.articles.insert(item)
        return item


if __name__ == "__main__":
    zhihu_pipeline = ZhihuScrapyPipeline()
