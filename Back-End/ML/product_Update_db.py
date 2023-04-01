import pymongo
from pymongo.errors import CollectionInvalid, OperationFailure, WriteError

# function to update the sentiment sentiment label to number of positive, negetive, neutral reviews, number of reviews found, and it's rating to products collection


def updateSentimentLabels(reviews_collection, product_collection):
    statement = ""
    try:
        # product Collection
        products = product_collection.find()
        statement = "Product collection access sucessfully."
    except CollectionInvalid as e:
        statement = 'Collection not available.'

    # update the values
    for product in products:
        productID = product["productId"]
        item_id = product['_id']
        positive = 0
        neutral = 0
        negative = 0
        foundReviewCount = 0
        foundReviewsRating = 0
        averageReviewRating = 0
        try:
            # reviews Collection
            reviews = reviews_collection.find()
            statement = "Reviews collection access sucessfully."
        except CollectionInvalid as e:
            statement = 'Collection not available.'

        for review in reviews:
            if (review["productId"] == productID):
                # print(review["productId"])
                foundReviewCount += 1  # calculate found review count
                # reviewRating = review["reviewRating"]
                # calculate found review rating
                foundReviewsRating += float(review["reviewRating"])
                sentimentLabel = review["sentimentLabel"]
                if (sentimentLabel == "positive"):
                    positive += 1
                elif (sentimentLabel == "neutral"):
                    neutral += 1
                elif (sentimentLabel == "negative"):
                    negative += 1

        # zore division error validation
        if (foundReviewCount != 0):
            # calculate the average of the review rating
            averageReviewRating = round(foundReviewsRating/foundReviewCount, 1)
        statement = "productID: ", productID, " | foundReviewCount: ", foundReviewCount, " | positive: ", positive, " | neutral: ", neutral, " | negative: ", negative, " | averageReviewRating: ", averageReviewRating

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
            statement = "Products added to the collection."

            print("foundReviewCount: ", foundReviewCount, " | positive: ", positive, " | neutral: ",
                  neutral, " | negative: ", negative, " | averageReviewRating: ", averageReviewRating)
        except WriteError as e:
            statement = ' An error ocured while updating the database.'
        except OperationFailure as e:
            statement = 'An error occured while reading data from collection.'
    return (statement)


# updateSentimentLabels()
