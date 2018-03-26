import http.client
import json
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)

info = conn.getresponse()

print(info)

print(info.status, info.reason)
repos_raw = info.read().decode("utf-8")

datos = (json.loads(repos_raw))

for element in datos['results']:
    print(element, datos['results'][0]['id'])




#for element in datos:
 #   print(element, ":", datos[element])
  #  print(datos['results'][0]['id'])
#datos2 = datos.keys()
#datos3 = datos.values()


#elements = datos.items()
#for datos2,datos3 in datos.items():
 #   print(datos2,'-->',datos3)
#for element in datos['results'][0]:
 #   print(element)

#print(datos['results'][0]['id'])

conn.close()