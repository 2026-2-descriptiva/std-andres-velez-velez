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



def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    n_codes   = data[3].str.split(",").str.len()
    n_metrics = data[4].str.split(",").str.len()

    resultado = list(zip(data[0].tolist(), n_codes.tolist(), n_metrics.tolist()))
    return resultado


# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_10())
