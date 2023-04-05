import unittest
from unittest.mock import patch, Mock

from sentiment_label import runSentimentLabelModel


class TestrunSentimentLabelModel(unittest.TestCase):

    def setUp(self):
        self.reviews_collection = Mock()

    # test function that test wether correct message is given when colletion is empty

    def test_collection_empty(self):
        self.reviews_collection.count_documents.return_value = 0
        output = runSentimentLabelModel(self.reviews_collection)
        self.assertEqual(output, "No reviews found in the collection")

    # test function to test model load failure

    def test_model_load_fail(self):
        with patch("joblib.load", side_effect=FileNotFoundError("Model not found")):
            # calling the function that is tested
            output = runSentimentLabelModel(self.reviews_collection)
            # asserting the function returns ecpected result
            self.assertEqual(output, "Unable to load model.")

    # test function that test if correct messege is given when product update is empty

    # def test_update_field_failiure(self):
    #     self.reviews_collection.count_documents.return_value = 1
    #     self.reviews_collection.find.return_value = [
    #         {'_id': '1', 'reviewText': 'This is a great product.'}]
    #     self.reviews_collection.update_one.side_effect = WriteError('Update failed')
    #     result = runSentimentLabelModel(self.reviews_collection)
    #     self.assertEqual(result, ' An error ocured while updating the database, 0 errors.')


if __name__ == "__main__":
    unittest.main()
