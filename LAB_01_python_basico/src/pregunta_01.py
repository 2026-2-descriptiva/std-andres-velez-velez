import pandas as pd
from pathlib import Path


# -----------------------------------
# Cargar las rutas de manera relativa
# -----------------------------------
DATA_DIR = Path('LAB_01_python_basico/data')
DATA_FILE = DATA_DIR / 'data.csv.gz'

# ---------------------------------
# Validar la existencia del archivo
# ---------------------------------
assert DATA_FILE.exists()


def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)    # Leer los datos
    suma_columna1 = data[1].sum()                           # Sumar valores columna 1

    return int(suma_columna1)

# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_01())