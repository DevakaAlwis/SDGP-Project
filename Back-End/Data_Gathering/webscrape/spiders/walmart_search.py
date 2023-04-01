import json
import pymongo
import scrapy
from urllib.parse import urlencode, urljoin
from webscrape.items import WalmartProductItem
from webscrape.settings import MONGO_DATABASE, MONGO_URI


# class for amazon search spider to scrape the amazon products
class WalmartSpider(scrapy.Spider):

    name = "walmart_search" # name of the spider

    # starting function of the walmartnSearchSpider
    def start_requests(self):
        # keyword_list = ["iphone 13"]

        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE]
        # delete previous collection
        products_collection = db["walmartProducts"]
        products_collection.drop()
        # select the searchProduct from collection
        search_collection = db["searchProducts"]

        searchProducts = search_collection.find()
        productNameList = [item["productName"] for item in searchProducts]
        for keyword in productNameList:
            payload = {
                "q": keyword, 
                "sort": "best_seller",
                "page": 1, 
                "affinityOverride": "default"
                }
            walmart_search_url = "https://www.walmart.com/search?" + urlencode(payload)
            yield scrapy.Request(url=walmart_search_url, 
                                 callback=self.parse, 
                                 meta={'keyword': keyword, 'page': 1}
                                 )

    # function to get product details
    def parse(self, response):
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)

            # Request Product Page
            product_list = json_blob["props"]["pageProps"]["initialData"]
            ["searchResult"]["itemStacks"][0]["items"]
            count = 0
            item = WalmartProductItem()
            for product in product_list:
                # get only 2 products
                if count < 2:
                    try:
                        item["productId"] = product.get("usItemId")
                        item["productName"] = product.get("name")
                        item["productPrice"] = product["priceInfo"].get("linePriceDisplay")
                        relative_url = product.get("canonicalUrl")
                        item["productURL"] = urljoin("https://www.walmart.com/", relative_url).split("?")[0]
                        item["productSiteName"] = "Walmart"
                        item["productRating"] = product["rating"].get("averageRating")
                        item["productReviewCount"] = product["rating"].get("numberOfReviews")
                        item["productImage"] = product["imageInfo"].get("thumbnailUrl")

                        # yield{
                        #     'productID': product.get('id'),
                        #     'productName' :   product.get('name'),
                        #     'productPrice' :   product['priceInfo'].get('linePriceDisplay'),
                        #     'productURL' :   urljoin('https://www.walmart.com/', relative_url).split("?")[0],
                        #     'productSiteName' :  "Walmart",
                        #     'productRating':   product['rating'].get('averageRating'),
                        #     'productReviewCount' :   product['rating'].get('numberOfReviews'),
                        #     'productImage' :   product['imageInfo'].get('thumbnailUrl'),
                        # }
                        yield item
                    except AttributeError as e:  # AttributeError
                        raise (e)
                else:
                    break
                count += 1


# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=nfh8rGf7TtA&t=230s
