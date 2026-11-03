import pandas as pd
from pathlib import Path
import os


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    # DEFINICION DE RUTAS, ARCHIVOS DE ENTRADA Y SALIDA
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "solicitudes_de_credito.csv.gz"
    SUBMISSION_FILE = Path(__file__).parent.parent / "submission" / "solicitudes_de_credito.csv"

    # DEFINICIÓN DE LISTAS SEGÚN LAS INDICACIONES: COLUMNAS REQUERIDAS, COLUMNAS TIPO TEXTO, COLUMNAS CON FALTANTES Y OBSERVACIONES NULAS
    REQUERIDAS = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato","comuna_ciudadano",
                   "fecha_de_beneficio", "monto_del_credito", "línea_credito"]

    COLUMNAS_TIPO_TEXTO = ["sexo", "tipo_de_emprendimiento", "idea_negocio",
                          "barrio", "línea_credito"]

    COLUMNA_CON_FALTANTES = "comuna_ciudadano"

    OBSERVACIONES_NULAS = [" ", "", "nan", "none", "null", "n/a", "na", "s/d"]


    # CONSTRUCCIÓN DE FUNCIONES AUXILIARES

    # LIMPIEZA DE TEXTO: FILAS
    def limpiar_texto(series):
        series = series.astype("string").str.lower()    # Se pone el contenido de los campos de cada columna en minúsculas, menos los encabezados
        series = series.str.replace("_", " ")           # Se reemplaza el "_" por un espacio en blanco
        series = series.str.replace(r"[-]", " ", regex=True)    # # Se identificó que no sólo hay que reemplazar espacios en blanco, luego, se debe usar una expresión regular que identifique los diferentes
        series = series.str.replace(r"\s+", " ", regex=True)    # Se reemplaza cualquier tipo de espacio en blanco por un espacio en blanco
        return series.mask(series.isin(OBSERVACIONES_NULAS))    # La función retorna series con el tratamiento anterior, pero además mask deja explícitamente con NA a todos los campos que contenga los elementos presentes en OBSERVACIONES_NULAS


    # LIMPIEZA DE ESTRATO
    def limpiar_estrato(series):
        numero_estrato = series.astype("string").str.extract(r"(\d+)", expand=False)    # Se extrae de cada campo la primera secuencia de digitos que aparezca  hasta que esta se corte por cualquier caracter diferente a un dígito
        return pd.to_numeric(numero_estrato, errors="coerce")                           # Se convierte cada serie de dígitos extraído (extraído como string) a un valor numérico


    # LIMPIEZA DE MONTO DE CRÉDITO
    def limpiar_monto_credito(series):
        series = series.astype("string").str.replace(r"[^\d.,]", "", regex=True)    # Al tener ^ dentro del corchete se indica que todo caracter que no sea un digito coma o punto debe reemplazarse por un string vacío, es decir, eliminarse
        series = series.str.replace(r"[.,]\d{1,2}$", "", regex=True)                # El regex empieza buscando donde esté un . o una , y luego si se tiene una secuencia de 1 o 2 dígitos al final del string se reemplaza por un string vacío, es decir, se elimina
        series = series.str.replace(r"\D", "", regex=True)                          # Se reemplaza cualquier caracter que no sea un dígito por un string vacío, es decir, se elimina
        series = series.mask(series == "")                                          # Todo campo vacío es reemplzada por mask con un NA
        return pd.to_numeric(series, errors="coerce")


    # LIMPIEZA DE LAS FECHAS
    def limpiar_fecha(series):
        series = series.astype("string").str.strip()               # Se eliminanlos espacios en blanco al inicial y al final
        series = series.str.replace(r"[/._]", "-", regex=True)     # Se reemplaza cualquier separador de fechas (/ . _) y se reemplaza por -

        resultado = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")    # pd.NaT significa Not a Time y corresponde a valores faltantes para las fechas. Con index = series.index resultado mantendrpa los mismos índices de series. resultado es uan serie que tiene el índice y dimensiones de series, pero todos sus valroes son NaT

        patrones = [                                               # Lista de tuplas, el primer elemento indica como está compuesta la fecha, el segundo indica las dos formas en que puede interpretarse
            (r"\d{4}-\d{1,2}-\d{1,2}", ["%Y-%m-%d", "%Y-%d-%m"]),
            (r"\d{1,2}-\d{1,2}-\d{4}", ["%d-%m-%Y", "%m-%d-%Y"])
        ]

        for patron, formato in patrones:
            coincidencias_formato = series.str.fullmatch(patron).fillna(False).astype(bool)   # Para el series tratado anteriormente se dan dos posibles tratamientos: True cuando coincide el patron y False cuando se tiene un dato faltante o cuando no cumple el patron
            for interpretacion in formato:
                por_clasificar = coincidencias_formato & resultado.isna()                     # Se buscan las fechas que cumplen el patron (coincidencia:formato) y que no han sido clasifcadas (resultado isna())
                if not por_clasificar.any():                                                  # Si no hay fechas que cumplan el patron y que no hayan sido clasificadas, se sale del ciclo
                  break                                                                       # Se detiene el loop cuando ya no haya en resultados un NA que cumpla el patron (que sea true)
                resultado[por_clasificar] = pd.to_datetime(series[por_clasificar], format=interpretacion, errors="coerce")  # Para todos los elementos en por_clasificar que sean true se hace la conversión a fecha según el formato de interpretacion

        return resultado

    # ---------------------
    # LECTURA DE LOS DATOS
    # ---------------------
    datos_credito = pd.read_csv(DATA_FILE, dtype=str, sep=";")
    datos_credito_final = datos_credito[REQUERIDAS].copy()


    # LIMPIEZ DE LAS COLUMNAS TIPO TEXTO
    for col in COLUMNAS_TIPO_TEXTO:
        datos_credito_final[col] = limpiar_texto(datos_credito_final[col])


    # LIMPIEZA DE ESTRATO, MONTO Y FECHA
    datos_credito_final["estrato"] = limpiar_estrato(datos_credito_final["estrato"])
    datos_credito_final["monto_del_credito"] = limpiar_monto_credito(datos_credito_final["monto_del_credito"])
    datos_credito_final["fecha_de_beneficio"] = limpiar_fecha(datos_credito_final["fecha_de_beneficio"])


    # VALIDAR FORMATO: COMUNA CIUDADANO
    datos_credito_final[COLUMNA_CON_FALTANTES] = pd.to_numeric(
    datos_credito_final[COLUMNA_CON_FALTANTES], errors="coerce").astype("Int64")


    # DEPURACIÓN DE DATOS FALTANTES DE LAS COLUMNAS REQUERIDAS NO PERMITIDAS
    columnas_requeridas = [c for c in REQUERIDAS if c != COLUMNA_CON_FALTANTES]
    datos_credito_final = datos_credito_final.dropna(subset=columnas_requeridas)


    # AJUSTE DE FORMATO: ENTEROS O FECHA
    datos_credito_final["estrato"] = datos_credito_final["estrato"].astype("int64")
    datos_credito_final["monto_del_credito"] = datos_credito_final["monto_del_credito"].astype("int64")
    datos_credito_final["fecha_de_beneficio"] = datos_credito_final["fecha_de_beneficio"].dt.strftime("%Y-%m-%d")

    # Validación de duplicados
    datos_credito_final = datos_credito_final.drop_duplicates().reset_index(drop=True)


    # CREACIÓN DEL ARCHIVO DE SALIDA
    datos_credito_final.to_csv(SUBMISSION_FILE, sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()

