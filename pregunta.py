"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------
Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.
"""

import re

import pandas as pd


def ingest_data():

    filas = []  # Filas almacenadas + encabezado

    columnas = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave"
    ]

    clusters = []  # Lista con toda la información

    diccionario = {
        "cluster": 0,
        "cantidad": 0,
        "porcentaje": 0,
        "palabras": "",
    }  # Diccionario que se va a reiniciar con cada fila y almacenar valores claves con las expresiones regulares

    with open("clusters_report.txt") as cluster:
        filas = cluster.readlines()  # Leer el archivo para su manipulación
    filas = filas[4:]  # Sólo las filas, se omite el encabezado

    for fila in filas:
        if re.match("^ +[0-9]+ +", fila):
            # expresión  regular que comienza con uno o mas espacios seguidos
            # de uno  o más dígitos seguidos de uno o más espacios.
            cluster, cantidad, porcentaje, *palabras = fila.split()
            diccionario["cluster"] = int(cluster)
            diccionario["cantidad"] = int(cantidad)
            diccionario["porcentaje"] = float(porcentaje.replace(",", "."))
            # Reemplazamos las comas por puntos en los porcentajes
            palabras = " ".join(palabras[1:])
            diccionario["palabras"] += palabras
            diccionario["palabras"] = diccionario["palabras"].replace(".", "")  # Cambio

        elif re.match("^ + [a-z]", fila):
            # expresión regular que comienza con uno o más espacios seguidos de una letra minúscula.
            # se utiliza para identificar líneas que parecen contener palabras
            palabras = fila.split()
            palabras = " ".join(palabras)
            diccionario["palabras"] += " " + palabras

        elif re.match("^\n", fila) or re.match("^ +$", fila):
            # Lo vamos a utilizar para reiniciar el diccionario al saltar de cluster
            # expresión regular que contiene un sólo salto de línea o líneas que
            # contienen uno o más espacios y luego un final de línea.
            # se utiliza para identificar líneas en blanco o líneas que contienen
            # sólo espacios

            clusters.append(diccionario.values())

            diccionario = {
                "cluster": 0,
                "cantidad": 0,
                "porcentaje": 0,
                "palabras": "",
            }


    df = pd.DataFrame(clusters, columns=columnas)
    # DataFrame final con la ingestión de datos
    return df 
