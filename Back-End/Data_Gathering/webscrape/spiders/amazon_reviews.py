import scrapy
from webscrape.items import AmazonReviewItem
from urllib.parse import urljoin


class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    def start_requests(self):
        # asin_list = getattr(self, 'keywords')
        # asin_list=['B0B87YNY91','B0BN91GD3J']
        asin_list = ['B0BN91GD3J']
        for asin in asin_list:
            amazon_reviews_url = f'https://www.amazon.com/product-reviews/{asin}/'
            yield scrapy.Request(url=amazon_reviews_url, callback=self.parse, dont_filter=True, meta={'asin': asin, 'retry_count': 0})

    def parse(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        next_page_relative_url = response.css(
            ".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/',
                                next_page_relative_url)
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})

        # Adding this retry_count here so we retry any amazon js rendered review pages
        elif retry_count < 3:
            retry_count = retry_count+1
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})

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
