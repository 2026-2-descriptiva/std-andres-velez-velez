import pandas as pd
from pathlib import Path

def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl0.tsv"
    data_0 = pd.read_csv(DATA_FILE, sep="\t")
    resultado = data_0.groupby("c1")["c2"].sum()

    return resultado

# ---------------------------------------------------------------
# VALIDAR RESPUESTA
# ---------------------------------------------------------------
print(pregunta_07())