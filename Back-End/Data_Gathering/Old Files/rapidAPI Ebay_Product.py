import http.client

conn = http.client.HTTPSConnection("countdown4.p.rapidapi.com")

RapidAPI_Key = "82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13"
#devaka X-RapidAPI-Key: 4c4dfc7bdbmshef48b2595442f89p107fd0jsn752e6f421f8f
#livini X-RapidAPI-Key: 82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13
headers = {
    'X-RapidAPI-Key': RapidAPI_Key,
    'X-RapidAPI-Host': "countdown4.p.rapidapi.com"
    }

conn.request("GET", "/request?type=product&ebay_domain=ebay.com&epid=233599133856", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
