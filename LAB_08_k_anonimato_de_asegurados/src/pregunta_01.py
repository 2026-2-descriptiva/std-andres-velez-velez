import pandas as pd
from pathlib import Path
import numpy as np
import json

def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    # Carga de las rutas
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "insurance.csv.gz"
    SUBMISSION_DIR = Path(__file__).parent.parent / "submission"
    SUBMISSION_PRIVACY = SUBMISSION_DIR / "privacy_report.json"
    SUBMISSION_INSURANCE = SUBMISSION_DIR / "insurance_published.csv"

    # Lectura de los datos
    datos = pd.read_csv(DATA_FILE, compression='gzip', encoding='utf-8')

    # Creación de las nuevas columnas solicitadas
    datos["age_group"] = pd.cut(datos["age"],   # cut permite segmentar los datos de "age" en grupos definidos en los bins
                                bins=[18, 30, 40, 50, 65],  # Definición de los grupos de edad. Se toma 65 para que cubra a las personas con 64 años
                                labels=["18-29", "30-39", "40-49", "50-64"],   # Se agregan los labels (etiquetas) para darle un nombre a cada uno de los intervalos creados
                                right=False                 # Al definir right=False, el límite derecho de cada intervalo será abierto
    )

    datos["bmi_group"] = pd.cut(datos["bmi"],
                                bins=[0, 18.5, 25, 30, 100], 
                                labels=["bajo peso", "normal", "sobrepeso", "obesidad"],   
                                right=False
    )

    datos["children_group"] = pd.cut(datos["children"],
                                    bins=[0, 1, 3, np.inf], # En este caso np.inf indica que no hay límite superior para el último conjunto: [3, ∞)
                                    labels=["0", "1-2", "3+"],
                                    right=False
    )

    # ---------------------------------------
    # ANÁLISIS DE LOS ESQUEMAS DE K-ANONIMATO
    # ---------------------------------------

    # Planteamiento de los esquemas indicados: with_children y without_children
    esquemas = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"]
    }

    resultados_esquemas = {}  # Se crea un diccionario vacío para almacenar los resultados de cada esquema

    for nombre, columnas in esquemas.items():                                                 # En este loop nombre es la llave de cada esquema y columnas es la lista de columnas asociada a cada llave
        tamaño_x_agrupacion = datos.groupby(columnas, observed=True).size()                   # datos se agrupa según el número de columnas definidas en cada uno de los esquemas (5 y 4 columnas). size regresa para cada una de ellas el número de veces que se identificó un sujeto con una coincidencia exacta para un mismo esquema para las diferentes combinaciones posibles generadas por el groupby
        equivalence_classes= len(tamaño_x_agrupacion)                                         # Número de diferentes combinaciones obsevradas para el esquema with_children y without_children
        k_before_suppression = int(tamaño_x_agrupacion.min())                                 # Mínimo número de coincidencias para cada esquema. Es decir, el valor mínimo de k antes de aplicar la supresión                               
        tamaño_x_fila = datos.groupby(columnas, observed=True)[columnas[0]].transform("size") # Se realiza la misma agrupación que en tamaños_x_agrupacion. La diferencia es el formato en que se entrega la información. Aplicando column[0] se indicó que al análisis debe ser sobre "age_group" y con transform se hizo el conteo del número de coincidencias sobre todas las combinaciones posibles, peero asignando el resultado para cada fila (cada observación). En tamaño_x_agrupacion se tiene el número de coincidencias se tiene un resumen: el número de coincidencias por categoría: no por fila.

        condicion = tamaño_x_fila >= 5                                                           # Se aplica la condición de k-anonimato. Es decir, la condicion indica que para cada fila (observación) se deben tener al menos otras 4 coincidencias (k=5)
        observaciones_cumplen = datos[condicion]                                                 # Se seleccionan las filas que cumplen la condición de k anonimato k=5
        published_records = len(observaciones_cumplen)                                           # Número de observaciones que cumplen la condición k=5
        published_classes = len(observaciones_cumplen.groupby(columnas, observed=True).size())   # Se repite la misma agrupación realizada en tamaño por agrupacion, pero ahora se realiza sobre las filas que cumplen la condicipon de k-anonimato>=5
        suppressed_records = len(datos) - published_records                                      # Cálculo de las agrupaciones que no cumplieron la condición de k-anonimato=5. Es decir, el número de observaciones que se suprimieron

        data_without_smoker_diversity = observaciones_cumplen.groupby(columnas, observed=True).filter(lambda x: len(x['smoker'].unique()) < 2)  # x corresponde a cada una de las diferentes agrupaciones construidas. Las agrupaciones e realizaron sobre las 5 y 4 columnas indicadas en los esquemas. Smoker no es una de ellas. Para cada una de las agrupaciones de las columnas quiero validar: Tengo agrupaciones que dentro de sus filas de smoker tienen todas el mismo tipo de respuesta, ya sea "yes" o "no"? al poner la condición <2 se indica que los casos true hablan de agrupaciones con respuestas uniformes (without_diversity) y las false de with_diversity. El filter recopila los casos true y los asigna a data_without_smoker_diversity
        records_without_smoker_diversity = len(data_without_smoker_diversity)
        groups_without_smoker_diversity = data_without_smoker_diversity.groupby(columnas, observed=True).size()
        classes_without_smoker_diversity = len(groups_without_smoker_diversity)

        resultados_esquemas[nombre] = {
            "data_publicada": observaciones_cumplen,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "quasi_identifiers": columnas,
            "published_records": published_records,
            "suppressed_records": suppressed_records,
            "published_classes": published_classes,
            "records_without_smoker_diversity": records_without_smoker_diversity,
            "classes_without_smoker_diversity": classes_without_smoker_diversity
        }

    schemes = {}


    for nombre, r in resultados_esquemas.items():
        schemes[nombre] = {k: v for k, v in r.items() if k != "data_publicada"} # Para cada uno de los dos esquemas: with_children y without_children se tiene que, nombre es el nombre del respectivo esquema y r es el diccionario con los resultados (las nueve entradas). k serían las llaves de estas nueve entradas y v sus value, finalente, se excluye data_publicada dell nuvo diccionario schemes por el formato de respuesta solicitado


    # ----------------------------------------------------------------------
    # ANÁLISIS DE LOS ITEMS DEL DICCIONARIO NO ANIDADOS EN SCHEMES: ESQUEMAS
    # ----------------------------------------------------------------------
    datos_original_k = datos.groupby(["age", "sex", "bmi", "children", "region"], observed=True).size()
    original_k = int(datos_original_k.min())
    original_unique_records = int(sum(datos_original_k == 1))
    selected_scheme = min(resultados_esquemas, key=lambda n: resultados_esquemas[n]["suppressed_records"])  # n representa los nombres de cada uno de los esquemas: with_children y without_children. El esquema elegido es aquel con menor número de registros suprimidos
    mean_charges_original = float(datos["charges"].mean())
    datos_publicados = resultados_esquemas[selected_scheme]["data_publicada"]   # Del diccionario resultados_esquemas se selecciona a selected_scheme, es decir, el diccionario con menor número de registros suprimidos y luego se toma la entrada data_publicada que contiene el dataframe con los registros que cumplen con k-anonimato=5
    mean_charges_published = float(datos_publicados["charges"].mean())
    smoker_rate_original = (datos["smoker"] == "yes").mean()
    smoker_rate_published = (datos_publicados["smoker"] == "yes").mean()

    # ---------------------------
    # PLANTEAR EL REPORTE FINAL
    # ---------------------------
    reporte = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published
    }


    # -------------------
    # ARCHIVOS DE SALIDA
    # -------------------
    with open(SUBMISSION_PRIVACY, "w") as f:
        json.dump(reporte, f, indent=4)

    COLUMNAS_INSURANCE_PUBLISHED = schemes[selected_scheme]["quasi_identifiers"] + ["smoker", "charges"]
    datos_publicados[COLUMNAS_INSURANCE_PUBLISHED].to_csv(SUBMISSION_INSURANCE, index=False)

    return reporte

# ------------------------
# VALIDACIÓN DE LA FUNCIÓN
# ------------------------
if __name__ == "__main__":
    print(pregunta_01())
