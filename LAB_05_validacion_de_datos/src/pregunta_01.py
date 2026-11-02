import pandas as pd
from pathlib import Path
import json

def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "ventas.csv.gz"
    RESULT_FILE = Path(__file__).parent.parent / "submission" / "data_quality_report.json"

    # Lectura de los datos
    data_ventas = pd.read_csv(DATA_FILE, dtype=str, keep_default_na=False, encoding="utf-8-sig")   
    data_ventas.columns = data_ventas.columns.str.strip().str.lower().str.replace(" ", "_")         # dtype=str garantiza una lectura del archivo que guarda la información original
                                                                                                    # keep_default_na=False hace que los términos comunes asociados a valores faltantes no sean declarados inmediantamente como NaN por pandas
                                                                                                    # utf-8-sig elimina la marca BOM

    # Se definen los campos requeridos según lo que se establece en la instrucción
    REQUIRED = ["supplier_id", "supplier", "country", "city", "purchase_date", 
                "amount", "discount", "weight", "units", "unit_price", "contact_email"]

    # Al realizar la lectura usando encoding="utf-8-sig", se hace necesario definir que será considerando NA
    MISSING_VALUES = ["", "N/A"]

    # También se hará uso de expresiones regulares para identificar los correos que no cumplan con el formato
    EMAIL_PATTERN = r"[^@\s]+@[^@\s]+.[^@\s]+"

    # Validación de filas y columnas
    row_count = int(data_ventas.shape[0])  # cantidad de filas
    column_count = int(data_ventas.shape[1])  # cantidad de columnas

    # Validación de columnas requeridas y no necesarias
    missing_required_columns = sorted(set(REQUIRED) - set(data_ventas.columns)) # Se usa set para operar entre ambos conjuntos
    unexpected_columns = sorted(set(data_ventas.columns) - set(REQUIRED))

    # Validación de duplicados
    duplicate_row_count = int(data_ventas.duplicated().sum())

    if "supplier_id" in data_ventas.columns:
        duplicate_supplier_id_count = int(data_ventas.duplicated(subset=["supplier_id"], keep=False).sum()) # subset para analizar los duplicados sobre supplier_id y keep=False para marcar todas las apariciones como repetidas, sin exlcuir la primera

    else:
        duplicate_supplier_id_row_count = 0

    # Validación de faltantes
    missing_value_count_by_column = {
        col: int(n) for col, n in data_ventas.isin(MISSING_VALUES).sum().items()    # Se analiza la cantidad de valores faltantes por columna siguiendo la definición de MISSING_VALUES. Con el .items() se crea el par clave, valor 
    }

    # Validación de correos sin el formato requerido
    if "contact_email" in data_ventas.columns:
        email_valido = data_ventas["contact_email"].str.fullmatch(EMAIL_PATTERN)  # Se usa str.fullmatch para validar que cada correo cumpla con el formato de la expresión regular definido en EMAIL_PATTERN
        invalid_email_count = int((~email_valido).sum())                          # Se usa ~ para indicar la negación. email_valido busca los emails validos, ~email_valido busca los emails invalidos

    else: 
        invalid_email_count = 0

  # Validación de enteros no positivos
    if "units" in data_ventas.columns:
        elementos = pd.to_numeric(data_ventas["units"], errors="coerce").dropna()
        no_positivo = elementos <=0
        no_entero = elementos % 1 != 0   # Se define no entero como todo número que tenga un residuo diferente de 0 al dividir el valor que toma elementos en ese bucle y lo divide entre 1
        invalid_unit_count = int((no_positivo | no_entero).sum())

    else:
        invalid_unit_count = 0

  # Validación de nombre de país
    if "country" in data_ventas.columns:
        paises = data_ventas["country"]
        country_values = sorted(paises[~paises.isin(MISSING_VALUES)].unique())  # Se organizan los países, es decir, los resultados de data_ventas["country"], excluyendo los NA con ~paises

    else:
        country_values = []

  # Generar el diccionario con el reporte
    reporte = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values
    }

    # Generar el diccionario en formato .json en submission
    with open(RESULT_FILE, "w", encoding="utf-8") as f:         
        json.dump(reporte, f, ensure_ascii=False, indent=4)     # Se pone el contenido de reporte en el nuevo file (f)
                                                                # ensure_ascii= False hace que se puedan leer caracteres especiales como tildes o ñ.indent=4 hace que el diccionario no sea una única línea muy extensa

    return reporte

if __name__ == "__main__":
    main()


# ----------------------------------------------------------
# VALIDAR PREGUNTA
# ----------------------------------------------------------
print(main)
                                                                                            