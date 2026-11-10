import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    # DEFINICIÓN DE LAS RUTAS
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "sales.csv.gz"
    SUBMISSION_DIR = Path(__file__).parent.parent / "submission"
    SUBMISSION_FILE_1 = SUBMISSION_DIR / "cohort_retention.csv"
    SUBMISSION_FILE_PNG = SUBMISSION_DIR / "cohort_retention_heatmap.png"

    # LECTURA DE LOS DATOS
    datos = pd.read_csv(DATA_FILE, compression='gzip')

    # GENERACIÓN DE LAS COLUMNAS REQUERIDAS
    datos["cohort_month"] = datos.groupby("CustomerID")["OrderDate"].transform("min").str.extract(r"(^.{7})")  # Usar expresiones regulares para extraer el mes en el formato requerido. Se agrupa por CustomerID pero se aplica el min sobre OrderDate
    datos["cohort_month_mm"] = datos["cohort_month"].str.extract(r"(.{2}$)").astype(int)                       # Usar expresiones regulares para extraer el mes en el formato requerido. Se extrae los últimos 2 caracteres de la fecha y se convierte a entero
    datos["order_month"] = datos["OrderDate"].str.extract(r"^.{5}(.{2})").astype(int)                          # Usar expresiones regulares para extraer el mes en el formato requerido. Se extraen los caracteres 6 y 7
    datos["period_index"] = datos["order_month"] - datos["cohort_month_mm"] 

    datos["active_customers"] = datos.groupby(["cohort_month", "period_index"])["CustomerID"].transform("nunique")  # Se agrupa por cohort_month y period_index y se aplica nunique sobre CustomerID para obtener el número de clientes activos
    datos["cohort_size"] = datos.groupby(["cohort_month"])["CustomerID"].transform("nunique")                       # Se agrupa por cohort_month y se aplica nunique sobre CustomerID para obtener el tamaño de la cohorte
    datos["retention_rate"] = datos["active_customers"] / datos["cohort_size"]

    # GENERACIÓN DE LA TABLA DE RETENCIÓN    
    COLUMNAS_COHORT_RETENTION = ["cohort_month", "period_index", "active_customers", "cohort_size", "retention_rate"]
    datos_cohort_retention = datos[COLUMNAS_COHORT_RETENTION].drop_duplicates().sort_values(by=["cohort_month", "period_index"]).reset_index(drop=True)

    # GENERACIÓN DEL GRÁFICO
    datos_grafico = datos_cohort_retention.pivot(index="cohort_month", columns="period_index", values="retention_rate")
    cohort_retention_heatmap = sns.heatmap(datos_grafico, annot=True, fmt=".0%", cmap="YlGnBu", cbar_kws={"label": "Retention Rate"})

    # GUARADAR LOS ARCHIVOS
    with open(SUBMISSION_FILE_1, "w") as f:
       datos_cohort_retention.to_csv(f, index=False)

    plt.savefig(SUBMISSION_FILE_PNG, bbox_inches="tight", dpi=300)

    return datos_cohort_retention

if __name__ == "__main__":
    build_cohort_analysis()

