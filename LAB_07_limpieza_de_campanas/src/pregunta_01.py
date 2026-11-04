import pandas as pd
from pathlib import Path


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    DATA_DIR = Path(__file__).parent.parent / "data"
    SUBMISSION_CLIENT = Path(__file__).parent.parent / "submission" / "client.csv"
    SUBMISSION_CAMPAIGN = Path(__file__).parent.parent / "submission" / "campaign.csv"
    SUBMISSION_ECONOMICS = Path(__file__).parent.parent / "submission" / "economics.csv"

    archivos_gz = list(DATA_DIR.glob("*.csv.gz"))   # glob busca todos los archivos al interior de DATA_DIR que cumplan con el patrón *.csv.gz. Se queda con una lista que tiene la ruta completa desde la raíz hasta cada archivo en data
    datos_marketing = [pd.read_csv(archivos) for archivos in archivos_gz]   # Se crea una lista de dataframes que corresponden a los datos de cada archivo contenido en achivos_gz
    datos_consolidados = pd.concat(datos_marketing, ignore_index=True)   # Se concatenan todos los dataframes de la lista datos_marketing en un solo dataframe llamado datos_consolidado. ignore_index=True asegura que los índices se reindexen de manera continua.

    #------------------------
    # PRIMER ARCHVIO 
    # -----------------------

    COLUMNAS_CLIENT_CSV = ["client_id", "age", "job", "marital",        # Se construye una lista con las columnas requeridas en el orden indicado
                          "education", "credit_default", "mortgage"]


    def limpiar_job(series):                                 # Se construye la función auxiliar limpiar_job 
        series = series.str.replace(".", "", regex=False)    # Se eliminan los puntos de la columna job
        series = series.str.replace("-", "_", regex=False)   # Se reemplazan los guiones por guiones bajos en la columna job
        return series

    def limpiar_education(series):
        series = series.str.replace(".", "_", regex=False)    # Se reemplazan los puntos por guiones bajos en la columna education
        series = series.mask(series == "unknown")             # Se usa mask para que en todas aquellas oportunidades en que haya una observación con unknown se tenga un NaN como salida
        return series

    def limpiar_credit_default_y_mortgage(series):            # Se construye la función auxiliar limpiar_credit_default_y_mortgage
        return (series == "yes").astype(int)                  # Si series == "yes" astype(int) devuelve 1, de lo contrario devuelve 0


    client = datos_consolidados[COLUMNAS_CLIENT_CSV].copy()   # Se crea un dataframe client que contiene las columnas indicadas en COLUMNAS_CLIENT_CSV sobre el cual realizar el procesamiento ya construido en las funciones
    client["job"] = limpiar_job(client["job"])                # Se aplica la función limpiar_job a la columna job del dataframe client
    client["education"] = limpiar_education(client["education"])
    client["credit_default"] = limpiar_credit_default_y_mortgage(client["credit_default"])
    client["mortgage"] = limpiar_credit_default_y_mortgage(client["mortgage"])


    # -----------------------
    # SEGUNDO ARCHIVO 
    # -----------------------

    COLUMNAS_CAMPAIGN_CSV = ["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", 
                            "previous_outcome","campaign_outcome", "last_contact_date"]


    MESES = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}


    def limpiar_previous_outcome(series):                 # Se construye la función auxiliar limpiar_previous_outcome
        return (series == "success").astype(int)


    def limpiar_campaign_outcome(series):                 # Se construye la función auxiliar limpiar_campaign_outcome
        return (series == "yes").astype(int)


    def construir_last_contact_date(datos_consolidados, año=2022):      # Se construye la función auxiliar construir_last_contact_date
        fecha = pd.to_datetime(pd.DataFrame({"year": año,
                                            "month": datos_consolidados["month"].map(MESES),
                                            "day": datos_consolidados["day"]}))
        return fecha.dt.strftime("%Y-%m-%d")

    datos_consolidados["last_contact_date"] = construir_last_contact_date(datos_consolidados)   # Se aplica la función construir_last_contact_date a los datos consolidados para crear la columna last_contact_date


    campaign = datos_consolidados[COLUMNAS_CAMPAIGN_CSV].copy()   # Se crea un dataframe campaign que contiene las columnas indicadas en COLUMNAS_CAMPAIGN_CSV sobre el cual realizar el procesamiento ya construido en las funciones
    campaign["previous_outcome"] = limpiar_previous_outcome(campaign["previous_outcome"])
    campaign["campaign_outcome"] = limpiar_campaign_outcome(campaign["campaign_outcome"])


    # -----------------------
    # TERCER ARCHIVO
    # -----------------------

    COLUMNAS_ECONOMICS_CSV = ["client_id", "cons_price_idx", "euribor_three_months"]  # Se construye una lista con las columnas requeridas en el orden indicado

    economcis = datos_consolidados[COLUMNAS_ECONOMICS_CSV].copy()   # Se crea un dataframe economcis que contiene las columnas indicadas en COLUMNAS_ECONOMICS_CSV sobre el cual realizar el procesamiento ya construido en las funciones


    # Guardado de las tablas
    client.to_csv(SUBMISSION_CLIENT, sep=",",index=False)
    campaign.to_csv(SUBMISSION_CAMPAIGN, sep=",", index=False)
    economcis.to_csv(SUBMISSION_ECONOMICS, sep=",", index=False)


    return client, campaign, economcis

if __name__ == "__main__":
    clean_campaign_data()