import socket
import http.client
import json

# Configuramos el servidor: IP, Puerto
IP = "212.128.255.131"
PORT = 8088
# Determinamos el maximo de peticiones que puede realizar el cliente
MAX_OPEN_REQUESTS = 5
headers = {'User-Agent': 'http-client'}
# Hacemos que el cliente se conecte con el servidor
conn = http.client.HTTPSConnection("api.fda.gov")
# Enviamos un mensaje de solicitud con el GET y el recurso seguido de un limite
conn.request("GET", "/drug/label.json?&limit=11", None, headers)
# Leemos el mensaje de respuesta recibido del servidor
info = conn.getresponse()
# Imprimimos la linea del estado de respuesta
print(info.status, info.reason)
# Leemos el contenido de la respuesta y lo convertimos a una cadena
drogas_raw = info.read().decode("utf-8")
# Imprimimos ese fichero que ha sido recibido
datos = (json.loads(drogas_raw))

# Creamos una funcion que permite atender al cliente, lee la peticion que recibe a pesar
# de que luego la ignore y le envia un mensaje de respuesta. En ese contenido encontramos
# un texto HTML que se muestra en el navegador
def process_client(clientsocket):

    # Se lee el socket a traves del mensaje de solicitud del cliente. Independientemente
    # de lo que el cliente pida, siempre va a recibir el mismo mensaje
    mensaje_solicitud = clientsocket.recv(1024)

    # Introducimos el texto en HTML para que aparezca en la pantalla del navegador
    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: lightgreen'>
        <h1>Bienvenid@ </h1>
        <h2> Medicamentos </h2>
    """
    ## Recorremos la lista de 'results', en este caso 10 veces por el limite que hemos añadido
    for elem in datos['results']:
        if elem['openfda']:
            print("El nombre del medicamento es:", elem['openfda']['generic_name'][0])
        else: # Si no se encuentra el 'openfda', el programa continua iterando los demas elementos
            continue
        # Renovamos el contenido para que los nombres de los medicamentos para que aparezcan por el
        # navegador
        contenido += elem['openfda']['generic_name'][0]
        # Determinamos que cada vez que nos de un nombre realice un salto de linea y cerramos el HTML
        contenido += """<br/></body></html>"""

    # Indicamos que todo va a ir correctamente, aunque la peticion sea incorrecta
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    # Creamos el mensaje de respuesta juntando la linea_inicial, la cabecera y el contenido
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()



# Creamos un socket para el servidor, que es a donde van a llegar todas las peticiones del cliente
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Asociamos el socket a la IP y puerto del servidor
    serversocket.bind((IP, PORT))
    # Solo permite el numero de solicitudes que hemos determinado, las demas se rechazan
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # Se espera a que lleguen conexiones del cliente
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        # De forma que cuando llega, se nos imprime la IP y el puerto del cliente
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

    # Utilizamos un except para evitar errores que pudieran surgir y asi evitar parar el programa
except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")