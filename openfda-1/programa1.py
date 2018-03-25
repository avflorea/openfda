import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=20", None, headers)

info = conn.getresponse()
print(info)
print(info.status, info.reason)
repos_raw = info.read().decode("utf-8")

datos = json.loads(repos_raw)

print("El identificador es", datos['results'][0]['id'])
print("El proposito del producto es", datos['results'][0]['purpose'])
print("El nombre del fabricante es", datos['results'][0]['openfda']['manufacturer_name'])

conn.close()