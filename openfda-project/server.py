from flask import Flask,redirect,abort #Importamos flask y los siguientes modulos que emplearemos luego
from flask import request
import http.client #Importamos http.client para conectarnos con openfda posteriormente
import json

app = Flask(__name__)

@app.route("/searchDrug") #Esto es lo que introduciremos despues del localhost y el puerto para buscar los medicamentos
def buscar_medicam():
    #Reemplazamos los espacios por el %20 para que no de error a la hora de buscar el ingrediente activo con la url
    ing_activo = request.args.get("active_ingredient").replace(" ", "%20")
    limit=request.args.get("limit") #Determinamos el limite de medicamentos que queremos buscar
    if limit:
        #El usuario puede añadir el numero de medicamentos que quiera, de manera que cuando no lo añada, ese limite sera 10 siempre
        json1 = openfda1("/drug/label.json?search=active_ingredient:"+ing_activo+"&limit="+limit)
        mi_html = openfdahtml(json1) #La informacion anterior la devolvemos con un html
    else:
        json1 = openfda1("/drug/label.json?search=active_ingredient:"+ing_activo+"&limit=10")
        mi_html = openfdahtml(json1)
    return mi_html #Devolvemos los nombres de los medicamentos

@app.route("/searchCompany") #Buscamos las compañias que se desean
def buscar_compania():
    compania = request.args.get("company").replace(" ", "%20") #Realizamos lo mismo que antes, cambiamos los espacios por el %20
    limit=request.args.get("limit")
    if limit:
        json2 = openfda2("/drug/label.json?search=manufacturer_name:"+compania+"&limit="+limit)
        mi_html = openfdahtml(json2)
    else:
        json2 = openfda2("/drug/label.json?search=manufacturer_name:"+compania+"&limit=10")
        mi_html = openfdahtml(json2)
    return mi_html #Devolvemos los nombres de las empresas

@app.route("/listDrugs") #Por pantalla aparecera una lista con los medicamentos, donde el numero dependera de lo que añada el usuario
def lista_medicam():
    limit=request.args.get("limit")
    json1 = openfda1("/drug/label.json?&limit="+limit)
    mi_html = openfdahtml(json1) #Como antes, esa informacion la convertimos en un html
    return mi_html #Devolvemos esa informacion, los nombres de las empresas

@app.route("/listCompanies") #Aqui, aparecera la lista con los nombres de las compañias
def lista_companias():
    limit=request.args.get("limit")
    json2 = openfda2("/drug/label.json?&limit="+limit)
    mi_html = openfdahtml(json2)
    return mi_html

@app.route("/listWarnings") #En este caso, buscamos los peligros que puede generar el medicamento, que se obtienen de la misma manera
def lista_advertencias():
    limit=request.args.get("limit")
    json3 = openfda3("/drug/label.json?&limit="+limit) #Establecemos el numero de medicamentos que queremos que aparezcan
    mi_html = openfdahtml(json3)
    return mi_html #Devolvemos las advertencias de los medicamentos

#Creamos una funcion donde vamos a conectarnos a openfda, de donde cogemos la informacion, en este caso, el generic_name
def openfda1(json1):
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov") #Nos conectamos a la api
    #Este json1 hace referencia a la url, en este caso para obtener los medicamentos y la lista de los mismos
    conn.request("GET", json1, None, headers)
    info = conn.getresponse() #Leemos el mensaje de respuesta recibido del servidor
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8") #Leemos el contenido de la respuesta y lo convertimos a una cadena
    datos = (json.loads(drogas_raw)) #Imprimimos ese fichero que ha sido recibido
    medicamentos = "" #Creamos una variable vacia a la que introduciremos los nombres de los medicamentos
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']: #Buscamos el generic_name que se añadira a la variable
                medicamentos += "<li>" #Separamos cada medicamento por puntos
                medicamentos += str(elem['openfda']['generic_name'][0])
                medicamentos += "</li>"
            else:
                medicamentos += "<li>"
                medicamentos += "No se tienen datos del producto"
                medicamentos += "</li>"
                continue #Cuando no se encuentra, el programa continua iterando los elementos que se encuentran en datos
    else:
        medicamentos= "Desconocido" #Si el 'results' no se encuentra en datos, se imprimira este mensaje por pantalla
    conn.close()
    return medicamentos #Devolvemos los nombres de los medicamentos que los introduciremos en un html

