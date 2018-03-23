import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=results.openfda:spl_id&limit=100", None, headers)

id = conn.getresponse()

for element in id:
    print(element)

print(id)
