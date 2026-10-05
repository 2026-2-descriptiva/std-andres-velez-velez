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


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    dict_max_min = {}

    for letter in data[0]: 
        dict_max_min[letter] = (letter,
                            data.loc[data[0] == letter, 1].max(), 
                            data.loc[data[0] == letter, 1].min()
                            )


    resultado = sorted(dict_max_min.values())
    return resultado

# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_05())
