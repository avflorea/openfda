import http.client
import json

lista_drogas = []
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic+acid"&limit=100', None, headers)
info = conn.getresponse()
print(info.status, info.reason)
drogas_raw = info.read().decode("utf-8")
datos = (json.loads(drogas_raw))

for elem in range(len(datos['results'])):
    info_drogas = datos['results'][elem]
    if (info_drogas['openfda']):
        lista_drogas.append(info_drogas['openfda']['manufacturer_name'][0])
        print("Fabricantes que producen aspirinas son: ",lista_drogas)
    else:
        continue

conn.close()