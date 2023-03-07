import json

json_data ='{"aasd":12,"offer": {"1": {"2": {"3": "31"},"22": 2},"currency": "USD","price": 499.99},"request_parameters": {"epid": "325389825157","ebay_domain": "ebay.com"},"seller": {"name": "orkmastermcgee"},"product": {"rating": 4.8,"images": [{"link": "https://i.ebayimg.com/images/g/3G8AAOSwNslhoSZW/s-l1600.jpg"},{"link": "https://i.ebayimg.com/images/g/4~MAAOSwC7Vh4JaJ/s-l1600.jpg"}],"review_count": 3214,"title": "PS5 Sony PlayStation 5 Console Disc Version!"},"reviews": {"helpful_votes": 13,"rating": 5,"date": {"utc": "2022-10-06T00:00:00.000Z","raw": "Oct 06, 2022"},"id": "10000000308190262","unhelpful_votes": 0,"attributes": [{"value": "Yes","name": "Verified purchase:"},{"value": "orkmastermcgee","name": "Sold by:"}],"body": "This is cofor me. Well it stith","title": "Best gaming console truly a next generation console"}}'


#parsed_json
parsed_json = json.loads(json_data)     #convert the json data string to dictionary 

data={}

def s(key,json_list):
    value=json_list.get(key)
    if(type(value)!=dict):
        print(key," : ",value)
    else:
        for new_key in value:
            new_value=json_list.get(key)
            if(type(new_value)!=dict):
                print(new_key," : ",new_value)
            else:
                s(new_key,new_value)

for i in parsed_json:
    # print(i)
    s(i,parsed_json)