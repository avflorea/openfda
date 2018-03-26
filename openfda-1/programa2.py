import http.client
import json
headers = {'User-Agent': 'http-client'}

# Nos conectamos con el servidor
conn = http.client.HTTPSConnection("api.fda.gov")

# Enviamos un mensaje de solicitud con el GET y el recurso seguido de un limite
# que será el número de medicamentos que queremos que aparezcan en pantalla, en este caso 10
conn.request("GET", "/drug/label.json?&limit=10", None, headers)

# Leemos el mensaje de respuesta recibido del servidor
info = conn.getresponse()

print(info)

# Imprimimos la linea del estado de respuesta
print(info.status, info.reason)

# Leemos el contenido de la respuesta y lo convertimos a una cadena
repos_raw = info.read().decode("utf-8")

# Imprimimos ese fichero que ha sido recibido
datos = json.loads(repos_raw)

# Imprimimos la id de los 10 medicamentos utilizando un bucle
# Recorremos los valores del diccionario hasta llegar al 'id', que es cuando imprimimos por pantalla
for element in datos['results']:
    print("El identificador es: ",element['id'])

conn.close()