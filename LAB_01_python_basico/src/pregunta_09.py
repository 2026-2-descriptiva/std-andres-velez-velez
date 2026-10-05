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


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    data["metrics_independientes"] = data[4].str.split(",")
    data_ampliada = data.explode("metrics_independientes")
    data_ampliada["metrics_independientes_2"] = data_ampliada["metrics_independientes"].str.split(":")

    data_ampliada["metrics_elemento_0"] = data_ampliada["metrics_independientes_2"].str[0]
    data_ampliada["metrics_elemento_1"] = data_ampliada["metrics_independientes_2"].str[1]
    data_ampliada["metrics_elemento_1"] = data_ampliada["metrics_elemento_1"].astype(int)
    data_ampliada

    conteo_metrics = {}

    for element in data_ampliada["metrics_elemento_0"]:
        if element not in conteo_metrics:
            conteo_metrics[element] = 1
        else:
            conteo_metrics[element] += 1

    resultado = dict(sorted(conteo_metrics.items()))
    return resultado

# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_09())
