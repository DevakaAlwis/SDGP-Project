import json
import pymongo
import scrapy
from webscrape.items import WalmartReviewItem
from webscrape.settings import MONGO_DATABASE, MONGO_URI


# class for walmart Review spider to scrape the amazon reviews
class WalmartSpider(scrapy.Spider):
    name = "walmart_reviews"    # name of the spider

    # starting function of the walmartReviewSpider
    def start_requests(self):
        # id_list = ["1362658851"]

        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE]
        # delete previous collection
        reviews_collection = db["walmartReviews"]
        reviews_collection.drop()
        
        # select the walmartProducts from collection
        products_collection = db["walmartProducts"]
        products = products_collection.find()

        productIDList = [item["productId"] for item in products]
        if productIDList != []:
            #for loop to run each productIDList
            for id in productIDList:
                walmart_review_url = f"https://www.walmart.com/reviews/product/{id}"
                yield scrapy.Request(
                    url=walmart_review_url, 
                    callback=self.parse_review_pages, 
                    dont_filter=False, 
                    meta={'id': id, 'page': 0}
                    )

    # function to get reviews
    def parse_review_pages(self, response):
        id = response.meta["id"]
        page = response.meta["page"]
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)
            item = WalmartReviewItem()
            reviews_list = json_blob["props"]["pageProps"]["initialData"]["data"]
            ["reviews"]["customerReviews"]
            # for loop to get details from the review elements
            for review in reviews_list:
                productID = id
                reviewText = review.get("reviewText")
                # if the review text is none break the loop
                if reviewText == None:
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

            # paginate Through review pages
            if page == 0:
                review_pages_blob = json_blob["props"]["pageProps"]["initialData"]
                ["data"]["reviews"]
                review_count = review_pages_blob["pagination"]["total"]
                # if review count is greater than 200 get only 200 reviews
                if review_count >200:
                    review_count = 200

                # for loop to run until end of the last page
                for page in range(1,(review_count//20)):
                    next_url= (
                        f"https://www.walmart.com/reviews/product/{id}?page={page}"
                               )
                    yield scrapy.Request(url=next_url, 
                                         callback=self.parse_review_pages, 
                                         dont_filter=False, 
                                         meta={'id': id, 'page': page})
                
# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=_8uxMS0anqQ
