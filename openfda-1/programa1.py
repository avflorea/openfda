import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=1", None, headers)

info = conn.getresponse()

for element in info:
    print(element)
    #print("El medicamento buscado es", element['results']['0']['id'])

print(info)
conn.close()