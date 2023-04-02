import os

import pymongo
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# function to connect with the database


def databaseConnection():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    try:
        # Database connection
        client = pymongo.MongoClient(MONGO_URI)
        db = client["db"]

        # Connecting to Collections
        search_collection = db["searchProducts"]
        reviews_collection = db["reviews"]
        products_collection = db["products"]
        amazon_reviews_collection = db["amazonReviews"]
        amazon_product_collection = db["amazonProducts"]
        walmart_reviews_collection = db["walmartReviews"]
        walmart_product_collection = db["walmartProducts"]
        return (
            search_collection,
            reviews_collection,
            products_collection,
            amazon_reviews_collection,
            amazon_product_collection,
            walmart_reviews_collection,
            walmart_product_collection,
        )
    except ConnectionFailure:
        # print(f'MongoDB connection error. {e}'); #if failed to connect to mongoDB
        return ("", "", "", "", "", "", "")


# result = databaseConnection()
# print(result)
