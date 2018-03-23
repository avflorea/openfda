import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=results.openfda:spl_id&limit=1", None, headers)

id = conn.getresponse()
print(id.status, id.reason)
data1 = id.read()
for element in id:
    print(element)

print(data1)
conn.close()