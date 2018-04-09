import http.client
import json

headers = {'User-Agent': 'http-client'}

# Nos conectamos con el servidor
conn = http.client.HTTPSConnection("api.fda.gov")
# Enviamos un mensaje de solicitud con el GET y el recurso seguido de un limite y buscamos con un search el
# principio activo que debe ser el acetilsalicidico
conn.request("GET", '/drug/label.json?&search=active_ingredient:"acetylsalicylic+acid"&limit=100', None, headers)
# Leemos el mensaje de respuesta recibido del servidor
info = conn.getresponse()
# Imprimimos la linea del estado de respuesta
print(info.status, info.reason)
# Leemos el contenido de la respuesta y lo convertimos a una cadena
drogas_raw = info.read().decode("utf-8")
# Imprimimos ese fichero que ha sido recibido
datos = (json.loads(drogas_raw))

# Al buscar el nombre del fabricante de los medicamentos que tienen ese principio activo nos saldran 4 resultados,
# de los cuales hay dos que se desconoce el nombre
for element in datos['results']:
    print("El medicamento de id:", element['id'])
    if element['openfda']:
        print("Tiene como fabricante:",element['openfda']['manufacturer_name'][0])
    else:
        print("No tenemos datos del fabricante de este medicamento")
        continue
conn.close()