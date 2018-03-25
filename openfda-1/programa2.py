import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=20", None, headers)

info = conn.getresponse()

print(info)


print(info.status, info.reason)

repos_raw = info.read().decode("utf-8")

datos = dict(json.loads(repos_raw))

for element in datos:
    print(datos['results'][0]['id'])
#for element in info:#datos['results'][0]['id']:
 #   print(element)

conn.close()