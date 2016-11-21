# -*- coding: utf-8 -*-


import pymongo


class MyMongoDB(object):
    def __init__(self, host="localhost", port=27017):
        self.client = self.connect_to_client(host, port)

    @classmethod
    def connect_to_client(cls, host, port):
        return pymongo.MongoClient(host, port)

    def use_db(self, db_name):
        return self.client[db_name]

    def use_collection(self, db_name, collection_name):
        return self.use_db(db_name)[collection_name]


if __name__ == "__main__":
    host = "localhost"
    port = 27017
    zhihudb = MyMongoDB(host, port)
    people = zhihudb.use_collection("zhihu", "people")
    r = people.find_one({"user_name": "不是归人"})
    if not r:
        print("进来")
