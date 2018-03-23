import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "https://api.fda.gov/drug/event.json?search=results.openfda:spl_id&limit=100", None, headers)

id = conn.getresponse()

for element in id:
    print(element)

print(id)
