
BOT_NAME = 'webscrape'

SPIDER_MODULES = ['webscrape.spiders']
NEWSPIDER_MODULE = 'webscrape.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False


#SCRAPEOPS_API_KEY = 'cb20c190-26f8-4c75-a805-8e81ed87e92f'     #devaka key
SCRAPEOPS_API_KEY = '617e74a2-96f9-4eba-ac12-59552235e249'      #bimsara key


SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}


DOWNLOADER_MIDDLEWARES = {

    # ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,

    # Proxy Middleware
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1

ITEM_PIPELINES = {
    'webscrape.pipelines.AmazonMongoDBPipeline': 300,
}


MONGO_URI = 'mongodb+srv://liviniAdmin:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority'
MONGO_DATABASE = 'db'
