import scrapy
from webscrape.items import AmazonProductItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from urllib.parse import urljoin


class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search"

    def start_requests(self):
        # keywords = getattr(self, 'keywords')
        keywords = ['Iphone 13']
        for keyword in keywords:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.parse)

    def parse(self, response):

        # Extract Overview Product Data
        search_products = response.css(
            "div.s-result-item[data-component-type=s-search-result]")
        count = 0
        item = AmazonProductItem()
        for product in search_products:
            if (count < 2):

                relative_url = product.css("h2>a::attr(href)").get()
                asin = relative_url.split(
                    '/')[3] if len(relative_url.split('/')) >= 4 else None
                product_url = urljoin(
                    'https://www.amazon.com/', relative_url).split("?")[0]

                item["productId"] = asin
                item["productName"] = product.css("h2>a>span::text").get()
                item["productPrice"] = product.css(
                    ".a-price[data-a-size=xl] .a-offscreen::text").get()
                item["productURL"] = product_url
                item["productSiteName"] = "Amazon"
                rating = (product.css(
                    "span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0]
                item["productRating"] = rating
                item["productReviewCount"]: product.css(
                    "span[aria-label~=stars] + span::attr(aria-label)").get()
                item["productImage"] = product.xpath(
                    "//img[has-class('s-image')]/@src").get()
                yield item

                count += 1
            else:
                break
