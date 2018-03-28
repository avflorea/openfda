import socket
import http.client
import json

# Configuracion del servidor: IP, Puerto
IP = "192.168.1.134"
PORT = 8080
MAX_OPEN_REQUESTS = 5
def introduce_datos():
    lista_drogas = []
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?&limit=20", None, headers)
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    datos = (json.loads(drogas_raw))
    for i in range(len(datos['results'])):
        info_drogas = datos['results'][i]
        if (info_drogas['openfda']):
            lista_drogas.append(info_drogas['openfda']['generic_name'][0])
            print(lista_drogas[i-1])
        else:
            continue


def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024)

    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: white'>
        <h1>Bienvenid@ </h1>
        <h2> Medicamentos </h2>
    """
    for i in range(len(introduce_datos())):
        contenido += i
        contenido += """</body></html>"""

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

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