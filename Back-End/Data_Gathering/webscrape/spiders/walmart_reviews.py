import json
import scrapy
from webscrape.items import WalmartReviewItem
import pymongo


class WalmartSpider(scrapy.Spider):
    name = "walmart_reviews"

    def start_requests(self):
        # id_list = ['1362658851']

        client = pymongo.MongoClient(
            'mongodb+srv://devakaAdmin:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority')
        db = client["db"]
        # delete previous collection
        reviews_collection = db["walmartReviews"]
        reviews_collection.drop()
        # select the walmartProducts from collection
        products_collection = db["walmartProducts"]
        products = products_collection.find()

        productIDList = [item["productId"] for item in products]
        if (productIDList != []):
            for id in productIDList:
                walmart_review_url = f'https://www.walmart.com/reviews/product/{id}'
                yield scrapy.Request(url=walmart_review_url, callback=self.parse_review_pages, dont_filter=False, meta={'id': id, 'page': 0})

    def parse_review_pages(self, response):
        id = response.meta['id']
        page = response.meta['page']
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)
            item = WalmartReviewItem()
            reviews_list = json_blob["props"]["pageProps"]["initialData"]["data"]["reviews"]["customerReviews"]
            for review in reviews_list:
                productID = id
                reviewText = review.get("reviewText")
                if (reviewText == None):
                    break
                reviewRating = review.get("rating")

                item["productId"] = productID
                item["reviewText"] = reviewText
                item["reviewRating"] = reviewRating

                # yield{
                #     'productID': productID,
                #     'reviewText':  reviewText,
                #     'reviewRating':  reviewRating,
                # }
                yield item

            #paginate Through review pages
            if(page == 0):
                review_pages_blob = json_blob["props"]["pageProps"]["initialData"]["data"]["reviews"]
                review_count = review_pages_blob["pagination"]["total"]
                if(review_count >200):
                    review_count = 100

                for page in range(1,(review_count//20)):
                    next_url= f'https://www.walmart.com/reviews/product/{id}?page={page}'
                    yield scrapy.Request(url=next_url, callback=self.parse_review_pages, dont_filter=False, meta={'id': id, 'page': page})
                
# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=_8uxMS0anqQ
