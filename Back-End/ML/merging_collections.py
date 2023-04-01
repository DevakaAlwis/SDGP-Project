import pymongo
from pymongo.errors import CollectionInvalid, OperationFailure, WriteError

# function to merge products with amazon and walmart collections
def mergingProducts(
        products_collection,amazon_product_collection,walmart_product_collection
        ):
    # empty string to return the statement
    statement = ""
    try:
        # amazon product Collection
        amazonProducts = amazon_product_collection.find()
        # for loop to add products to the collection
        for product in amazonProducts:
            products_collection.insert_one(product)
        statement = statement + "Amazon products added sucessfully."
    except CollectionInvalid as e:
        statement = statement + "No Amazon products added."
    try:
        # walamrt product Collection
        walmartProducts = walmart_product_collection.find()
        # for loop to add products to the collection
        for product in walmartProducts:
            products_collection.insert_one(product)
        statement = statement + "Walmart products added sucessfully."
    except CollectionInvalid as e:
        statement = statement + "No Walmart products added."
    return statement

def mergingReviews(
        reviews_collection,amazon_reviews_collection,walmart_reviews_collection
        ):
    # empty string to return the statement
    statement = ""
    try:
        # amazon review Collection
        amazonReviews = amazon_reviews_collection.find()
        # for loop to add products to the collection
        for review in amazonReviews:
            reviews_collection.insert_one(review)
        statement = statement + "Amazon Reviews added sucessfully."
    except CollectionInvalid as e:
        statement = statement + "No Amazon Reviews added."
    try:
        # walamrt review Collection
        walmartReviews = walmart_reviews_collection.find()
        # for loop to add products to the collection
        for review in walmartReviews:
            reviews_collection.insert_one(review)
        statement = statement + "Walmart reviews added sucessfully."
    except CollectionInvalid as e:
        statement = statement + "No Walmart reviews added."
    return statement