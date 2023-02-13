import http.client

conn = http.client.HTTPSConnection("countdown4.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "82dc2bcd88msh83a165b7cfc6adep125265jsn3ceb0a315a13",
    'X-RapidAPI-Host': "countdown4.p.rapidapi.com"
    }

conn.request("GET", "/request?type=search&ebay_domain=ebay.com&search_term=memory%20cards&page=2", headers=headers)

res = conn.getresponse()
data = res.read()

a = list(data.decode("utf-8"))
print(a[0])