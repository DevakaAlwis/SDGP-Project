import json

def convertToDictionary(temp_data):
    if(len(temp_data)==1):
        temp_data.update(temp_data)
    elif(len(temp_data)!=0):
        print(len(temp_data))
        # for i in temp_data:
        #     convertToDictionary(temp_data)


json_data ='{"offer": {"currency": "USD","price": 499.99},"request_parameters": {"epid": "325389825157","ebay_domain": "ebay.com"},"seller": {"name": "orkmastermcgee"},"product": {"rating": 4.8,"images": [{"link": "https://i.ebayimg.com/images/g/3G8AAOSwNslhoSZW/s-l1600.jpg"},{"link": "https://i.ebayimg.com/images/g/4~MAAOSwC7Vh4JaJ/s-l1600.jpg"}],"review_count": 3214,"title": "PS5 Sony PlayStation 5 Console Disc Version!"}}'

#parsed_json
parsed_json = json.loads(json_data)     #convert the json data string to dictionary 
convertToDictionary(parsed_json)

#nested dict remove the nested
    #multi nested dict
#create a single dict  
#relavent data gathering 
    #validation the data
#add the relavent data to variable (print)

#insert to the db


data={}
if(data.get("epid") or data.get("id")):
    if(data.get("epid")):
        data={}



# data={"currency": "USD","price": 499.99,"epid": "325389825157","ebay_domain": "ebay.com"}
# for i in parsed_json:
#     print(parsed_json.get(i))
#     convertToDictionary(parsed_json.get(i))

# print(data)



    # print(len(x))
    # print(x)
    # print(len(i))
# print(type(parsed_json))


# if()

# epid = parsed_json["request_parameters"]["epid"]
# ebay_domain = parsed_json["request_parameters"]["ebay_domain"]
# currency = parsed_json["offer"]["currency"]
# price = parsed_json[""]["price"]
# title = parsed_json["product"]["title"]
# review_rating = parsed_json["product"]["rating"]
# review_count = parsed_json["product"]["review_count"]
# images = parsed_json["product"]["images"]
# seller_name = parsed_json["seller"]["name"]

# print("EPID:", epid)
# print("Ebay Domain:", ebay_domain)
# print("Currency:", currency)
# print("Price:", price)
# print("Title:", title)
# print("Review_rating:", review_rating)
# print("Review_count:", review_count)
# print("Images:", images)
# print("Seller Name:", seller_name)