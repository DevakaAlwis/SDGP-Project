# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    productId = scrapy.Field()
    productURL = scrapy.Field()
    productName = scrapy.Field()
    productSiteName = scrapy.Field()
    productPrice = scrapy.Field()
    productRating = scrapy.Field()
    productImage = scrapy.Field()
    productReviewCount = scrapy.Field()

    pass


class AmazonReviewItem(scrapy.Item):

    productId = scrapy.Field()
    reviewText = scrapy.Field()
    reviewRating = scrapy.Field()

    pass


class WalmartProductItem(scrapy.Item):

    productId = scrapy.Field()
    productURL = scrapy.Field()
    productName = scrapy.Field()
    productSiteName = scrapy.Field()
    productPrice = scrapy.Field()
    productRating = scrapy.Field()
    productReviewCount = scrapy.Field()
    productImage = scrapy.Field()

    pass


class WalmartReviewItem(scrapy.Item):

    productId = scrapy.Field()
    reviewText = scrapy.Field()
    reviewRating = scrapy.Field()

    pass
