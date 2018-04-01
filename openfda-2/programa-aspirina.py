import http.client
import json

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic+acid"&limit=100', None, headers)
info = conn.getresponse()
print(info.status, info.reason)
drogas_raw = info.read().decode("utf-8")
datos = (json.loads(drogas_raw))

try:
    for element in datos['results']:
        print("Fabricantes que producen aspirinas son: ",element['openfda']['manufacturer_name'])
        continue
except KeyError:
    print("No tenemos datos del fabricante de este medicamento")
conn.close()