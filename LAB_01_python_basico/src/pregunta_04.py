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


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    data[2] = data[2].astype(str)
    data["mes"] = data[2].str[5:7]
    data["año"] = data[2].str[0:4]
    data["dia"] = data[2].str[8:10]

    dict_mes = {}

    for element in data["mes"]:
        if element in dict_mes:
            dict_mes[element] += 1
        else:
            dict_mes[element] = 1

    resultado = sorted(dict_mes.items())
    return resultado

# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_04())
