# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import pymongo
from pymongo.errors import DuplicateKeyError
from webscrape.items import AmazonProductItem, AmazonReviewItem


class AmazonMongoDBPipeline:
    collection_name=""
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            if(spider.name=="amazon_search"):
                collection_name='products'
                self.db[collection_name].insert_one(
                    dict(AmazonProductItem(item)))
            elif(spider.name=="amazon_reviews"):
                collection_name="reviews"
                self.db[collection_name].insert_one(
                    dict(AmazonReviewItem(item)))
        except DuplicateKeyError:
            print("Duplicate key error occurred")
        return item

