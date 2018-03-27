import http.client
import json
headers = {'User-Agent': 'http-client'}

# Nos conectamos con el servidor dando por hecho que el puerto es 8000
conn = http.client.HTTPSConnection("api.fda.gov")

# Enviamos un mensaje de solicitud con el GET y el recurso seguido de un limite
# que será el número de medicamentos que queremos que aparezcan en pantalla
conn.request("GET", "/drug/label.json?&limit=1", None, headers)

# Leemos el mensaje de respuesta recibido del servidor
info = conn.getresponse()

print(info)

# Imprimimos la linea del estado de respuesta
print(info.status, info.reason)

# Leemos el contenido de la respuesta y lo convertimos a una cadena
drogas_raw = info.read().decode("utf-8")

# Imprimimos ese fichero que ha sido recibido
datos = json.loads(drogas_raw)

# Imprimimos la id, el proposito y el fabricante del medicamento
print("El identificador del medicamento es", datos['results'][0]['id'])
print("El propósito del producto es", datos['results'][0]['purpose'])
print("El nombre del fabricante es", datos['results'][0]['openfda']['manufacturer_name'])

conn.close()