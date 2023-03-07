import http.client
import json
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["proRev_analyer_db"]
collection = db["ebayProductDetailCollection"]



conn = http.client.HTTPSConnection("countdown4.p.rapidapi.com")
RapidAPI_Key = "82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13"
#devaka X-RapidAPI-Key: 4c4dfc7bdbmshef48b2595442f89p107fd0jsn752e6f421f8f
#livini X-RapidAPI-Key: 82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13
headers = {
    'X-RapidAPI-Key': RapidAPI_Key,
    'X-RapidAPI-Host': "countdown4.p.rapidapi.com"
    }
epid="325389825157"
conn.request("GET", "/request?type=product&ebay_domain=ebay.com&epid="+epid, headers=headers)

response = conn.getresponse()

json_data = response.read()
print(type(json_data))
data=json_data.decode("utf-8")
print(type(data))
stringdata = json.loads(data)
print(type(stringdata))
epid = stringdata["request_parameters"]["epid"]
ebay_domain = stringdata["request_parameters"]["ebay_domain"]
# currency = stringdata["offer"]["currency"]
# price = stringdata["offer"]["price"]
title = stringdata["product"]["title"]
review_rating = stringdata["product"]["rating"]
review_count = stringdata["product"]["review_count"]
images = stringdata["product"]["images"]
seller_name = stringdata["seller"]["name"]

print("EPID:", epid)
print("Ebay Domain:", ebay_domain)
# print("Currency:", currency)
# print("Price:", price)
print("Title:", title)
print("Review_rating:", review_rating)
print("Review_count:", review_count)
print("Images:", images)
print("Seller Name:", seller_name)



# Extract only the data fields you want
# desired_fields = [epid, ebay_domain, currency, price, currency, title, review_rating, review_count, images, seller_name]
# filtered_data = {field: data[field] for field in desired_fields if field in data}

# Insert the filtered data into MongoDB
# collection.insert_one(filtered_data)

# Use the filtered data as needed
# print(filtered_data)