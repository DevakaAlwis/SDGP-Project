# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import pymongo
from pymongo.errors import DuplicateKeyError
from webscrape.items import (
    AmazonProductItem,
    AmazonReviewItem,
    WalmartProductItem,
    WalmartReviewItem,
)


# class for MongoDB pipeline to connect to the database and save the details to the collection
class MongoDBPipeline:
    collection_name = ""

    # constructor of the MongoDBPipeline
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # method is called when the spider is opened
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
            )

    # method is called when the spider is closed
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # self.db["searchProducts"].drop()

    # method is called for every item pipeline component
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            # check if the spider name is equal to the correspondent spider and 
            # insert the data to the correspondent collection
            if spider.name == "amazon_search":
                collection_name = "amazonProducts"
                self.db[collection_name].insert_one(dict(AmazonProductItem(item)))
            elif spider.name == "amazon_reviews":
                collection_name = "amazonReviews"
                self.db[collection_name].insert_one(dict(AmazonReviewItem(item)))
            elif spider.name == "walmart_search":
                collection_name = 'walmartProducts'
                self.db[collection_name].insert_one(dict(WalmartProductItem(item)))
            elif spider.name == "walmart_reviews":
                collection_name = "walmartReviews"
                self.db[collection_name].insert_one(dict(WalmartReviewItem(item)))
        except DuplicateKeyError:
            print("Duplicate key error occurred")
        return item
