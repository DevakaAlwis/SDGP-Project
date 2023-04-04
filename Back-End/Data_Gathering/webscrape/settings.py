import os

from dotenv import load_dotenv

BOT_NAME = "webscrape"

SPIDER_MODULES = ["webscrape.spiders"]
NEWSPIDER_MODULE = "webscrape.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Scrapeops API key
load_dotenv()
WEBSCRAPE_API_KEY = os.getenv("WEBSCRAPE_API_KEY")
SCRAPEOPS_API_KEY = WEBSCRAPE_API_KEY  # key


SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
    "scrapeops_scrapy.extension.ScrapeOpsMonitor": 500,
}


DOWNLOADER_MIDDLEWARES = {
    # ScrapeOps Monitor
    "scrapeops_scrapy.middleware.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    # Proxy Middleware
    "scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk": 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1

ITEM_PIPELINES = {
    "webscrape.pipelines.MongoDBPipeline": 300,
}

# MongoDB connection
MONGO_URI = "mongodb+srv://liviniAdmin:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority"
MONGO_DATABASE = "db"
