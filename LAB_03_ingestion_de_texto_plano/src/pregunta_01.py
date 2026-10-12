import pandas as pd
from pathlib import Path
import re

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "clusters_report.txt"
    with open(DATA_FILE, encoding="UTF-8") as archivo:
            lineas = archivo.readlines()

    patron = re.compile(r"^(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s*(.*)$")   # ^la coincidencia debe estar al inicio de la linea: así se excluyen las líneas que no son de interés
                                                                     # Se sigue un esquema de digito y espacio para las columnas de cluster y cantidad de palabras clave: ambas conformadas por números enteros
                                                                     # Para porcentaje se sigue la estrcutura digito , digita %, tal como se visualizó anteriormente en los datos
    registros = []
    for linea in lineas:
        linea = linea.strip()                                      # lectura línea por línea, eliminando \n
        coincidencia = patron.match(linea)                         # Captura el campo de las líneas que siguen la estructura del regex
        if coincidencia:
            registros.append(list(coincidencia.groups()))          # Introduce estos campos en la lista registros
        elif len(linea) > 0 and len(registros) > 0:
             registros[-1][3] += " " + linea

    resultado = pd.DataFrame(registros, columns=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"])   # Se crean las columnas con los nombres requeridos
    resultado = resultado.astype({"cluster": int, "cantidad_de_palabras_clave": int})                                             # Se inidca el tipo de datoa a asociar a cada columna 
    resultado["porcentaje_de_palabras_clave"] = resultado["porcentaje_de_palabras_clave"].str.replace(",", ".").astype(float)     #Para la columna porcentajee de palabras clave se sustituye la coma por un punto y se convierte a float para reportar el dato en el formato solicitado
    resultado["principales_palabras_clave"] = resultado["principales_palabras_clave"].apply(
    lambda texto: ", ".join(" ".join(p.split()) for p in texto.split(",") if p.strip()).rstrip("."))
    return resultado

# ------------------------------------
# VALIDAR RESPUESTA
# ------------------------------------
print(pregunta_01())

