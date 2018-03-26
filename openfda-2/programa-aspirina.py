import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=100", None, headers)

info = conn.getresponse()

print(info)

print(info.status, info.reason)

repos_raw = info.read().decode("utf-8")

datos = json.loads(repos_raw)

print(datos['results'][0]['openfda']['manufacturer_name'])
if "aspirin" in datos:
    #for element in datos['results']['openfda']:
    print(datos['results'][0]['openfda']['manufacturer_name'])
#for element in datos['results']:

 #   print(element, datos['results'][0]['id'])


conn.close()