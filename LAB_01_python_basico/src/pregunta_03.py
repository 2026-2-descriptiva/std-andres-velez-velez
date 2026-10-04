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


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)   
    dic_conteo = {}   # El diccionario almacenará la suma de los valores de la segunda columna para cada letra

    for letra in data[0]:
        if letra not in dic_conteo:
            dic_conteo[letra] = data.loc[data[0] == letra, 1].sum()   # loc permite coordinar la relación entre fila y columna (coordenadas del df)
                                                                      # 1 es el nombre de la segunda columna (value)
    resultado = sorted(dic_conteo.items())
    return resultado

# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_03())
