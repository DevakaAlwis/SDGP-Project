from urllib.parse import urljoin

import pymongo
import scrapy
from webscrape.items import AmazonProductItem
from webscrape.settings import MONGO_DATABASE, MONGO_URI


# class for amazon search spider to scrape the amazon products 
class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search"  # name of the spider

    # starting function of the amazonSearchSpider
    def start_requests(self):
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE]
        # delete previous collection
        products_collection = db["amazonProducts"]
        products_collection.drop()

        # select the searchProduct from collection
        search_collection = db["searchProducts"]
        searchProducts = search_collection.find()
        productNameList = [item["productName"] for item in searchProducts]

        # keywords = getattr(self, 'keywords')
        # keywords = ['Black Soft Faux Vegan PU {Peta Approved Vegan} Leather by The Yard Synthetic Pleather 0.9 mm Nappa Yards (72 inch Wide x 52 inch) Soft Smooth Upholstery (Black Pebble, 2 Yards (72"x54"))']
        for keyword in productNameList:
            amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
            yield scrapy.Request(url=amazon_search_url, callback=self.parse)

    # function to get product details
    def parse(self, response):

        # Extract Overview Product Data
        search_products = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )
        count = 0
        item = AmazonProductItem()
        for product in search_products:
            # get only 2 products
            if count < 2:

                relative_url = product.css("h2>a::attr(href)").get()
                asin = (relative_url.split("/")[3]
                        if len(relative_url.split('/')) >= 4
                        else None
                )
                product_url = urljoin("https://www.amazon.com/",
                                      relative_url).split(
                    "?"
                )[0]
                item["productId"] = asin
                item["productName"] = product.css("h2>a>span::text").get()
                item["productPrice"] = product.css(
                    ".a-price[data-a-size=xl] .a-offscreen::text"
                ).get()
                item["productURL"] = product_url
                item["productSiteName"] = "Amazon"
                rating = (
                    product.css("span[aria-label~=stars]::attr(aria-label)").re(
                        r"(\d+\.*\d*) out"
                    ) 
                    or [None]
                )[0]
                item["productRating"] = rating
                item["productReviewCount"] = product.css(
                    "span[aria-label~=stars] + span::attr(aria-label)"
                ).get()
                item["productImage"] = product.xpath(
                    "//img[has-class('s-image')]/@src"
                ).get()
                yield item

                count += 1
            else:
                break


# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=rkb9LVb4hlU&t=439s
