import pandas as pd
from pathlib import Path


# -----------------------------------
# Cargar las rutas de manera relativa
# -----------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
DATA_FILE = DATA_DIR / 'data.csv.gz'

# ---------------------------------
# Validar la existencia del archivo
# ---------------------------------
assert DATA_FILE.exists()


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None) 
    conteo_letras = {}   # El diccionario indicará el conteo de cada letra

    for letra in data[0]:
        if letra in conteo_letras:
            conteo_letras[letra] += 1
        else:
            conteo_letras[letra] = 1

    resultado = sorted(conteo_letras.items())   # sorted crea una lista a partir de objetos iterables (diccionarios, listas, tuplals)
    return resultado                            # .items() devuelve tuplas de (clave, valor) del diccionario


# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_02())


