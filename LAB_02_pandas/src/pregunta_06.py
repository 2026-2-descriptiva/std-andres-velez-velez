import pandas as pd
from pathlib import Path

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    DATA_DIR = Path(__file__). resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl1.tsv"
    data_1 = pd.read_csv(DATA_FILE, sep="\t")
    resultado = sorted(data_1["c4"].str.upper().unique())

    return resultado

# ----------------------------------------------------------------------------
# VALIDAR RESPUESTA
# ----------------------------------------------------------------------------
print(pregunta_06())
