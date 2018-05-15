from flask import Flask,redirect,abort
from flask import request
import http.client
import json

app = Flask(__name__)

@app.route("/searchDrug")
def buscar_medicam():
    ing_activo = request.args.get("active_ingredient").replace(" ", "%20")
    #limit=request.args.get("limit")
    json1 = openfda1("/drug/label.json?search=active_ingredient:"+ing_activo+"&limit=10")#+limit)
    mi_html = openfdahtml(json1)
    return mi_html

@app.route("/searchCompany")
def buscar_compania():
    compania = request.args.get("company").replace(" ", "%20")
    #limit=request.args.get("limit")
    json2 = openfda2("/drug/label.json?search=manufacturer_name:"+compania+"&limit=10")#+limit)
    mi_html = openfdahtml(json2)
    return mi_html

@app.route("/listDrugs")
def lista_medicam():
    limit=request.args.get("limit")
    json1 = openfda1("/drug/label.json?&limit="+limit)
    mi_html = openfdahtml(json1)
    return mi_html

@app.route("/listCompanies")
def lista_companias():
    limit=request.args.get("limit")
    json1 = openfda2("/drug/label.json?&limit="+limit)
    mi_html = openfdahtml(json1)
    return mi_html

@app.route("/listWarnings")
def lista_advertencias():
    limit=request.args.get("limit")
    json3 = openfda3("/drug/label.json?&limit="+limit)
    mi_html = openfdahtml(json3)
    return mi_html

def openfda1(json1):
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json1, None, headers)
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    datos = (json.loads(drogas_raw))
    medicamentos = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']:
                medicamentos += "<li>"
                medicamentos += str(elem['openfda']['generic_name'][0])
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

def openfda2(json2):
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json2, None, headers)
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

def openfda3(json3):
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", json3, None, headers)
    info = conn.getresponse()
    print(info.status, info.reason)
    drogas_raw = info.read().decode("utf-8")
    datos = (json.loads(drogas_raw))

    medicamentos = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'warnings' in elem:
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


@app.route("/")
def crear_html():
    contenido = """
    <!doctype html>
    <html>
    <body style='background-color: lightcyan'>
    <h2 style="border: 2px solid orange;">Puntos de entrada</h2>
        <form action="searchDrug">
            <b><p>1. Introduce el nombre del ingrediente activo del medicamento:</b></p>
            <ins>Ingrediente activo </ins>
            <input type="text"  name="active_ingredient" value=""><br>
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

@app.route("/")
def openfdahtml(medicamentos):
    info = """
    <!doctype html>
    <html>
    <body style='background-color: lavender'>
    <h2 style="border: 2px solid orange;">Medicamentos</h2>
    <ul>
    """
    info += medicamentos
    info += """</ul><br/></body></html>"""
    return info


@app.route("/secret")
def autenticar_pag():
    abort(401)


@app.route("/redirect")
def volver_page():
    return redirect('http://localhost:8000/', code=302)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)