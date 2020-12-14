from flask import Flask, render_template, request, json, jsonify
import csv
from algoritmos import algoritmo
from datetime import datetime

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def inicio():

    return render_template('index.html')


@app.route('/modelo', methods=['GET', 'POST', 'DELETE', 'PUT'])
def modelo():
    data = request.get_json()
    # print(data)
    print(data['modo'])
    val = data['csv'].split('\n')
    # print(val)
    valores = csv.reader(val)
    lista = list(valores)
    del lista[0]
    #print(len(lista), lista[0])

    f = open("bitacora.txt","a")
    now = datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write(fecha_hora +"\n    Archivo: ")
    f.write(data['archivo']+"\n")

    crit = "    Criterio de finalizacion: "
    numCr1 = int(data['criterio'])

    if numCr1 == 1:
        crit += "Maxima Generacion\n"
    elif numCr1 == 2:
        crit += "Valor Minimo\n"
    else:
        crit += "Porcentaje\n"

    pad = "    Criterio de Padres: "
    numPa = int(data['modo'])

    if numPa == 1:
        pad += "Aleatorio\n"
    elif numPa == 2:
        pad += "Torneo\n"
    else:
        pad += "Mejor fitness\n"  
    f.write(crit)
    f.write(pad)
    f.close()

    mejor = algoritmo.ejecutar(lista, int(data['criterio']), int(data['modo']))
    
    return jsonify(
        solucion = mejor.solucion,
        fitness  = mejor.fitness
    )
