import socket
import http.client
import json

# Configuracion del servidor: IP, Puerto
IP = "192.168.1.133"
PORT = 8081
MAX_OPEN_REQUESTS = 5

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?&limit=20", None, headers)

info = conn.getresponse()
print(info.status, info.reason)

repos_raw = info.read().decode("utf-8")

datos = json.loads(repos_raw)
for elem in datos['results']:
     datos2 = (elem['id'])

def process_client(clientsocket):
    """Funcion que atiende al cliente. Lee su peticion (aunque la ignora)
       y le envia un mensaje de respuesta en cuyo contenido hay texto
       en HTML que se muestra en el navegador"""

    # Leemos a traves del socket el mensaje de solicitud del cliente
    # Pero no hacemos nada con el. Lo descartamos: con independencia de
    # lo que nos pida, siempre le devolvemos lo mismo

    mensaje_solicitud = clientsocket.recv(1024)

    # Empezamos definiendo el contenido, porque necesitamos saber cuanto
    # ocupa para indicarlo en la cabecera
    # En este contenido pondremos el texto en HTML que queremos que se
    # visualice en el navegador cliente
    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: white'>
        <h1>Hola! Soy Andreea!
        Que tal estas? </h2>
        <p></p>
      </body>
      </html>
    """



    # -- Indicamos primero quetodo OK Cualquier peticion, aunque sea
    # -- incorrecta nos va bien (somos un servidor cutre...)
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    # -- Creamos el mensaje uniendo todas sus partes
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


# -----------------------------------------------
# ------ Aqui comienza a ejecutarse el servidor
# -----------------------------------------------

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")