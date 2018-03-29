import http.client
import json
lista_drogas = [] #Creamos una lista vacia donde añadiremos los datos de los medicamentos

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
drogas_raw = info.read().decode("utf-8")

# Imprimimos ese fichero que ha sido recibido
datos = json.loads(drogas_raw)

# Imprimimos la id de los 10 medicamentos utilizando un bucle
# Recorremos la lista de 'results', en este caso 10 veces por el limite que hemos añadido
for elem in range(len(datos['results'])):
    info_drogas = datos['results'][elem] # Creamos una lista con cada medicamento
    if (info_drogas['id']): # Cuando encuentre el 'id' añade esa informacion a la lista del principio
        lista_drogas.append(info_drogas['id'])
        print("El identificador es:", lista_drogas[elem]) # Imprime el 'id' de cada elemento
    else:
        continue

conn.close()