def openfda2(json2): #Realizamos el mismo proceso, salvo que en este caso, devolvera la informacion de las compañias, manufacturer_name
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json2, None, headers) #Este json2 se refiere a la url para poder obtener las compañias y su lista
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    datos = (json.loads(drogas_raw))
    medicamentos = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'manufacturer_name' in elem['openfda']:
                medicamentos += "<li>"
                medicamentos += str(elem['openfda']['manufacturer_name'][0])
                medicamentos += "</li>"
            else:
                medicamentos += "<li>"
                medicamentos += "No se tienen datos del producto"
                medicamentos += "</li>"
                continue
    else:
        medicamentos= "Desconocido"
    conn.close()

    return medicamentos

def openfda3(json3): #Sucede lo mismo que antes, aunque aqui se devuelven las advertencias
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json3, None, headers) #Aqui json3 se utiliza para obtener las advertencias de los medicamentos
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    datos = (json.loads(drogas_raw))

    medicamentos = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'warnings' in elem: #Cada vez que se encuentra un 'warnings', lo añadiremos para que aparezca luego por pantalla
                medicamentos += "<li>"
                medicamentos += str(elem['warnings'][0])
                medicamentos += "</li>"
            else:
                medicamentos += "<li>"
                medicamentos += "No se tienen datos del producto"
                medicamentos += "</li>"
                continue
    else:
        medicamentos= "Desconocido"
    conn.close()
    return medicamentos


@app.route("/") #Si añadimos (/) despues del localhost y el puerto aparecera el siguiente mensaje por pantalla, siempre
def crear_html():
    contenido = """
    <!doctype html>
    <html>
    <body style='background-color: beige'>
    <h2 style="border: 2px solid orange;">Puntos de entrada</h2>
        <form action="searchDrug">
            <b><p>1. Introduce el nombre del ingrediente activo del medicamento:</b></p> 
            <ins>Ingrediente activo </ins>
            <input type="text"  name="active_ingredient" value=""><br>
            Limite
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="searchCompany">
            <b><p>2. Introduce la compañia que se desea buscar:</b></p>
            <ins>Compañia</ins>
            <input type="text"  name="company" value=""><br>
            Limite
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="listDrugs">
            <b><p>3. Ver lista de fármacos:</b></p>
            <ins>Limite </ins>
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="listCompanies">
            <b><p>4. Ver lista de compañias:</b></p>
            <ins>Limite </ins>
            <input type="text"  name="limit" value=""><br> 
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="listWarnings">
            <b><p>5. Ver lista de advertencias:</b></p>
            <ins>Limite </ins>
            <input type="text"  name="limit" value=""><br> 
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    return contenido

#Este es el html que se devolvera con la informacion de los medicamentos, una vez escrito lo que se quiere buscar
def openfdahtml(medicamentos):
    info = """
    <!doctype html>
    <html>
    <body style='background-color: lavender'>
    <h2 style="border: 2px solid orange;">Medicamentos</h2>
    <ul>
    """
    info += medicamentos #Renovamos la informacion
    info += """</ul><br/></body></html>""" #Cerramos el html con los puntos de entrada <ul> y </ul>, especiales para listas
    return info #Devolvemos el html con la informacion


@app.route("/secret") #Si añadimos (/secret) a la url, no nos deja observar la pagina de inicio, pues es privada, el programa aborta
def autenticar_pag():
    abort(401)


@app.route("/redirect") #Si añadimos (/redirect) volvemos a la pagina de inicio donde tenemos las opciones para elegir nuestra busqueda
def volver_page():
    return redirect('http://localhost:8000/', code=302)


if __name__ == "__main__": #Determinamos que nuestro codigo solo funcione en el localhost y en el puerto 8000
    app.run(host="127.0.0.1", port=8000)