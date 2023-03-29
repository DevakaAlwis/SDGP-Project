import scrapy
import pymongo
from webscrape.items import AmazonReviewItem
from urllib.parse import urljoin


class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    def start_requests(self):
        client = pymongo.MongoClient(
            'mongodb+srv://devakaAdmin:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority')
        db = client["db"]
        # delete previous collection
        reviews_collection = db["amazonReviews"]
        reviews_collection.drop()

        # select the amazonProducts from collection
        products_collection = db["amazonProducts"]
        products = products_collection.find()

        productIDList = [item["productId"] for item in products]
        if (productIDList != []):
            # keyword = ["iphone 12"]
            # asin_list = getattr(self, 'keywords')
            # asin_list=['B0B87YNY91','B0BN91GD3J']
            # one review B07MVMZDMD
            # 90 reviews B081TK6DDD
            # asin_list = ['B07MVMZDMD']
            for asin in productIDList:
                amazon_reviews_url = f'https://www.amazon.com/product-reviews/{asin}/'
                yield scrapy.Request(url=amazon_reviews_url, callback=self.parse_reviews, dont_filter=False, meta={'asin': asin, 'retry_count': 0})

    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        next_page_relative_url = response.css(
            ".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/',
                                next_page_relative_url)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, dont_filter=False, meta={'asin': asin, 'retry_count': retry_count})

        # Adding this retry_count here so we retry any amazon js rendered review pages
        elif retry_count < 2:
            retry_count = retry_count+1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=False, meta={'asin': asin, 'retry_count': retry_count})

        # Parse Product Reviews
        review_elements = response.css("#cm_cr-review_list div.review")
        item = AmazonReviewItem()
        for review_element in review_elements:
            item["productId"] = asin
            item["reviewText"] = "".join(review_element.css(
                "span[data-hook=review-body] ::text").getall()).strip()
            item["reviewRating"] = review_element.css(
                "*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0]
            yield item

# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=wRHLX7xX2Xw
