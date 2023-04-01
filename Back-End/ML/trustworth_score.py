import joblib
from pymongo.errors import WriteError


# function to run the trust worthy score to the products and save it to the collection
def runTrustWorthyScoreModel(product_collection):

    # getting product Collection
    products = product_collection.find()
    statement = ''
    load = False

    try:
        # loading the trustworth score model
        loaded_rf_model = joblib.load('model/trustworthyScore_RFModel.sav')
        load = True
        statement = 'trustworthy score model loaded successfully.'
    except FileNotFoundError:
        statement = 'Unable to load model.'
        load = False

    if (load):
        # run the model to each iteration
        for product in products:
            # getting the product id
            item_id = product['_id']
            reviewCount = 0
            # checking if the reviwcount is there and getting it
            try:
                reviewCount = product['foundReviewCount']
            except KeyError:
                statement = 'No review counts found.'
            trustworth_score = 0
            # if the review count is 0 trustworthscore is 0
            if (reviewCount != 0):
                features = [[product['foundReviewRating'], product['foundReviewCount'],
                            product['positiveReviews'], product['neutralReviews'], product['negativeReviews']]]
                trustworth_score = loaded_rf_model.predict(features)
                trustworth_score = round(float(trustworth_score[0]), 1)
                print(trustworth_score)
            # updating the products collection
            try:
                product_collection.update_one(
                    {"_id": item_id}, {'$set': {'TrustworthyScore': trustworth_score}})
                statement = 'Trustworthy Score added to the products collection sucessfully.'

            except WriteError:
                statement = 'An error occured while updating data to collection.'
    return statement


# result=runTrustWorthyScoreModel()
# print(result)
