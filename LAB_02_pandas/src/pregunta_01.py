import pandas as pd
from pathlib import Path


def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_FILE = DATA_DIR / "tbl0.tsv"
    data_0 = pd.read_csv(DATA_FILE, sep = "\t")

    return len(data_0)

# -------------------------------------------------------------
# VALIDAR RESULTADO
# -------------------------------------------------------------
print(pregunta_01())