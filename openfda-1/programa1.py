import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=20", None, headers)

info = dict(conn.getresponse())
# craear diccionario donde introducimos el json y de ahi leemos

print(info.status, info.reason)
repos_raw = info.read().decode("utf-8")
conn.close()

datos = json.loads(repos_raw)

for element in datos:
    print(element)
    print("El identificador es", element['results'][0]['id'])
    print("El proposito del producto es", element['results'][0]['purpose'])
    print("El nombre del fabricante es", element['results'][0]['openfda']['manufacturer_name'])

print(info)
conn.close()