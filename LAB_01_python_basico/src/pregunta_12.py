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



def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    resultado = (
        data.assign(llave_numero=data[4].str.split(","))
            .explode("llave_numero")
            .assign(valor=lambda d: d["llave_numero"].str.split(":").str[1].astype(int))
            .groupby(0)["valor"]
            .sum()
            .to_dict()
    )

    return resultado


# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_12())