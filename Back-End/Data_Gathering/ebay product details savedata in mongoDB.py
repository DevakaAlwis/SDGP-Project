import http.client
import json
import pymongo

# # Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["proRev_analyer_db"]
# collection = db["ebayProductDetailCollection"]

#rapid API
conn = http.client.HTTPSConnection("countdown4.p.rapidapi.com")
RapidAPI_Key = "82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13"
#devaka X-RapidAPI-Key: 4c4dfc7bdbmshef48b2595442f89p107fd0jsn752e6f421f8f
#livini X-RapidAPI-Key: 82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13
headers = {
    'X-RapidAPI-Key': RapidAPI_Key,
    'X-RapidAPI-Host': "countdown4.p.rapidapi.com"
    }

epid="334500445571"

conn.request("GET", "/request?type=product&ebay_domain=ebay.com&epid="+epid, headers=headers)

response = conn.getresponse()

json_data = response.read()


# json_data ='{"aasd":12,"offer": {"1": {"2": {"3": "31"},"22": 2},"currency": "USD","price": 499.99},"request_parameters": {"epid": "325389825157","ebay_domain": "ebay.com"},"seller": {"name": "orkmastermcgee"},"product": {"rating": 4.8,"images": [{"link": "https://i.ebayimg.com/images/g/3G8AAOSwNslhoSZW/s-l1600.jpg"},{"link": "https://i.ebayimg.com/images/g/4~MAAOSwC7Vh4JaJ/s-l1600.jpg"}],"review_count": 3214,"title": "PS5 Sony PlayStation 5 Console Disc Version!"},"reviews": {"helpful_votes": 13,"rating": 5,"date": {"utc": "2022-10-06T00:00:00.000Z","raw": "Oct 06, 2022"},"id": "10000000308190262","unhelpful_votes": 0,"attributes": [{"value": "Yes","name": "Verified purchase:"},{"value": "orkmastermcgee","name": "Sold by:"}],"body": "This is cofor me. Well it stith","title": "Best gaming console truly a next generation console"}}'


# #parsed_json
parsed_json = json.loads(json_data)     #convert the json data string to dictionary 

data={}

def s(key,json_list):
    value=json_list.get(key)
    if(type(value)!=dict):
        print(key," : ",value)
        data[key]=value
    else:
        for new_key in value:
            new_value=json_list.get(key)
            if(type(new_value)!=dict):
                print(new_key," : ",new_value)
                data[new_key]=new_value
            else:
                s(new_key,new_value)

for i in parsed_json:
    # print(i)
    s(i,parsed_json)

print(data)


# # Extract only the data fields you want
# desired_fields = ["epid", "ebay_domain", "currency", "price", "currency", "title", "review_rating", "review_count", "images", "seller_name"]
# filtered_data = {field: data[field] for field in desired_fields if field in data}

# # Insert the filtered data into MongoDB
# collection.insert_one(filtered_data)

# # Use the filtered data as needed
# print(filtered_data)





