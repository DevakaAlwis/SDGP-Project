import pymongo
from pymongo.errors import ConnectionFailure

try:
    #Database connection
    client = pymongo.MongoClient('mongodb+srv://techwarriors:dSTHFzXdNc4aHXV@cluster0.0c2sc0t.mongodb.net/?retryWrites=true&w=majority');
    db = client["db"];

    #Connecting to Collections
    reviews_collection = db["reviewsN"];
    product_collection = db["productsN"]
except ConnectionFailure as e:
    print(f'MongoDB connection error. {e}'); #if failed to connect to mongoDB