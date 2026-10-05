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



def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    data["metrics_independientes"] = data[4].str.split(",")
    data_ampliada = data.explode("metrics_independientes")
    data_ampliada["metrics_independientes_2"] = data_ampliada["metrics_independientes"].str.split(":")

    data_ampliada["metrics_elemento_0"] = data_ampliada["metrics_independientes_2"].str[0]
    data_ampliada["metrics_elemento_1"] = data_ampliada["metrics_independientes_2"].str[1]
    data_ampliada["metrics_elemento_1"] = data_ampliada["metrics_elemento_1"].astype(int)
    data_ampliada

    resultado = list(map(tuple,           # Se crea la lista para cumplir con el formato de respuesta
                         data_ampliada.   # map hace que todas las funciones se aplican a cada elemento que indica la métrica (metrics_elemento_1)
                         groupby("metrics_elemento_0")["metrics_elemento_1"].   # Se filtra por metrics_elemento 0 pero se calcula max y min para metrics_elemento_1
                         agg(["min", "max"]).   # agg permite que se calcule max y min en simultáneo se indican "min" y "max" con "" por sintaxis de agg
                         reset_index().values   # reset index se utiliza para recuperar a métrica_elemento_0 en la respuesta, sin él, la respuesta sólo recuperaría el min y max
                         )
                    )
    return resultado


# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_06())
