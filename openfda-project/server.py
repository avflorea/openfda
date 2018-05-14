from flask import Flask
from flask import request
from flask import jsonify
import http.client
import json

app = Flask(__name__)


@app.route("/searchDrugs")
def buscar_medicam():
    ing_activo = request.args.get("active_ingredient")
    ing_activo = ing_activo.replace(" ", "%20")
    limit=request.args.get("limit")
    json1 = openfda("/drug/label.json?search=active_ingredient:"+ing_activo+"&limit"+limit)
    mi_html = openfdahtml(json1)
    return mi_html


@app.route("/searchCompany")
def buscar_compania():
    compania = request.args.get("manufacturer_name")
    compania = compania.replace(" ", "%20")
    limit=request.args.get("limit")
    json1 = openfda("/drug/label.json?search=manufacturer_name:"+compania+"&limit"+limit)
    mi_html = openfdahtml(json1)
    return mi_html


@app.route("/listDrugs")
def lista_medicam():
    limit=request.args.get("limit")
    medicam = request.args.get("generic_name").replace(" ", "%20")
    json1 = openfda("/drug/label.json?search=generic_name:"+medicam+"&limit"+limit)
    mi_html = openfdahtml(json1)
    return mi_html


@app.route("/listCompanies")
def lista_companias():
    limit=request.args.get("limit")
    empresa = request.args.get("manufacturer_name")
    empresa = empresa.replace(" ", "%20")
    json1 = openfda("/drug/label.json?search=manufacturer_name:"+empresa+"&limit="+limit)
    mi_html = openfdahtml(json1)
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
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']:
                medicamentos += str(elem['openfda']['generic_name'])
                medicamentos += "<br>"
            elif 'manufacturer_name' in elem['openfda']:
                medicamentos += str(elem['openfda']['manufacturer_name'])
                medicamentos += "<br>"
            else:
                medicamentos += "No se tienen datos del nombre del producto"
                medicamentos += "<br>"
                continue

    return "<ul><li>{}</li></ul>".format(medicamentos)

@app.route("/")
def crear_html():
    contenido = """
    <!doctype html>
    <html>
    <body style='background-color: lightcyan'>
    <h2 style="border: 2px solid orange;">Puntos de entrada</h2>
        <form action="/searchDrugs">
            1. Introduce el nombre del ingrediente activo del medicamento: <br>
            Medicamentos <br>
            <input type="text"  name="active_ingredient" value=""><br>
            Limite
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="/searchCompany">
            2. Introduce la compañia que se desea buscar: <br>
            Companias <br>
            <input type="text"  name="manufacturer_name" value=""><br>
            Limite
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
    <!doctype html>
    <html>
    <body>
        <form action="/listDrugs">
            3. Ver lista de fármacos: <br>
            Lista de farmacos <br>
            Limite
            <input type="text"  name="limit" value=""><br>
            <input type="submit"  value="Submit">
        </form><br/></body></html>"""
    contenido += """
        <!doctype html>
        <html>
        <body>
            <form action="/listCompanies">
                4. Ver lista de compañias: <br>
                Lista de Companias <br>
                Limite
                <input type="text"  name="limit" value=""><br> 
                <input type="submit"  value="Submit">
            </form><br/></body></html>"""
    return contenido


@app.route("/")
def openfdahtml(medicamentos):
    info = """
    <!doctype html>
    <html>
    <body style='background-color: lightcyan'>
    <h2 style="border: 2px solid orange;">Medicamentos</h2>
    """
    info += medicamentos
    info += """<br/></body></html>"""

    return info


# url relativa y url absoluta


# Poner aqui como un formulario, es decir, que el ususario interactue con la pagina,
# tocando botonmes poniendo preguntas y que el usuario responda... que escriba
# en una casilla..

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)