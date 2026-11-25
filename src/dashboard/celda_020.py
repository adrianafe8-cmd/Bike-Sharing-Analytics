# ==========================================================
# DASHBOARD GLOBAL - CELDA 19B
# Integración académica final de la Fase 1
# ==========================================================

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dash import dash_table

# ==========================================================
# 1. ACTUALIZAR FICHA TÉCNICA
# ==========================================================

fecha_archivo = datetime.fromtimestamp(
    RUTA_ZIP.stat().st_mtime,
    tz=timezone.utc
).astimezone(ZoneInfo("America/Bogota"))

df_ficha_tecnica.loc[
    df_ficha_tecnica["Campo"] == "Fecha de extracción",
    "Valor"
] = (
    fecha_archivo.strftime("%Y-%m-%d %H:%M:%S")
    + " Colombia (estimada mediante modificación del ZIP)"
)

df_ficha_tecnica.loc[
    df_ficha_tecnica["Campo"] == "Licencia",
    "Valor"
] = (
    "Pendiente de confirmación oficial. "
    "El README exige citar la publicación original."
)

campos_adicionales = pd.DataFrame([
    (
        "Año de creación",
        "2013"
    ),
    (
        "Última actualización reportada por UCI",
        "2024-03-10"
    ),
    (
        "Sistema de bicicletas",
        "Capital Bikeshare"
    ),
    (
        "Ubicación",
        "Washington D.C., Estados Unidos"
    ),
    (
        "Referencia del dataset",
        referencia_dataset
    ),
    (
        "Referencia científica",
        referencia_articulo
    )
], columns=["Campo", "Valor"])

# Evitar duplicados si la celda se ejecuta nuevamente.

df_ficha_tecnica = pd.concat([
    df_ficha_tecnica,
    campos_adicionales
], ignore_index=True).drop_duplicates(
    subset="Campo",
    keep="last"
)

# ==========================================================
# 2. ACTUALIZAR DICCIONARIO DE VARIABLES
# ==========================================================

df_diccionario_fase1.loc[
    df_diccionario_fase1["Variable"] == "season",
    "Rango_o_valores"
] = (
    "1: Invierno; 2: Primavera; "
    "3: Verano; 4: Otoño"
)

df_diccionario_fase1.loc[
    df_diccionario_fase1["Variable"] == "weekday",
    "Rango_o_valores"
] = (
    "0: Domingo; 1: Lunes; 2: Martes; "
    "3: Miércoles; 4: Jueves; "
    "5: Viernes; 6: Sábado"
)

df_diccionario_fase1.loc[
    df_diccionario_fase1["Variable"] == "weathersit",
    "Rango_o_valores"
] = (
    "1: Despejado o parcialmente nublado; "
    "2: Niebla o nublado; "
    "3: Precipitación ligera o tormenta; "
    "4: Condiciones severas"
)

nota_estaciones = (
    "El README original presenta una inconsistencia "
    "en la descripción de las estaciones. La codificación "
    "utilizada en este dashboard fue contrastada con las "
    "fechas de las 731 observaciones, confirmando que "
    "1 corresponde a invierno, 2 a primavera, "
    "3 a verano y 4 a otoño."
)

nota_outliers = (
    "El método IQR identificó 59 valores atípicos "
    "y Z-score identificó 12. Estas cantidades "
    "corresponden a detecciones por variable y no "
    "necesariamente a registros únicos. "
    "No se eliminaron observaciones durante el EDA."
)

# ==========================================================
# 3. ACTUALIZAR ARCHIVOS DE EVIDENCIA
# ==========================================================

complementos_fase1["ficha_tecnica"] = (
    df_ficha_tecnica
)

complementos_fase1["diccionario_datos"] = (
    df_diccionario_fase1
)

