import joblib
from pymongo.errors import WriteError

# function to run the setiment label model to reviews and update the reviews collection with the sentiment label


def runSentimentLabelModel(reviews_collection):
    # review Collection
    reviews = reviews_collection.find()

    statement = ""
    # exiting the function if collection is empty
    if reviews_collection.count_documents({}) == 0:
        statement = "No reviews found in the collection"
        return statement

    load = False
    try:
        # loading sentiment model and vectorizer
        loaded_svm_model = joblib.load("sentimentLabel_svmModel.sav")
        loaded_vectorizer = joblib.load("sentimentVectorizer.pk1")
        statement = "Sentiment label model loaded successfully."
        load = True
    except FileNotFoundError:
        statement = "Unable to load model."
        load = False

    if load:
        # run the model to each iteration
        for review in reviews:
            # get the product id
            item_id = review["_id"]
            error = 0
            # transfroming  review text from vectorizer and predicting sentiment label from the model
            try:
                transformed_text = loaded_vectorizer.transform(
                    [review["reviewText"]]
                ).toarray()
                sentiment_prediction = loaded_svm_model.predict(transformed_text)[0]
            except Exception:
                # if model fails to label the review
                error += 1
                statement = "Error labeling the model. With", str(error), " errors."
                continue

            # print("Label: ",sentiment_prediction," | reviewText: ",review['reviewText'])
            # updating field in my collction to add sentiment count
            try:
                reviews_collection.update_one(
                    {"_id": item_id}, {"$set": {"sentimentLabel": sentiment_prediction}}
                )
                statement = (
                    "Sentiment Label added to the reviews sucessfully.",
                    str(error),
                    " errors.",
                )
            except WriteError:
                statement = (
                    " An error ocured while updating the database",
                    str(error),
                    " errors.",
                )
                error += 1
    return statement


# result = runSentimentLabelModel()
# print(result)
