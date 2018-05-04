from flask import Flask
from flask import request
from flask import jsonify
import http.client
import json
app = Flask(__name__)


@app.route("/searchDrugs")
def buscar_medicam():
    ing_activo= request.args.get("active_ingredient").replace(" ","%20")
    json1 = openfda("/drug/label.json?search=active_ingredient:"+ing_activo+"&limit=10")
    mi_html= crear_html(json1)
    return mi_html


@app.route("/searchCompany")
def buscar_compania():
    compania = request.args.get("manufacturer_name")
    json1 = openfda("/drug/label.json?limit=10&search=manufacturer_name:"+compania)
    mi_html= crear_html(json1)
    return mi_html

@app.route("/listDrugs")
def lista_medicam():
    medicam = request.args.get("generic_name")
    json1 = openfda("/drug/label.json?limit=10&search=generic_name:"+medicam)
    mi_html= crear_html(json1)
    return mi_html

@app.route("/listCompanies")
def lista_companias():
    empresa = request.args.get("manufacturer_name")
    json1 = openfda("/drug/label.json?limit=10&search=manufacturer_name:"+empresa)
    mi_html= crear_html(json1)
    return mi_html

def openfda(json1):
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json1, None, headers)
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    conn.close()

    datos = (json.loads(drogas_raw))

    medicamentos = ""
    for elem in datos['results']:
        if "generic_name" in elem['openfda']:
            medicamentos += str(elem['openfda']['generic_name'][0])
            medicamentos += "<br>"
        else:
            medicamentos += "No se tienen datos del nombre del producto"
            medicamentos += "<br>"
            continue
    return medicamentos

@app.route("/")
def crear_html(medicamentos):
    contenido = """
    <!doctype html>
    <html>
    <body style='background-color: lightcyan'>
    <h2 style="border: 2px solid orange;">Puntos de entrada</h2>
        <form>
            1. Introduce uno de los siguientes puntos de entrada: <br>
            <input type="radio" name="entrada" value="active_ingredient" > Nombre del ingrediente activo<br>
            <input type="radio" name="entrada" value="manufacturer_name"> Compania<br>
            <input type="submit"  value="Submit"><br>
        </form>
        <form>
            2. Introduce otro punto de entrada: <br>
            <input type="text"  name="entrada"><br>
            <input type="submit"  value="Submit">
        </form>"""

    contenido += medicamentos
    contenido += """<br/></body></html>"""

    return contenido


# url relativa y url absoluta

            
# Poner aqui como un formulario, es decir, que el ususario interactue con la pagina,
# tocando botonmes poniendo preguntas y que el usuario responda... que escriba
# en una casilla..

if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 8088)