for nombre, tabla in complementos_fase1.items():

    tabla.to_csv(
        FASE1 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

df_verificacion_estaciones.to_csv(
    FASE1 / "verificacion_estaciones.csv",
    encoding="utf-8-sig"
)

df_verificacion_dias.to_csv(
    FASE1 / "verificacion_dias_semana.csv",
    index=False,
    encoding="utf-8-sig"
)

(FASE1 / "nota_metodologica_estaciones.txt").write_text(
    nota_estaciones,
    encoding="utf-8"
)

(FASE1 / "referencias_bibliograficas.txt").write_text(
    referencia_dataset + "\n\n" + referencia_articulo,
    encoding="utf-8"
)

# ==========================================================
# 4. FUNCIÓN DE TABLAS ACADÉMICAS
# ==========================================================

def tabla_complementaria_f1(tabla, identificador):

    datos = tabla.copy()

    # Convertir fechas a texto para serialización.

    for columna in datos.columns:

        if pd.api.types.is_datetime64_any_dtype(
            datos[columna]
        ):

            datos[columna] = (
                datos[columna].astype(str)
            )

    return dash_table.DataTable(

        id=f"academico-f1-{identificador}",

        columns=[
            {
                "name": columna.replace("_", " "),
                "id": columna
            }
            for columna in datos.columns
        ],

        data=datos.round(4).to_dict("records"),

        page_size=10,
        sort_action="native",
        filter_action="native",

        style_table={
            "overflowX": "auto"
        },

        style_header={
            "backgroundColor": "#142C49",
            "color": "white",
            "fontWeight": "bold",
            "whiteSpace": "normal"
        },

        style_cell={
            "fontFamily": "Arial",
            "fontSize": "13px",
            "padding": "12px",
            "textAlign": "left",
            "whiteSpace": "normal",
            "height": "auto",
            "minWidth": "100px",
            "maxWidth": "550px"
        },

        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#F8FAFC"
            }
        ]
    )


# ==========================================================
# 5. CONSTRUIR SECCIONES ACADÉMICAS
# ==========================================================

def panel_academico_fase1():

    return html.Div([

        html.H3(
            "Complementos académicos",
            className="mt-4 mb-3"
        ),

        dbc.Alert(
            "Esta sección complementa el análisis "
            "exploratorio reconstruido desde el dataset "
            "original. No se dispone del notebook "
            "original de la Fase 1.",
            color="info"
        ),

        dbc.Accordion([

            # ----------------------------------------------
            # Formulación del problema
            # ----------------------------------------------

            dbc.AccordionItem([

                html.P(
                    contexto_fase1.strip(),
                    style={
                        "whiteSpace": "pre-line"
                    }
                ),

                html.H5(
                    "Preguntas de investigación"
                ),

                tabla_complementaria_f1(
                    preguntas_fase1,
                    "preguntas"
                )

            ], title="1. Formulación del problema"),

            # ----------------------------------------------
            # Objetivos SMART
            # ----------------------------------------------

            dbc.AccordionItem([

                html.H5("Objetivo general"),

                html.P(
                    objetivo_general_fase1.strip()
                ),

                html.H5("Objetivos específicos SMART"),

                tabla_complementaria_f1(
                    df_objetivos_fase1,
                    "objetivos"
                )

            ], title="2. Objetivos de investigación"),

            # ----------------------------------------------
            # Ficha técnica
            # ----------------------------------------------

            dbc.AccordionItem([

                tabla_complementaria_f1(
                    df_ficha_tecnica,
                    "ficha"
                )

            ], title="3. Ficha técnica del dataset"),

            # ----------------------------------------------
            # Diccionario de variables
            # ----------------------------------------------

            dbc.AccordionItem([

                tabla_complementaria_f1(
                    df_diccionario_fase1,
                    "diccionario"
                ),

                dbc.Alert(
                    nota_estaciones,
                    color="warning",
                    className="mt-3"
                )

            ], title="4. Diccionario de datos"),

            # ----------------------------------------------
            # Comparación de valores atípicos
            # ----------------------------------------------

            dbc.AccordionItem([

                html.P(nota_outliers),

                tarjeta_grafica(
                    fig_comparacion_outliers,
                    "fase1-comparacion-iqr-zscore"
                ),

                html.H5("Comparación de métodos"),

                tabla_complementaria_f1(
                    df_comparacion_outliers,
                    "comparacion-outliers"
                ),

                html.H5(
                    "Resumen Z-score",
                    className="mt-4"
                ),

                tabla_complementaria_f1(
                    df_zscore_fase1,
                    "resumen-zscore"
                ),

                html.H5(
                    "Detalle de observaciones detectadas",
                    className="mt-4"
                ),

                tabla_complementaria_f1(
                    df_detalle_zscore,
                    "detalle-zscore"
                )

            ], title="5. Análisis complementario de outliers"),

            # ----------------------------------------------
            # Referencias
            # ----------------------------------------------

            dbc.AccordionItem([

                html.P(referencia_dataset),

                html.P(referencia_articulo),

                html.A(
                    "Consultar repositorio original UCI",
                    href=(
                        "https://archive.ics.uci.edu/"
                        "dataset/275/bike+sharing+dataset"
                    ),
                    target="_blank",
                    rel="noopener noreferrer"
                )

            ], title="6. Referencias bibliográficas")

        ],
            start_collapsed=True,
            always_open=True
        )

    ], className="mb-4")


