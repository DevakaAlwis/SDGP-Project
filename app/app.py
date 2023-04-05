import subprocess

import pymongo
from database import database_connection,merging_collections,product_Update_db
from flask import Flask, render_template, redirect, url_for, request, jsonify
from model import sentiment_label,trustworth_score

app = Flask(__name__)


# route for the index page
@app.route('/')
def index():
    return render_template('index.html')


# route for about page
@app.route('/about')
def about():
    return render_template('about.html')


# route for the page page
@app.route('/page')
def page():
    (
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    ) = database_connection.databaseConnection()
    products = products_collection.find()
    return render_template('page.html',products=products)


# route for the findProducts page when Extension button clicked
@app.route('/findProducts' , methods=["POST","GET"])
def findProducts():

    product = request.json  # access the request body and make it a python dictonary
    searchName = product["name"]
    searchProductId = product["id"]

    # call the dataconnection function to get the db connection
    (
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    ) = database_connection.databaseConnection()

    # delete previous collections
    removeCollections(
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    )

    # insert extension gathered product
    search_collection.insert_one({'productName':searchName})

    # call the process function to do the back-end part
    process(
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    )
    products = products_collection.find()

    return render_template('page.html',products=products)


# route for the search page when website keyword is searched
@app.route('/search', methods=['POST'])
def search():

    keyword = request.form.get('search-keyword')
    if(keyword == ""):
        return render_template('index.html')
    
    # call the dataconnection function to get the db connection
    (
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    ) = database_connection.databaseConnection()
    
    # delete previous collections
    removeCollections(
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    )

    # insert searched product
    search_collection.insert_one({'productName':keyword})

    # call the process function to do the back-end part
    process(
        search_collection,
        reviews_collection,
        products_collection,
        amazon_reviews_collection,
        amazon_products_collection,
        walmart_reviews_collection,
        walmart_products_collection
    )
    products = products_collection.find()

    return render_template('page.html', products=products)


# function to remove the existing collections from the database
def removeCollections(
    search_collection,
    reviews_collection,
    products_collection,
    amazon_reviews_collection,
    amazon_products_collection,
    walmart_reviews_collection,
    walmart_products_collection
):
    # delete previous collections
    search_collection.drop()
    products_collection.drop()
    reviews_collection.drop()
    amazon_products_collection.drop()
    amazon_reviews_collection.drop()
    walmart_products_collection.drop()
    walmart_reviews_collection.drop()


# function to do the back end page
def process(
    search_collection,
    reviews_collection,
    products_collection,
    amazon_reviews_collection,
    amazon_products_collection,
    walmart_reviews_collection,
    walmart_products_collection
):
    # scrape the products
    # list of search spiders 
    spiders = ["amazon_search", "walmart_search"]
    # list of processes
    processes = []

    # run a for loop to call the spiders
    for spider in spiders:
        # cmd command list
        cmd = ["scrapy", "crawl", spider]
        # execute the commands in string
        process = subprocess.Popen(cmd)
        processes.append(process)

    for process in processes:
        process.wait()

    # scrape the reviews
    # list of review spiders 
    spiders = ["amazon_reviews", "walmart_reviews"]
    # list of processes
    processes = []

    # run a for loop to call the spiders
    for spider in spiders:
        # run a for loop to call the spiders
        cmd = ["scrapy", "crawl", spider]
        # execute the commands in string
        process = subprocess.Popen(cmd)
        processes.append(process)

    for process in processes:
        process.wait()

    # merging the product and reviews seperatly
    merging_collections.mergingProducts(
        products_collection,
        amazon_products_collection,
        walmart_products_collection
    )
    merging_collections.mergingProducts(
        reviews_collection,
        amazon_reviews_collection,
        walmart_reviews_collection
    )
    
    # call the runSentimentLabelModel to get the sentiment label
    result = sentiment_label.runSentimentLabelModel(reviews_collection)
    print(result)
    # call the updateSentimentLabels to update the products collection
    result = product_Update_db.updateSentimentLabels(
        reviews_collection, products_collection
    )
    print(result)
    # call the runTrustWorthyScoreModel to get the trustworth score
    result=trustworth_score.runTrustWorthyScoreModel(products_collection)
    print(result)

    # return redirect(url_for('page'))
  
    # return url_for(scrapeProducts)
    # return jsonify({'message': "JSON recived"}),200


if(__name__=="__main__"):
    app.run()