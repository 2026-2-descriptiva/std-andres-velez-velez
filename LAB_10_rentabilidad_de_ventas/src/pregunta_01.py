import pandas as pd
import numpy as np
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """
    # SE ESTABLECEN LAS RUTAS DE LOS ARCHIVOS DE DATOS Y DE SALIDA
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_FILE = DATA_DIR / "superstore_orders.csv.gz"
    SUBMISSION_DIR = Path(__file__).parent.parent / "submission"
    SUBMISSION_PROFITABILITY_FILE = SUBMISSION_DIR / "profitability_summary.csv"
    SUBMISSION_DISCOUNT_FILE = SUBMISSION_DIR / "discount_summary.csv"
    SUBMISSION_PRIORITY_FILE = SUBMISSION_DIR / "priority_segments.csv"

    # LECTURA DE DATOS
    datos = pd.read_csv(DATA_FILE, compression='gzip', encoding='utf-8', sep=";")

    # AJUSTE DE STRING A FLOAT
    datos["Sales"] = datos["Sales"].str.replace(",", ".").astype(float)
    datos["Profit"] = datos["Profit"].str.replace(",", ".").astype(float)
    datos["Discount"] = datos["Discount"].str.replace(",", ".").astype(float)

    # ------------------------------
    #CONSTRUCCIÓN DEL PRIMER ARCHIVO
    # ------------------------------
    lines = len(datos['Order ID'])                                                   # Número de filas de los datos
    orders = datos['Order ID'].nunique()                                             # Número de pedidos únicos  
    sales = datos['Sales'].sum()                                                     # Cantidad de ventas totales
    profit = datos["Profit"].sum()                                                   # Cantidad de ganancias totales
    profit_margin = profit / sales                                                   # Margen de ganancia
    datos["perdidas"] = datos["Profit"] < 0                                          # Identificar las filas con pérdidas
    loss_lines = datos["perdidas"].sum()                                             # Total de líneas con pérdidas
    loss_line_rate = datos["perdidas"].mean()                                        # Pérdida promedio por línea, sobre los productos que generan pérdida
    lost_profit = datos.loc[datos["perdidas"], "Profit"].abs().sum()                 # Se agrupa sobre las observaciones que cumplen la condición de pérdidas (profit < 0) y se calcula la suma de las pérdidas absolutas.

    # Construcción de un diccionario con los resultados
    profitability_summary = pd.DataFrame([{
        "lines": lines,
        "orders": orders,
        "sales": sales,
        "profit": profit,
        "profit_margin": profit_margin,
        "loss_lines": loss_lines,
        "loss_line_rate": loss_line_rate,
        "lost_profit": lost_profit
        }])

    with open(SUBMISSION_PROFITABILITY_FILE, "w", encoding="utf-8") as f:
        profitability_summary.to_csv(f, index=False)

    # --------------------------------
    # CONSTRUCCIÓN DEL SEGUNDO ARCHIVO
    # --------------------------------
    datos["discount_band"] = pd.cut(datos["Discount"],                        # Se crea discount_band, creando los bins según la instrucción del ejercicio
                                bins=[-1 , 0, 0.05, 0.1, np.inf],
                                labels=["0%", "1%-5%", "6%-10%", "más de 10%"]
                                )


    datos["perdidas"] = datos["Profit"] < 0                         # Se establece la condición de pérdidas
    datos["perdidas_abs"] = datos["Profit"].clip(upper=0).abs()     # Se reemplazan los valores con ganancias por cero para no afectar la sumatoria de perdidas


    discount_summary = (                                            # Se agrupa por discount band y se busscan todas las combinaciones posibles 
        datos.groupby("discount_band", observed=False).agg(         # Se aplica agg para realizar calculos al interior de cada banda de descuento
            lines=("Order ID", "size"),                             # Los métodos siez, mean y sum se aplican a cada columna indicada
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_line_rate=("perdidas", "mean"),
            lost_profit=("perdidas_abs", "sum")
        )
    )

    discount_summary["profit_margin"] = discount_summary["profit"] / discount_summary["sales"]  # Se crea profit_margin fuera  de discount summary para aprovechar que ya se tiene el cálculo agregado de profit y sales para definir este término fácilmente
    discount_summary = discount_summary.reset_index()                                           # Se resetea el índice

    discount_summary = discount_summary[["discount_band", "lines", "sales", "profit", "profit_margin",
                                        "loss_line_rate", "lost_profit"]]                              # Se determina el orden requerido para el futuro archivo. Se usa doble corchete. El primer es el operador de selección, el segundo para crear una lista

    discount_summary.to_csv(SUBMISSION_DISCOUNT_FILE, index=False)


    # --------------------------------
    # CONSTRUCCIÓN DEL TERCER ARCHIVO
    # --------------------------------
    priority_segments = datos.groupby(["Customer Segment", "Product Category"], observed=False).agg(    # Se agrupa por dos categorías
        lines=("Order ID", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        lost_profit=("perdidas_abs", "sum")
    )

    priority_segments["profit_margin"] = priority_segments["profit"] / priority_segments["sales"]   # Se calcula profit_margin fuera de la agrupación para aprovechar el cálculo de profit y sales ya agregado
    priority_segments = priority_segments.reset_index()

    priority_segments = priority_segments[["Customer Segment", "Product Category", "lines",         # Se incluye profit_margin y se ordena la información
                                           "sales", "profit", "profit_margin", "lost_profit"]]

    priority_segments = priority_segments[priority_segments["lines"] >= 100]                        # Se establece un filtro sobre lines tal como dice el enunciado
    priority_segments = priority_segments.sort_values(by="lost_profit", ascending=False).head(5)    # Se ordena de manera ascendente por lost profit tal como dice el enunciado y se seleccionan las 5 primeras filas

    priority_segments.to_csv(SUBMISSION_PRIORITY_FILE, index=False)

    return profitability_summary, discount_summary, priority_segments



if __name__ == "__main__":
    pregunta_01()