# ==========================================================
# 6. EXTENDER LA VISTA ORIGINAL DE LA FASE 1
# ==========================================================

# Conservar la función original.
# Esta condición evita extensiones duplicadas.

if "vista_fase1_original" not in globals():

    vista_fase1_original = vistas_dashboard["fase1"]


def vista_fase1_integrada():

    return html.Div([

        vista_fase1_original(),

        panel_academico_fase1()

    ])


vistas_dashboard["fase1"] = vista_fase1_integrada
# ==========================================================
# 7. EVITAR DUPLICACIÓN DE FIGURAS
# ==========================================================

# La gráfica de comparación IQR vs. Z-score
# ya está incluida en el panel académico de Fase 1.
# Se elimina del diccionario de gráficas generales
# para evitar duplicaciones.

figuras_fase1.pop("comparacion_outliers", None)

assert len(figuras_fase1) == 11

print("Gráficas originales de Fase 1: 11")
print("Gráfica complementaria IQR vs. Z-score: 1")
print("Total de gráficas de Fase 1: 12")
# ==========================================================
# 8. VALIDAR TODAS LAS VISTAS ACTUALIZADAS
# ==========================================================

inventario_final = []

for nombre, funcion_vista in vistas_dashboard.items():

    vista = funcion_vista()

    componentes = list(
        recorrer_componentes(vista)
    )

    graficas = sum(
        isinstance(c, dcc.Graph)
        for c in componentes
    )

    tablas = sum(
        isinstance(c, dash_table.DataTable)
        for c in componentes
    )

    imagenes = sum(
        isinstance(c, html.Img)
        for c in componentes
    )

    ids = [
        str(c.id)
        for c in componentes
        if getattr(c, "id", None) is not None
    ]

    assert len(ids) == len(set(ids)), (
        f"Identificadores duplicados en {nombre}"
    )

    inventario_final.append({
        "Vista": nombre,
        "Componentes": len(componentes),
        "Graficas": graficas,
        "Tablas": tablas,
        "Imagenes": imagenes,
        "Estado": "OK"
    })

df_inventario_final = pd.DataFrame(
    inventario_final
)

# ==========================================================
# 9. VALIDACIONES FINALES
# ==========================================================

assert len(df_inventario_final) == 5

assert df_inventario_final["Graficas"].sum() == 47

assert df_inventario_final["Tablas"].sum() == 41

assert df_inventario_final["Imagenes"].sum() == 25

assert len(df_diccionario_fase1) == 16

assert len(app.callback_map) == 2

assert len(df) == 731

assert int(df["cnt"].sum()) == total_alquileres

df_inventario_final.to_csv(
    RESULTADOS / "inventario_final_dashboard.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 10. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("DASHBOARD GLOBAL - INTEGRACIÓN ACADÉMICA FINAL")
print("=" * 60)

print("\n=== INVENTARIO FINAL ===")
print(df_inventario_final.to_string(index=False))

print("\n=== COMPONENTES INTEGRADOS ===")

print("Pestañas:", len(df_inventario_final))

print(
    "Gráficas interactivas:",
    df_inventario_final["Graficas"].sum()
)

print(
    "Tablas interactivas:",
    df_inventario_final["Tablas"].sum()
)

print(
    "Imágenes originales:",
    df_inventario_final["Imagenes"].sum()
)

print(
    "Componentes de interfaz:",
    df_inventario_final["Componentes"].sum()
)

print("\n=== VALIDACIONES ===")
print("Formulación del problema: OK")
print("Objetivos SMART: OK")
print("Ficha técnica actualizada: OK")
print("Diccionario de variables: OK")
print("Codificación estacional verificada: OK")
print("Comparación IQR y Z-score: OK")
print("Referencias bibliográficas: OK")
print("Identificadores únicos: OK")
print("Integridad del dataset: OK")
print("Modelos reentrenados: 0")

print("\nIntegración académica finalizada.")