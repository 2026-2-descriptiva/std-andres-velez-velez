import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """
    DATA_DIR_TEST = Path(__file__).resolve().parent.parent / "data" / "test"
    DATA_DIR_TRAIN = Path(__file__).resolve().parent.parent / "data" / "train"
    SUBMISSION = Path(__file__).resolve().parent.parent / "submission"

    conjuntos = {"test": DATA_DIR_TEST, "train": DATA_DIR_TRAIN}

    for nombre, ruta in conjuntos.items():  # nombre = llave y ruta = valor, ambos se llaman con .items()
        registros = []                      # La lista debe crearse dentro del ciclo for para evitar doble conteo
        for carpeta in sorted(ruta.iterdir()):      # Con iterdir() se leen todos los elementos, de la primera capa, al interior de carpeta: negative, neutral y positive
            if carpeta.is_dir():            # Se verifica si los elementos (negative, neutral, positive) son carpetas. 
                for archivo in sorted(carpeta.glob("*.txt")):   # Se seleccionan todos los archivos de extensión .txt
                    registros.append({                  # Se incluye el contenido de todos estos archivos en el diccionario registros
                        "phrase": archivo.read_text(encoding="utf-8").strip(),
                        "target": carpeta.name
                    })

        datos_consolidados = pd.DataFrame(registros)                                            # Se conveirte el contenido del diccionario en un dataframe
        lineas = '"' + datos_consolidados["phrase"] + '"' + "," + datos_consolidados["target"]  # Se incluye las comillas y las comas para cumplir con el formato de respuesta

        with open(SUBMISSION / f"{nombre}_dataset.csv", "w", encoding="utf-8") as f:            # Se relaciona la carpeta SUBMISSION en la que se debe dejar la respuesta. Cada archivo toma el nombre que se relacionó como llave en el diccionario conjuntos
            f.write("phrase,target\n")    # Salto de línea respecto al encabezado               # w indica "write" sobre cada archivo y utf-8 es la traducción de cada carácter
            f.write("\n".join(lineas))    # Salto de línea entre cada línea

# -----------------
# LLAMAR LA FUNCIÓN
# -----------------
pregunta_01()           # No se usa reutrn porque la función no devuelve ningún valor
