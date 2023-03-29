import joblib
import pymongo
from pymongo.errors import WriteError
from database_connection import db, reviews_collection

def runSentimentLabelModel():


    #review Collection
    reviews = reviews_collection.find();

    #exiting the function if collection is empty
    if reviews_collection.count_documents({}) == 0:
        print('No reviews found in the collection')
        return;

    try:
        # loading sentiment model and vectorizer
        loaded_svm_model = joblib.load('sentimentLabel_svmModel.sav');
        loaded_vectorizer = joblib.load('sentimentVectorizer.pk1');
    except FileNotFoundError as f:
        print(f'Unable to load model {f}');

    #run the model to each iteration
    for review in reviews:
        item_id = review['_id'];

        #transfroming  review text from vectorizer and predicting sentiment label from the model
        try:
            transformed_text = loaded_vectorizer.transform([review['reviewText']]).toarray();
            sentiment_prediction = loaded_svm_model.predict(transformed_text)[0];
        except Exception as e:
            print(f'Error labeling the model. {e}'); #if model fails to label the review
            continue;   

        print("Label: ",sentiment_prediction," | reviewText: ",review['reviewText']);
        # updating field in my collction to add sentiment count
        try:
            reviews_collection.update_one({"_id":item_id}, {'$set': {'sentimentLabel2': sentiment_prediction}});
        except WriteError as e:
            print(f' An error ocured while updating the database {e}');


runSentimentLabelModel();





