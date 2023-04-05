# SDGP-Project
2nd Year Software Development GroupProject 2022/2023

## Project Name: ProRev-Analyzer
## Description
An extension and a web application that allow users to compare e-commerce sites (Amazon and Walmart) products with reviews rating and provide a reputable trustworthy score with a product summary feedback (number of positive, negative, neutral reviews) so that the customer can decided which product is suitable to him/her.

The Application use scraping technic to data gather and processed through two machine learning models, which gives a sentiment label for each product review using SVC Linear Classifier Analgorithm and combine all the reviews for a particular product and give a overall trustworthy score using the Random Forest Regrassion.

## 👉 Install dependencies

### ✨ Windows
```bash
python -m venv env
env\Scripts\activate 
pip install -r requirements.txt
```

### ✨ OS
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 👉 Start the App

```bash
cd app    #move to the app folder
python app.py
```

### 👉 Adding the Extension

STEP 01: Open the chrome brower
STEP 02: Click the manage extension
STEP 03: Turn on the Developer Mode from the TOP RIGHT side
STEP 04: Click Load Unpack
STEP 05: Go to the project file location
         SDGP-PROJECT -> app -> extension
STEP 06: SELECT the extension folder

## ✨ HOW TO USE THE EXTENSION
Amazon:
    Visit the amazon page and select a product. Once the browser is loaded click on the extension
Walmart:
    Visit the walmart page and select a product. RELOAD the page once the product page is visible and click in the extension

## ✨ IMPORTANT
### Before clicking the extension page "view similar products" button RUN the app.py
It will take a will to load to the similar product page.

## ✨ HOW TO USE THE SITE
Run the app.py and click the URL "http://127.0.0.1:5000" to go to the HOME page.
Enter a product name in the search bar to view similar products.
It will take a will to load to the similar product page.

### Pages Created
Home page - index.html
Loading page - loading.html
About us page - about.html
Similar products page - page.html

### Note
It will take some time to gather data and process and display.
#### When using extension after clicking the 'view similar products' button DON'T move to a new page or a browser the similar product page WILL NOT be loaded. but the process will be happening in the backend. You can see the output once the backend process is done. and by going to the  "http://127.0.0.1:5000/page"

## Similar products page
"http://127.0.0.1:5000/page"
about link will be the similar products page


## ✨ Codebase structure

The project has a simple structure, represented as bellow:

```bash
< PROJECT ROOT >
   |
   |-- .github
   |    |-- workflows
   |    |    |-- superlinter.yml                # CI  
   |-- app/                                     # main app part
   |    |-- database/                           # database part
   |    |    |-- __init__.py
   |    |    |-- database_connection.py         # database connection
   |    |    |-- merging_collections.py         # margin product and reviews collection
   |    |    |-- product_Update_db.py           # score update
   |    |-- extension/
   |    |    |-- css/                           
   |    |    |   |-- popup.css                  # extension css
   |    |    |-- images/
   |    |    |-- scripts/
   |    |    |   |-- content.js                 # web page script
   |    |    |-- background.js                  # background
   |    |    |-- manifest.json                  # extension config
   |    |    |-- popup.html                     # extension html
   |    |    |-- popup.js                       # extension js
   |    |-- model/ 
   |    |    |-- notebooks
   |    |    |   |-- Creating_2000000_rows_review_datasets.ipynb                    # reviews dataset creation part
   |    |    |   |-- Creating_trustworth_score_dataset_using_product_reviews.ipynb  # trustworthy score dataset creation part
   |    |    |   |-- labeling_for_sentiment_reviews_in_csv.ipynb                    # labeling reviews part
   |    |    |   |-- Sentiment_labelModel.ipynb                                     # sentiment ML part
   |    |    |   |-- trustworthy_score_model.ipynb                                  # trustworthy ML part
   |    |    |-- __init__.py
   |    |    |-- sentiment_label.py             # sentiment label part      
   |    |    |-- sentimentLabel_svmModel.sav    # sentiment label ML model part 1
   |    |    |-- sentimentVectorizer.pk1        # sentiment label ML model part 2
   |    |    |-- test_sentiment_label.py        # sentiment label testing part
   |    |    |-- test_tustworth_score.py        # test tustworth score testing part
   |    |    |-- TrustScore_RfModel.sav         # test tustworth score ML model part
   |    |    |-- trustworth_score.py            # trustworth score part
   |    |-- static/
   |    |    |-- css                            # website css folder
   |    |    |-- images                         # website images folder
   |    |-- templates/              
   |    |    |-- about.html                     # about page
   |    |    |-- index.html                     # home page
   |    |    |-- loading.html                   # loading page
   |    |    |-- page.html                      # similar product page
   |    |-- webscrape/ 
   |    |    |-- spriders/  
   |    |    |    |-- __init__.py 
   |    |    |    |-- amazon_reviews.py         # amazon reviews spider
   |    |    |    |-- amazon_search.py          # amazon product search spider
   |    |    |    |-- walmart_reviews.py        # walmart reviews spider
   |    |    |    |-- walmart_search.py         # walmart product search spider
   |    |    |-- __init__.py
   |    |    |-- items.py                       # creating class for items that are scrape 
   |    |    |-- middlewares.py                 # middleware part
   |    |    |-- pipelines.py                   # pipeline to save the details
   |    |    |-- settings.py                    # config the spiders settings
   |    |-- __init__.py
   |    |-- app.py                              # flask routes main file
   |    |-- scrapy.cfg                          # scrapy cfg
   |-- env/                                     # vertual env
   |-- .env                                     # API keys secure
   |-- .eslintignore                            # eslintignore extension part
   |-- .gitignore                               # gitignore
   |-- build.sh                                 # database part
   |-- LICENSE
   |-- README.md                                # readme file
   |-- requirements.txt                         # requirements file
   |
   |-- ************************************************************************
