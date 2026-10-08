import pandas as pd
from pathlib import Path

def pregunta_04():
    """
    Usando `data/tbl0.tsv`, calcule el promedio de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son los promedios.

    Ejemplo del formato de la respuesta:

        c1
        A    4.6250
        B    5.1429
        C    5.4000
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl0.tsv"
    data_0 = pd.read_csv(DATA_FILE, sep="\t")
    resultado = data_0.groupby("c1")["c2"].mean()
    
    return resultado


# --------------------------------------------------------------
# VALIDAR RESPUESTA
# --------------------------------------------------------------
print(pregunta_04())
