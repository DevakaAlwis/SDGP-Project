import joblib
import pymongo
import numpy as np
from pymongo.errors import WriteError
from database_connection import db, product_collection

def runTrustWorthyScoreModel():

    #product Collection
 
    products = product_collection.find()

    try:
        #loading the trustworth score model
        loaded_rf_model = joblib.load('D:/sentiment_model/rf_model.sav')
    except FileNotFoundError as e:
        print(f'Unable to load model. {e}' )

    #run the model to each iteration
    for product in products:
        item_id = product['_id']
        try:
            reviewCount= product['foundReviewCount']
        except KeyError as e:
            print(f'No review counts found. {e}')
            break    
        trustworth_score = 0
        #if the review count is 0 trustworthscore is 0
        if(reviewCount!=0):
            features = [[product['foundReviewRating'],product['foundReviewCount'], product['positiveReviews'],product['neutralReviews'],product['negativeReviews']]]
            trustworth_score = loaded_rf_model.predict(features)
            trustworth_score = round(float(trustworth_score[0]), 1)

        print("trustworth_score: ",trustworth_score," | reviewText: ",product['positiveReviews'],product['neutralReviews'],product['negativeReviews'])
        print()
        try:
            product_collection.update_one({"_id":item_id}, {'$set': {'TrustworthyScore': trustworth_score}})
        except WriteError as e:
            print(f'An error occured while reading data from collection {e}')   


runTrustWorthyScoreModel()

