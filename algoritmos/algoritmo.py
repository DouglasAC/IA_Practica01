from algoritmos import nodo
from datetime import datetime
import random
import pandas

tamPoblacion = 100
generacionMaxima = 500
valorMinimo = 1
valorPorcentaje = tamPoblacion * 0.75
cantidadPadres = int(tamPoblacion / 2)


def inicializarPoblacion(lista):
    poblacion = []
    for x in range(tamPoblacion):
        solucion = []
        for y in range(4):
            solucion.append(random.uniform(-2, 2))
        poblacion.append(nodo.Nodo(solucion, evaluarFitness(solucion, lista)))
    return poblacion


def verificarCriterio(poblacion, generacion, opcion):
    result = False
    if opcion == 1:
        result = verificarMaximoGenenracion(generacion)
    elif opcion == 2:
        result = verificarValorMinimo(poblacion)
    elif opcion == 3:
        result = verificarPorcentaje(poblacion)
    return result


def verificarMaximoGenenracion(generacion):
    return False if generacion < generacionMaxima else True


def verificarValorMinimo(poblacion):
    for individuo in poblacion:
        if individuo.fitness < valorMinimo:
            return True
    return False


def verificarPorcentaje(poblacion):
    valores = []
    for individuo in poblacion:
        valores.append(individuo.fitness)
    df = pandas.DataFrame({'valor': valores})
    conteo = df.value_counts()
    for valor in conteo:
        if valor >= valorPorcentaje:
            return True
    return False


def evaluarFitness(solucion, lista):
    valoresNotas = []
    for elemento in lista:
        valor = float(solucion[0]) * float(elemento[0]) + float(solucion[1]) * float(elemento[1]) + \
            float(solucion[2]) * float(elemento[2]) + \
            float(solucion[3]) * float(elemento[3])
        valoresNotas.append(valor)
    sumaCuadrada = 0
    for elemento in range(len(lista)):
        sumaCuadrada += (float(lista[elemento][4]) - valoresNotas[elemento])**2

    valorFit = sumaCuadrada/len(lista)
    return valorFit


def seleccionarPadres(poblacion, opcion):
    if opcion == 1:
        return padresAleatorio(poblacion)
    elif opcion == 2:
        return padresTorneo(poblacion)
    elif opcion == 3:
        return padresMejores(poblacion)


def padresAleatorio(poblacion):
    padres = []
    for x in range(cantidadPadres):
        pos = random.randint(0, int(len(poblacion)) - 1)
        padres.append(poblacion[pos])
        poblacion.pop(pos)
    return padres


def padresTorneo(poblacion):
    padres = []
    for x in range(cantidadPadres):
        op1 = poblacion[x*2]
        op2 = poblacion[x*2+1]
        if op1.fitness < op2.fitness:
            padres.append(op1)
        else:
            padres.append(op2)
    return padres


def padresMejores(poblacion):
    padres = []
    poblacion = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        :len(poblacion)]
    for x in range(cantidadPadres):
        padres.append(poblacion[x])
    return padres


def cruzar(padre1, padre2):
    hijo = []
    for x in range(len(padre1)):
        probabilidad = random.uniform(0, 1)
        if probabilidad > 0.6:
            hijo.append(padre2[x])
        else:
            hijo.append(padre1[x])
    return hijo


def mutar(solucion):
    for x in range(len(solucion)):
        if random.randrange(2) == 1:
            solucion[x] = random.uniform(-2, 2)
    return solucion


def emparejar(padres, lista):
    nuevaPoblacion = []
    solHijos = []
    for x in range(int(cantidadPadres/2)):
        hijo1 = cruzar(padres[x*2].solucion, padres[x*2+1].solucion)
        solHijos.append(hijo1)
        hijo2 = cruzar(padres[x*2+1].solucion, padres[x*2].solucion)
        solHijos.append(hijo2)

    for x in range(len(solHijos)):
        if random.randrange(2) == 1:
            solHijos[x] = mutar(solHijos[x])

    hijos = []
    for elemento in solHijos:
        hijos.append(nodo.Nodo(elemento, evaluarFitness(elemento, lista)))

    for x in range(len(hijos)):
        nuevaPoblacion.append(padres[x])
        nuevaPoblacion.append(hijos[x])

    return nuevaPoblacion


def imprimirPoblacion(poblacion):
    print("------------------ Poblacion -------------------")
    for individuo in poblacion:
        print("Solucion: ", individuo.solucion, "Fitness: ", individuo.fitness)


def ejecutar(lista, finalizacion, Opadres):
    generacion = 0
    p = inicializarPoblacion(lista)
    fin = verificarCriterio(p, generacion, finalizacion)

    while (not fin):
        padres = seleccionarPadres(p, Opadres)
        p = emparejar(padres, lista)
        generacion += 1
        fin = verificarCriterio(p, generacion, finalizacion)

    print("---------- Generacion ", generacion, " ------------------ ")
    imprimirPoblacion(p)
    p = sorted(p, key=lambda item: item.fitness, reverse=False)[
        :len(p)]

    w = open("bitacora.txt", "a")
    w.write("    Numero de Generaciones: " + str(generacion) + "\n")
    w.write("    Mejor Solucion: " + str(p[0].solucion) + "\n")
    w.write("    Fitness Solucion: " + str(p[0].fitness) + "\n")
    now = datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    w.write("    Terminino: "+fecha_hora + "\n")
    w.close()
    return p[0]
