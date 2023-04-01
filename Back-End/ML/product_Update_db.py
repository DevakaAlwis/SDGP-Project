import pymongo
from pymongo.errors import CollectionInvalid, WriteError, OperationFailure
from database_connection import db, reviews_collection, product_collection


def updateSentimentLabels():

    try:
        # reviews Collection
        reviews = reviews_collection.find()

        # product Collection
        products = product_collection.find()
    except CollectionInvalid as e:
        print(f'Collection not available {e}')

    # update the values
    for product in products:
        productID = product["productId"]
        item_id = product['_id']
        positive = 0
        neutral = 0
        negative = 0
        foundReviewCount = 0
        foundReviewsRating = 0
        for review in reviews:
            foundReviewCount += 1  # calculate found review count
            reviewRating = review["reviewRating"]
            # calculate found review rating
            foundReviewsRating += float(review["reviewRating"])
            sentimentLabel = review["sentimentLabel"]
            if (sentimentLabel == "positive"):
                positive += 1
            elif (sentimentLabel == "neutral"):
                neutral += 1
            elif (sentimentLabel == "negative"):
                negative += 1
        averageReviewRating = 0

        # zore division error validation
        if (foundReviewCount != 0):
            # calculate the average of the review rating
            averageReviewRating = round(foundReviewsRating/foundReviewCount, 1)

        try:
            product_collection.update_one(
                {"_id": item_id}, {'$set': {'positiveReviews': positive}})
            product_collection.update_one(
                {"_id": item_id}, {'$set': {'neutralReviews': neutral}})
            product_collection.update_one(
                {"_id": item_id}, {'$set': {'negativeReviews': negative}})
            product_collection.update_one(
                {"_id": item_id}, {'$set': {'foundReviewCount': foundReviewCount}})
            product_collection.update_one(
                {"_id": item_id}, {'$set': {'foundReviewRating': averageReviewRating}})
            print("foundReviewCount: ", foundReviewCount, " | positive: ", positive, " | neutral: ",
                  neutral, " | negative: ", negative, " | averageReviewRating: ", averageReviewRating)
        except WriteError as e:
            print(f' An error ocured while updating the database {e}')
        except OperationFailure as e:
            print(f'An error occured while reading data from collection {e}')


updateSentimentLabels()
