import json
import scrapy
from urllib.parse import urlencode, urljoin
from webscrape.items import WalmartProductItem
import pymongo


class WalmartSpider(scrapy.Spider):

    name = "walmart_search"

    def start_requests(self):
        # keyword_list = ['iphone 13']

        client = pymongo.MongoClient(
            'mongodb+srv://devakaAdmin:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority')
        db = client["db"]
        # delete previous collection
        products_collection = db["walmartProducts"]
        products_collection.drop()
        # select the searchProduct from collection
        search_collection = db["searchProducts"]

        searchProducts = search_collection.find()
        productNameList = [item["productName"] for item in searchProducts]
        for keyword in productNameList:
            payload = {'q': keyword, 'sort': 'best_seller',
                       'page': 1, 'affinityOverride': 'default'}
            walmart_search_url = 'https://www.walmart.com/search?' + \
                urlencode(payload)
            yield scrapy.Request(url=walmart_search_url, callback=self.parse, meta={'keyword': keyword, 'page': 1})

    def parse(self, response):
        script_tag = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            json_blob = json.loads(script_tag)

            # Request Product Page
            product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
            count = 0
            item = WalmartProductItem()
            for product in product_list:
                if (count < 2):
                    try:
                        item['productId'] = product.get('usItemId')
                        item['productName'] = product.get('name')
                        item['productPrice'] = product['priceInfo'].get(
                            'linePriceDisplay')
                        relative_url = product.get('canonicalUrl')
                        item['productURL'] = urljoin(
                            'https://www.walmart.com/', relative_url).split("?")[0]
                        item['productSiteName'] = "Walmart"
                        item['productRating'] = product['rating'].get(
                            'averageRating')
                        item['productReviewCount'] = product['rating'].get(
                            'numberOfReviews')
                        item['productImage'] = product['imageInfo'].get(
                            'thumbnailUrl')

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
                    except:  # AttributeError
                        raise ("Error in product inserting")
                else:
                    break
                count += 1

# References
# https://scrapy.org/
# https://scrapeops.io/
# https://www.youtube.com/watch?v=nfh8rGf7TtA&t=230s
