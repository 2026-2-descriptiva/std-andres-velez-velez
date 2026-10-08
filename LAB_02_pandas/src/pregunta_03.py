import pandas as pd
from pathlib import Path 

def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl0.tsv"
    data_0 = pd.read_csv(DATA_FILE, sep = "\t")

    resultado = data_0.groupby("c1").size() # groupby cuenta por categoría y size cuenta los elementos de cada grupo
    return resultado

# -------------------------------------------------------------
# VALIDAR RESPUESTA
# -------------------------------------------------------------
print(pregunta_03())


# conteo = {}
# for letter in data_0["c1"]:
#     if letter in conteo:
#         conteo[letter] += 1 
#     else: 
#         conteo[letter] = 1
# respuesta = pd.Series(conteo).sort_index()
# respuesta.index.name = "c1"

# return respuesta

