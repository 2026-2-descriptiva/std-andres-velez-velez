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



def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    data = pd.read_csv(DATA_FILE, sep="\t", header=None)
    suma = (data.assign(letra = data[3].str.split(","))   # con data.assign se crea una copia de data que contiene una columna llamada letra, en donde los elmentos de data[3] son elementos de una lista
            .explode("letra")     # Generan nuevas filas en las que cada elemento de data[3] esta individualmente conservando la información de las demás
            .groupby("letra")[1]  # Se usa a letra como llave y a data[1] como valor
            .sum()
    )

    resultado = suma.to_dict()
    return resultado


# ----------------------------------
# Validar resultado
# ----------------------------------
print(pregunta_11())
