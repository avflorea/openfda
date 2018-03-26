import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)

info = conn.getresponse()

print(info)

print(info.status, info.reason)
repos_raw = info.read().decode("utf-8")

datos = json.loads(repos_raw)

for element in datos['results']:
    print("El identificador es: ",element['id'])



conn.close()