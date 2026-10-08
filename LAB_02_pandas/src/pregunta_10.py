import pandas as pd
from pathlib import Path

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl0.tsv"
    data_0 = pd.read_csv(DATA_FILE, sep="\t")

    resultado = (
                data_0.groupby("c1")["c2"]                       # s recibe los valores de c2 agrupados por c1
                .apply(lambda s: ":".join(map(str, sorted(s))))  # map aplica str a cada elemento, joint une cada elemento mediante :
                .to_frame()
                )

    return resultado

# -------------------------------------------------------------
# VALIDAR RESPUESTA
# -------------------------------------------------------------
print(pregunta_10())