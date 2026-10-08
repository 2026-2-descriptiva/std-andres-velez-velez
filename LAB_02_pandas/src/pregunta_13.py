import pandas as pd
from pathlib import Path

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE_0 = DATA_DIR / "tbl0.tsv"
    DATA_FILE_2 = DATA_DIR / "tbl2.tsv"
    data_0 = pd.read_csv(DATA_FILE_0, sep="\t")
    data_2 = pd.read_csv(DATA_FILE_2, sep="\t")
    data = pd.merge(data_0, data_2, left_on="c0", right_on="c0", how="inner")

    resultado = (data.groupby("c1")["c5b"].sum())
    return resultado


# -----------------------------------------------------------------------------
# VALIDAR RESPUESTA 
# -----------------------------------------------------------------------------
print(pregunta_13())