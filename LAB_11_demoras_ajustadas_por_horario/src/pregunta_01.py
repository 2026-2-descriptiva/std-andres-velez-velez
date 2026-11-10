import pandas as pd
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las demás. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aerolínea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """
    # DEFINIR LAS RUTAS
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "flights_by_carrier_day_hour.csv.gz"
    SUBMISSION_DIR = Path(__file__).parent.parent / "submission"
    SUBMISSION_HOURLY_DELAY = SUBMISSION_DIR / "hourly_delay_rates.csv"
    SUBMISSION_CARRIER_ADJUSTED_DELAYS = SUBMISSION_DIR / "carrier_adjusted_delays.csv"

    # CARGAR LOS DATOS
    datos = pd.read_csv(DATA_FILE, compression="gzip")

    # AGRUPACION POR HORA
    agrupacion_x_hora_demora = (datos.groupby("scheduled_departure_hour", as_index=False)                             # Se agrupa por scheduled_departure_hour como indica el enunciado
                                [["operated_flights", "delayed_departure_15_flights"]].sum()                          # Se toman las dos columnas requeridas para calcular el índice y se suma cada agrupación generada para tener los datos listos para generar el índice
                                )
    
    # AGRUPACION POR HORA Y AEROLINEA
    agrupacion_x_aerolinea_y_hora = (datos.groupby(["reporting_airline", "scheduled_departure_hour"], as_index=False) # Se agrupa por aerolínea y hora
                                     [["operated_flights", "delayed_departure_15_flights"]].sum()
                                     )
    
    # AGRUPACION POR HORA: CALCULA DE LA TASA DE DEMORA NACIONAL (TND)
    agrupacion_x_hora_demora["delay_rate"] = (agrupacion_x_hora_demora["delayed_departure_15_flights"] / agrupacion_x_hora_demora["operated_flights"])                                            # Se calcula la TND agrupando por hora
    # AGRUPACION POR AEROLINEA Y HORA: CALCULA LA DEMORA ESPERADA POR AEROLÍNEA Y HORA USANDO LA TND
    agrupacion_x_aerolinea_y_hora_tnd = pd.merge(agrupacion_x_aerolinea_y_hora, agrupacion_x_hora_demora[["delay_rate", "scheduled_departure_hour"]], on="scheduled_departure_hour", how="left")  # Se hace un merge para tener la TND por hora en el dataframe de aerolíneas y horas
    agrupacion_x_aerolinea_y_hora_tnd["expected_delayed_flights"] = (agrupacion_x_aerolinea_y_hora_tnd["delay_rate"] * agrupacion_x_aerolinea_y_hora_tnd["operated_flights"])                                   # Se calcula la demora esperada por aerolínea y hora

    # AGRUPACION POR AEROLINEA: SE AGRUPA POR AEROLINEA NUEVAMENTE PARA OBTENER UNA DEMORA ESPERADA ÚNICA POR AEROLINEA
    agrupacion_aerolinea_tnd = (agrupacion_x_aerolinea_y_hora_tnd.groupby("reporting_airline", as_index=False)                                     # Se agrupa nuevamente por aerolínea dado que en agrupacion_x_aerolinea_y_hora_tnd se agrupó por hora y aerolínea, dando más de una observación para cada aerolínea. Se requiere una sola observación por aerolínea.
                                [["operated_flights", "delayed_departure_15_flights", "expected_delayed_flights"]].sum()
                                )
    # SE APLICA FILTRO POR NÚMERO DE VUELOS OPERADOS
    datos_filtrados = agrupacion_aerolinea_tnd.copy()
    datos_filtrados = datos_filtrados[datos_filtrados["operated_flights"] >= 100000]

    # CALCULO DE LA DEMORA OBSERVADA VS ESPERADA, TASA DE DEMORA, RANKING CRUDO Y RANKING AJUSTADO
    datos_filtrados["observed_to_expected_ratio"] = (datos_filtrados["delayed_departure_15_flights"] / datos_filtrados["expected_delayed_flights"])  # Se calcula la demora observada vs esperada por aerolínea
    datos_filtrados["delay_rate"] = datos_filtrados["delayed_departure_15_flights"] / datos_filtrados["operated_flights"]
    datos_filtrados["crude_rank"] = datos_filtrados["delay_rate"].rank(ascending=False).astype(int)                   # ascending=False para ir de mayor a menor delay, el ranking en enteros para seguir las instrucciones del enunciado
    datos_filtrados["adjusted_rank"] = datos_filtrados["observed_to_expected_ratio"].rank(ascending=False).astype(int)  # ascending=False para ir de mayor a menor razón, el ranking en enteros para seguir las instrucciones del enunciado
    datos_filtrados = datos_filtrados.sort_values("adjusted_rank").reset_index(drop=True)

    # ORDENAR COLUMNAS DE CADA TABLA EN EL ORDEN SOLICITADO
    HOURLY_DELAY_RATES_COLUMNS = ["scheduled_departure_hour", "operated_flights", "delayed_departure_15_flights", "delay_rate"]
    CARRIER_ADJUSTED_DELAYS_COLUMNS = ["reporting_airline", "operated_flights", "delayed_departure_15_flights", "delay_rate",
                                    "expected_delayed_flights", "observed_to_expected_ratio", "crude_rank", "adjusted_rank"]
    
    agrupacion_x_hora_demora = agrupacion_x_hora_demora[HOURLY_DELAY_RATES_COLUMNS]
    datos_filtrados = datos_filtrados[CARRIER_ADJUSTED_DELAYS_COLUMNS]

    # GUARDAR COMO CSV
    with open(SUBMISSION_HOURLY_DELAY, "w") as f:
        agrupacion_x_hora_demora.to_csv(f, index=False)

    with open(SUBMISSION_CARRIER_ADJUSTED_DELAYS, "w") as f:
        datos_filtrados.to_csv(f, index=False)

    return agrupacion_x_hora_demora, datos_filtrados

if __name__ == "__main__":
    pregunta_01()