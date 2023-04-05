import unittest
from unittest.mock import Mock, patch

import joblib
import numpy as np
from pymongo.errors import WriteError
from trustworth_score import runTrustWorthyScoreModel


class TestrunTrustWorthyScoreModel(unittest.TestCase):
    def setUp(self):
        # create a mock product
        self.product = {
            "_id": "123",
            "foundReviewRating": 4.5,
            "foundReviewCount": 10,
            "positiveReviews": 8,
            "neutralReviews": 1,
            "negativeReviews": 1,
        }

        # creating a mock product collection
        self.product_collection = Mock()
        self.product_collection.find.return_value = [self.product]

        # creating a mock loaded model
        self.loaded_rf_model = Mock()
        self.loaded_rf_model.predict.return_value = np.array([90])

    # function to test model load failure
    def test_model_load_fail(self):
        with patch("joblib.load", side_effect=FileNotFoundError("Model not found")):
            # calling the function that is tested
            output = runTrustWorthyScoreModel(self.product_collection)
            # asserting the function returns ecpected result
            self.assertEqual(output, "Unable to load model.")

    def test_trustscore_values(self):
        products = self.product_collection.find()
        loaded_rf_model = joblib.load("TrustScore_RfModel.sav")
        for product in products:
            item_id = product["_id"]
            try:
                reviewCount = product["foundReviewCount"]
            except KeyError as e:
                self.fail(f"No review counts found. {e}")
                break
            trustworth_score = 0
            # if the review count is 0 trustworthscore is 0
            if reviewCount != 0:
                features = [
                    [
                        product["foundReviewRating"],
                        product["foundReviewCount"],
                        product["positiveReviews"],
                        product["neutralReviews"],
                        product["negativeReviews"],
                    ]
                ]
                trustworth_score = loaded_rf_model.predict(features)
                trustworth_score = round(float(trustworth_score[0]), 1)
            self.assertGreaterEqual(trustworth_score, 0)
            self.assertLessEqual(trustworth_score, 100)
            try:
                self.product_collection.update_one(
                    {"_id": item_id}, {"$set": {"TrustworthyScore": trustworth_score}}
                )
            except WriteError as e:
                self.fail(f"An error occured while reading data from collection {e}")


if __name__ == "__main__":
    unittest.main()
