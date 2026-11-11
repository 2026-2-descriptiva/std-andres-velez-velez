import pandas as pd
from pathlib import Path
import numpy as np

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    # SE DEFINEN LAS RUTAS
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE_LETTER = DATA_DIR / "historical_requests_letter.csv.gz"
    DATA_FILE_WEB = DATA_DIR / "historical_requests_web.csv.gz"
    SUBMISSION_DIR = Path(__file__).parent.parent / "submission"
    SUBMISSION_FILE_CHANNEL = SUBMISSION_DIR / "channel_summary.csv"
    SUBMISSION_FILE_YEARLY = SUBMISSION_DIR / "yearly_summary.csv"
    SUBMISSION_FILE_ENTRY_DAY = SUBMISSION_DIR / "entry_day_summary.csv"

    # SE CARGAN LOS DATOS
    datos_letter = pd.read_csv(DATA_FILE_LETTER, compression='gzip')
    datos_web = pd.read_csv(DATA_FILE_WEB, compression='gzip')

    # LIMPIEZA DE DUPLICADOS
    datos_letter = datos_letter.drop_duplicates()
    datos_web = datos_web.drop_duplicates()

    # CREACION DE LA VARIABLE CHANEL
    datos_letter['channel'] = 'letter'
    datos_web['channel'] = 'web'

    # AJUSTE DE FORMATO: LOS DATOS SON LEIDOS COMO STRGING, SE CONVIERTEN A DATETIME PARA PODER OPERAR CON ELLOS
    datos_letter["in_date"] = pd.to_datetime(datos_letter["in_date"])
    datos_letter["out_date"] = pd.to_datetime(datos_letter["out_date"])
    datos_web["in_date"] = pd.to_datetime(datos_web["in_date"])
    datos_web["out_date"] = pd.to_datetime(datos_web["out_date"])

    # RECLAMACIONES RESUELTAS
    reclamaciones_resueltas_letter = datos_letter["out_date"].notna()   # Las reclamaciones resueltas son aquellas que ya tienen el campo out_date diligenciado, es decir, no nulo
    reclamaciones_resueltas_web = datos_web["out_date"].notna()   # Las reclamaciones resueltas son aquellas que ya tienen el campo out_date diligenciado, es decir, no nulo

    # PREPARACION PARA LA VARIABLE BUSINESS DAYS
    inicio_reclamacion_letter = (datos_letter.loc[reclamaciones_resueltas_letter, "in_date"] + 
                                pd.Timedelta(days=1)).values.astype("datetime64[D]")           # El conteo inicia un día después de la reclamación, por eso el pd.Timedelta(days=1)

    fin_reclamacion_letter = (datos_letter.loc[reclamaciones_resueltas_letter, "out_date"] + 
                              pd.Timedelta(days=1)).values.astype("datetime64[D]")              # Posteriormente, se quiere usar bus_count de numpy y este conteo es un intervalo abierto en el extremo derecho, se suma 1 para cobijar el día de respuesta como pide el enunciado

    inicio_reclamacion_web = (datos_web.loc[reclamaciones_resueltas_web, "in_date"] + 
                              pd.Timedelta(days=1)).values.astype("datetime64[D]")

    fin_reclamacion_web = (datos_web.loc[reclamaciones_resueltas_web, "out_date"] + 
                          pd.Timedelta(days=1)).values.astype("datetime64[D]")

    # CREACIÓN DE BUSINESS DAYS: SE BLINDA ANTE LOS NA PRIMERO
    datos_letter["business_days"] = np.nan      # Se llena la columna business_days con NaN para luego solo llenar los registros que tienen out_date diligenciado y evitar un error
    datos_web["business_days"] = np.nan          
    datos_letter.loc[reclamaciones_resueltas_letter, "business_days"] = np.busday_count(inicio_reclamacion_letter, fin_reclamacion_letter)   # Se aplica el bus_count para hacer el conteo de los días hábiles (se ignoran festivos) se ajustó el intervalo abierto a cerrado anteriormente
    datos_web.loc[reclamaciones_resueltas_web, "business_days"] = np.busday_count(inicio_reclamacion_web, fin_reclamacion_web)

    # CREACIÓN DE LOS DÍAS CALENDARIO: SE BLINDA ANTE LOS NA PRIMERO
    datos_letter["calendar_days"] = np.nan      # Se llena la columna calendar_days con NaN para luego solo llenar los registros que tienen out_date diligenciado
    datos_web["calendar_days"] = np.nan
    datos_letter.loc[reclamaciones_resueltas_letter, "calendar_days"] = (datos_letter["out_date"] - datos_letter["in_date"]).dt.days  
    datos_web.loc[reclamaciones_resueltas_web, "calendar_days"] = (datos_web["out_date"] - datos_web["in_date"]).dt.days   

    # CONCATENACIÓN DE LOS DATAFRAMES
    datos = pd.concat([datos_letter, datos_web], axis=0)

    # CÁLCULO DE INFORMACIÓN POR CANAL
    requests = datos.groupby("channel")["record_id"].size()
    answered = datos[datos["out_date"].notna()].groupby("channel")["record_id"].size()
    pending = datos[datos["out_date"].isna()].groupby("channel")["record_id"].size()
    median_business_days = datos.groupby("channel")["business_days"].median()
    cumple_plazo = datos[datos["business_days"] <= 15].groupby("channel")["record_id"].size()
    on_time_rate = cumple_plazo / requests

    # CREACIÓN DEL CHANEL SUMMARY
    channel_summary = pd.DataFrame({
        "requests": requests,
        "answered": answered,
        "pending": pending,
        "median_business_days": median_business_days,
        "on_time_rate": on_time_rate
    }).reset_index()

    # GUARDAR EL ARCHIVO
    with open(SUBMISSION_FILE_CHANNEL, "w") as f:
        channel_summary.to_csv(f, index=False)

    # CÁLCULO DE INFORMACIÓN POR CANAL Y AÑO DE ENTRADA
    datos["year"] = datos["in_date"].dt.year
    requests = datos.groupby(["year", "channel"])["record_id"].size()
    pending = datos[datos["out_date"].isna()].groupby(["year","channel"])["record_id"].size().reindex(requests.index, fill_value=0)  # Se reindexa para que los años que no tengan pendientes queden con 0 y no con NaN
    cumple_plazo = datos[datos["business_days"] <= 15].groupby(["year", "channel"])["record_id"].size().reindex(requests.index, fill_value=0)  # Se reindexa para que los años que no tengan pendientes queden con 0 y no con NaN
    on_time_rate = cumple_plazo / requests

    yearly_summary = pd.DataFrame({
        "requests": requests,
        "pending": pending,
        "on_time_rate": on_time_rate
    }).reset_index()

    # GUARDAR EL ARCHIVO
    with open(SUBMISSION_FILE_YEARLY, "w") as f:
        yearly_summary.to_csv(f, index=False)

    # CÁLCULO DE INFORMACIÓN POR DÍA DE ENTRADA
    requests = datos.groupby(["day_name"])["record_id"].size()
    median_calendar_days = datos.groupby(["day_name"])["calendar_days"].median()
    median_business_days = datos.groupby(["day_name"])["business_days"].median()

    # ESTABLECER EL ORDEN DE LOS DIAS
    orden_dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    entry_day_summary = pd.DataFrame({
        "requests": requests,
        "median_calendar_days": median_calendar_days,
        "median_business_days": median_business_days
    }).reindex(orden_dias_semana).reset_index()

    # GUARDAR EL ARCHIVO
    with open(SUBMISSION_FILE_ENTRY_DAY, "w") as f:
        entry_day_summary.to_csv(f, index=False)

    return channel_summary, yearly_summary, entry_day_summary

if __name__ == "__main__":
    pregunta_01()
