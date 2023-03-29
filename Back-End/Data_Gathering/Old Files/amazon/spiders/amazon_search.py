import scrapy
from urllib.parse import urljoin

class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def start_requests(self):
        keyword_list = ['Apple iPhone 14']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Extract Overview Product Data
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        count=0
        for product in search_products:
            if(count<2):
                relative_url = product.css("h2>a::attr(href)").get()
                asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                yield  {
                        # "keyword": keyword,
                        "asin": asin,
                        "url": product_url,
                        # "ad": True if "/slredirect/" in product_url else False, 
                        "title": product.css("h2>a>span::text").get(),
                        "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                        # "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                        "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                        "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                        "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                    }
                count+=1


        ## Get All Pages
        # if page == 1:
        #     available_pages = response.xpath(
        #         '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
        #     ).getall()

        #     for page_num in available_pages:
        #         amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
        #         yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})


        
    

