# ==========================================================
# DASHBOARD GLOBAL - CELDA 15
# Construcción de la interfaz gráfica en Dash
# ==========================================================

import base64
import mimetypes
from pathlib import Path

from dash import Dash, dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc

# ==========================================================
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Bike Sharing Analytics"
)

app.server.config["JSON_AS_ASCII"] = False

ESTILO_FONDO = "#F1F5F9"
ESTILO_ENCABEZADO = "#142C49"
ESTILO_TEXTO = "#334155"

ESTILO_TARJETA = {
    "border": "1px solid #E2E8F0",
    "borderRadius": "12px",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
    "backgroundColor": "#FFFFFF",
    "height": "100%"
}

CONFIG_GRAFICAS = {
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "toImageButtonOptions": {
        "format": "png",
        "scale": 2
    }
}

# ==========================================================
# 2. FUNCIONES AUXILIARES DE FORMATO
# ==========================================================

def formato_entero(valor):

    return f"{int(valor):,}".replace(",", ".")


def formato_decimal(valor, decimales=2):

    return (
        f"{float(valor):,.{decimales}f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def formato_porcentaje(valor, decimales=2):

    return f"{formato_decimal(valor, decimales)} %"


# ==========================================================
# 3. COMPONENTES REUTILIZABLES
# ==========================================================

# 3.1 Tarjetas de indicadores KPI.

def tarjeta_kpi(titulo, valor, descripcion="",
                color="#2563EB"):

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                titulo,
                style={
                    "fontSize": "13px",
                    "color": "#64748B",
                    "fontWeight": "600"
                }
            ),

            html.H3(
                valor,
                style={
                    "color": color,
                    "fontWeight": "700",
                    "marginTop": "10px",
                    "marginBottom": "8px"
                }
            ),

            html.Small(
                descripcion,
                style={"color": "#64748B"}
            )
        ]),
        style={
            **ESTILO_TARJETA,
            "borderTop": f"4px solid {color}"
        }
    )


# 3.2 Fila adaptable de indicadores.

def fila_kpis(indicadores):

    return dbc.Row(
        [
            dbc.Col(
                tarjeta_kpi(*indicador),
                xs=12,
                sm=6,
                lg=3,
                className="mb-3"
            )
            for indicador in indicadores
        ],
        className="g-3 mb-3"
    )


# 3.3 Encabezado de sección.

def encabezado_seccion(titulo, descripcion=""):

    return html.Div([
        html.H3(
            titulo,
            style={
                "fontWeight": "700",
                "color": ESTILO_ENCABEZADO
            }
        ),

        html.P(
            descripcion,
            style={"color": "#64748B"}
        )
    ], className="mt-3 mb-3")


# 3.4 Bloque de interpretación metodológica.

def nota_metodologica(titulo, contenido,
                      color="info"):

    return dbc.Alert(
        [
            html.Strong(titulo),
            html.P(
                contenido,
                className="mb-0 mt-2"
            )
        ],
        color=color,
        className="mb-4"
    )


# 3.5 Tarjeta de gráfica interactiva.

def tarjeta_grafica(figura, identificador=None):

    # Crear una copia para conservar la figura original.
    figura_visual = go.Figure(figura)

    figura_visual.update_layout(
        autosize=True,
        height=450,
        margin=dict(
            l=65,
            r=35,
            t=80,
            b=100
        )
    )

    parametros = {
        "figure": figura_visual,
        "config": CONFIG_GRAFICAS,
        "responsive": True,
        "style": {
            "height": "450px",
            "minHeight": "450px",
            "width": "100%"
        }
    }

    if identificador is not None:
        parametros["id"] = identificador

    return dbc.Card(
        dbc.CardBody(
            dcc.Graph(**parametros),
            style={
                "padding": "12px",
                "minHeight": "474px"
            }
        ),
        style={
            **ESTILO_TARJETA,
            "height": "auto",
            "minHeight": "474px",
            "width": "100%",
            "overflow": "hidden"
        },
        className="mb-3"
    )

# 3.6 Cuadrícula de gráficas.

def cuadricula_graficas(figuras, prefijo,
                        columnas=2):

    ancho = 12 if columnas == 1 else 6

    return dbc.Row(
        [
            dbc.Col(
                tarjeta_grafica(
                    figura,
                    f"{prefijo}-{nombre}"
                ),
                xs=12,
                md=12,
                lg=ancho,
                className="mb-3",
                style={
                    "minWidth": "0",
                    "height": "auto"
                }
            )
            for nombre, figura in figuras.items()
        ],
        className="g-3",
        style={
            "alignItems": "flex-start"
        }
    )

# 3.7 Tablas interactivas.

def tabla_interactiva(dataframe, pagina=10):

    datos = dataframe.copy()

    for columna in datos.columns:

        if pd.api.types.is_datetime64_any_dtype(
            datos[columna]
        ):
            datos[columna] = (
                datos[columna].astype(str)
            )

        elif pd.api.types.is_float_dtype(
            datos[columna]
        ):
            datos[columna] = (
                datos[columna].round(6)
            )

    datos = datos.astype(object).where(
        pd.notna(datos),
        None
    )

    return dash_table.DataTable(
        data=datos.to_dict("records"),

        columns=[
            {
                "name": str(columna).replace("_", " "),
                "id": str(columna)
            }
            for columna in datos.columns
        ],

        page_size=pagina,
        page_action="native",
        sort_action="native",
        filter_action="native",

        export_format="csv",

        style_table={
            "overflowX": "auto"
        },

        style_header={
            "backgroundColor": "#142C49",
            "color": "white",
            "fontWeight": "bold",
            "padding": "12px"
        },

        style_cell={
            "fontFamily": "Arial",
            "fontSize": "12px",
            "padding": "10px",
            "textAlign": "left",
            "whiteSpace": "normal",
            "height": "auto",
            "minWidth": "100px",
            "maxWidth": "450px"
        },

        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#F8FAFC"
            }
        ]
    )


# 3.8 Sección desplegable de tablas.

def panel_tablas(tablas):

    return dbc.Accordion(
        [
            dbc.AccordionItem(
                tabla_interactiva(tabla),
                title=titulo
            )
            for titulo, tabla in tablas.items()
        ],
        start_collapsed=True,
        always_open=True,
        className="mb-4"
    )


# 3.9 Convertir imágenes originales a Base64.
# Permite visualizarlas sin depender de rutas públicas.

def imagen_base64(ruta):

    ruta = Path(ruta)

    assert ruta.is_file(), (
        f"No se encontró la imagen: {ruta}"
    )

    tipo_mime = (
        mimetypes.guess_type(str(ruta))[0]
        or "image/png"
    )

    contenido = base64.b64encode(
        ruta.read_bytes()
    ).decode("utf-8")

    return f"data:{tipo_mime};base64,{contenido}"


# 3.10 Galería de evidencias originales.

def galeria_imagenes(inventario):

    if inventario.empty:

        return html.P(
            "No se dispone de imágenes originales."
        )

    assert "Ruta" in inventario.columns, (
        "El inventario no contiene la columna Ruta."
    )

    tarjetas = []

    for _, registro in inventario.iterrows():

        ruta = Path(registro["Ruta"])

        nombre = ruta.stem.replace("_", " ")

        tarjetas.append(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        nombre,
                        style={
                            "fontWeight": "600",
                            "fontSize": "13px"
                        }
                    ),

                    dbc.CardBody(
                        html.Img(
                            src=imagen_base64(ruta),
                            alt=nombre,
                            style={
                                "width": "100%",
                                "height": "auto",
                                "objectFit": "contain"
                            }
                      )
                    )
                ], style=ESTILO_TARJETA),

                xs=12,
                lg=6,
                className="mb-3"
            )
        )

    return dbc.Row(
        tarjetas,
        className="g-3"
    )


# 3.11 Panel desplegable de evidencias.

def panel_evidencias(inventario):

    return dbc.Accordion([
        dbc.AccordionItem(
            galeria_imagenes(inventario),
            title=(
                f"Evidencias gráficas originales "
                f"({len(inventario)})"
            )
        )
    ], start_collapsed=True, className="mb-4")


# ==========================================================
# 4. PESTAÑA: RESUMEN EJECUTIVO
# ==========================================================

def vista_resumen():

    return html.Div([

        encabezado_seccion(
            "Resumen ejecutivo",
            "Visión integral de la demanda de bicicletas "
            "y los resultados de las cuatro fases."
        ),

        fila_kpis([
            (
                "Total de alquileres",
                formato_entero(total_alquileres),
                "Periodo 2011–2012",
                "#2563EB"
            ),
            (
                "Promedio diario",
                formato_entero(round(promedio_diario)),
                "Alquileres por día",
                "#0D9488"
            ),
            (
                "Crecimiento anual",
                "+" + formato_porcentaje(
                    crecimiento_anual
                ),
                "2012 frente a 2011",
                "#16A34A"
            ),
            (
                "Completitud",
                formato_porcentaje(
                    porcentaje_completitud, 0
                ),
                "Sin valores faltantes",
                "#7C3AED"
            )
        ]),

        # Filtros que se conectarán en la celda 16.

        dbc.Card(
            dbc.CardBody([
                html.H5("Filtros de demanda"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Año"),

                        dcc.Dropdown(
                            id="filtro-anio",
                            options=[
                                {
                                    "label": "Todos",
                                    "value": "todos"
                                },
                                {
                                    "label": "2011",
                                    "value": "2011"
                                },
                                {
                                    "label": "2012",
                                    "value": "2012"
                                }
                            ],
                            value="todos",
                            clearable=False
                        )
                    ], xs=12, md=4),

                    dbc.Col([
                        html.Label("Tipo de usuario"),

                        dcc.Dropdown(
                            id="filtro-usuario",
                            options=[
                                {
                                    "label": "Todos",
                                    "value": "cnt"
                                },
                                {
                                    "label": "Registrados",
                                    "value": "registered"
                                },
                                {
                                    "label": "Casuales",
                                    "value": "casual"
                                }
                            ],
                            value="cnt",
                            clearable=False
                        )
                    ], xs=12, md=4),

                    dbc.Col([
                        html.Label("Granularidad"),

                        dcc.Dropdown(
                            id="filtro-granularidad",
                            options=[
                                {
                                    "label": "Diaria",
                                    "value": "diaria"
                                },
                                {
                                    "label": "Mensual",
                                    "value": "mensual"
                                }
                            ],
                            value="mensual",
                            clearable=False
                        )
                    ], xs=12, md=4)

                ], className="g-3"),

                html.Div(
                    id="kpis-filtrados",
                    className="mt-3"
                )

            ]),

            style=ESTILO_TARJETA,
            className="mb-4"
        ),

        tarjeta_grafica(
            figuras_resumen["demanda_mensual"],
            "grafica-demanda-filtrada"
        ),

        cuadricula_graficas(
            {
                nombre: figura
                for nombre, figura
                in figuras_resumen.items()
                if nombre != "demanda_mensual"
            },
            "resumen"
        ),

        encabezado_seccion(
            "Hallazgos principales"
        ),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Badge(
                            registro["Fase"],
                            color="primary",
                            className="mb-2"
                        ),

                        html.H6(
                            registro["Hallazgo"],
                            style={"fontWeight": "600"}
                        ),

                        html.P(
                            registro["Implicacion"],
                            className="mb-0",
                            style={"fontSize": "14px"}
                        )
                    ]),
                    style=ESTILO_TARJETA
                ),
                xs=12,
                lg=6,
                className="mb-3"
            )
            for _, registro
            in df_hallazgos_globales.iterrows()
        ], className="g-3"),

        encabezado_seccion(
            "Resultados y trazabilidad"
        ),

        panel_tablas({
            "Indicadores ejecutivos":
                df_indicadores_ejecutivos,

            "Resultados globales de regresión":
                df_regresion_global,

            "Clasificación por protocolo":
                df_clasificacion_global,

            "Inventario de fases":
                inventario_fases,

            "Limitaciones metodológicas":
                df_limitaciones_globales
        }),

        nota_metodologica(
            "Interpretación de resultados",
            "Las comparaciones de regresión son "
            "contextuales. Los resultados de clasificación "
            "de las fases 3 y 4 corresponden a protocolos "
            "diferentes y no permiten establecer un "
            "ganador global.",
            "warning"
        )
    ])


# ==========================================================
# 5. PESTAÑA: FASE 1 - EDA
# ==========================================================

def vista_fase1():

    return html.Div([

        encabezado_seccion(
            "Fase 1 — Análisis exploratorio de datos",
            "Caracterización estadística, calidad y "
            "relaciones entre las variables."
        ),

        fila_kpis([
            (
                "Registros",
                formato_entero(len(df)),
                "Observaciones diarias",
                "#2563EB"
            ),
            (
                "Variables originales",
                str(df.shape[1]),
                "Dataset day.csv",
                "#0D9488"
            ),
            (
                "Valores faltantes",
                str(int(df.isna().sum().sum())),
                "Completitud del 100 %",
                "#16A34A"
            ),
            (
                "Duplicados",
                str(int(df.duplicated().sum())),
                "Registros completos duplicados",
                "#7C3AED"
            )
        ]),

        nota_metodologica(
            "Procedencia de la Fase 1",
            "El análisis exploratorio fue reconstruido "
            "a partir del dataset original, debido a "
            "que no se dispone del notebook inicial."
        ),

        cuadricula_graficas(
            figuras_fase1,
            "fase1"
        ),

        encabezado_seccion(
            "Resultados estadísticos"
        ),

        panel_tablas({
            "Estadísticas descriptivas":
                estadisticas_eda,

            "Frecuencias categóricas":
                df_frecuencias,

            "Correlación de Pearson":
                correlacion_pearson.reset_index(),

            "Correlación de Spearman":
                correlacion_spearman.reset_index(),

            "Factores asociados a la demanda":
                correlacion_demanda.reset_index(),

            "Pruebas Chi-cuadrado":
                df_chi2,

            "Detección de valores atípicos":
                df_outliers_eda,

            "Calidad de datos":
                df_calidad_eda
        }),

        nota_metodologica(
            "Consideraciones estadísticas",
            "La correlación no implica causalidad. "
            "Las pruebas Chi-cuadrado son exploratorias "
            "por la posible dependencia temporal. "
            "casual y registered no deben utilizarse "
            "como predictores de cnt.",
            "warning"
        )
    ])


# ==========================================================
# 6. PESTAÑA: FASE 2 - REGRESIÓN
# ==========================================================

def vista_fase2():

    return html.Div([

        encabezado_seccion(
            "Fase 2 — Regresión simple y múltiple",
            "Evaluación predictiva, comparación de "
            "modelos y análisis complementario en R."
        ),

        fila_kpis([
            (
                "Modelo seleccionado",
                "Múltiple",
                "Menor MAE de validación",
                "#2563EB"
            ),
            (
                "Reducción de MAE",
                formato_porcentaje(mejora_mae_f2),
                "Frente al baseline en validación",
                "#16A34A"
            ),
            (
                "RMSE en prueba",
                formato_decimal(
                    metricas_test_f2["RMSE"]
                ),
                "Alquileres",
                "#0D9488"
            ),
            (
                "R² en prueba",
                formato_decimal(
                    metricas_test_f2["R2"], 4
                ),
                "Regresión múltiple",
                "#7C3AED"
            )
        ]),

        cuadricula_graficas(
            figuras_fase2,
            "fase2"
        ),

        encabezado_seccion(
            "Resultados originales"
        ),

        panel_tablas({
            "Evaluación del modelo seleccionado":
                df_evaluacion_f2,

            "Resultados de prueba":
                df_regresion_global.loc[
                    df_regresion_global["Fase"]
                    == "Fase 2"
                ]
        }),

        panel_evidencias(df_imagenes_f2),

        nota_metodologica(
            "Validación Python y R",
            "El notebook original confirmó la "
            "equivalencia de las predicciones de "
            "LinearRegression y lm(). En R se "
            "identificaron cinco coeficientes no "
            "estimables por singularidades.",
            "warning"
        )
    ])


# ==========================================================
# 7. PESTAÑA: FASE 3 - MODELADO AVANZADO
# ==========================================================

def vista_fase3():

    return html.Div([

        encabezado_seccion(
            "Fase 3 — Modelado avanzado",
            "Regresión regularizada, Random Forest, "
            "KNN, clustering y validación temporal."
        ),

        fila_kpis([
            (
                "Regresor seleccionado",
                mejor_regresion_f3,
                "RMSE de validación",
                "#2563EB"
            ),
            (
                "Clasificador seleccionado",
                mejor_clasificacion_f3,
                "F1 de validación temporal",
                "#0D9488"
            ),
            (
                "Silueta K-Means",
                formato_decimal(
                    df_clustering_f3.loc[
                        df_clustering_f3["Algoritmo"]
                        == "K-Means",
                        "Silueta"
                    ].iloc[0],
                    4
                ),
                "Separación de clústeres",
                "#7C3AED"
            ),
            (
                "Folds utilizables",
                f"{folds_validos_f3}/5",
                "Validación cruzada temporal",
                "#16A34A"
            )
        ]),

        cuadricula_graficas(
            figuras_fase3,
            "fase3"
        ),

        encabezado_seccion(
            "Métricas y configuraciones"
        ),

        panel_tablas({
            "Métricas de regresión":
                df_regresion_f3,

            "Clasificación en prueba":
                df_clasificacion_test_f3,

            "Validación temporal":
                df_clasificacion_cv_f3,

            "Clustering":
                df_clustering_f3,

            "Hiperparámetros seleccionados":
                df_configuraciones_f3,

            "Distribución temporal de clases":
                df_clases_f3,

            "Particiones de validación cruzada":
                df_folds_f3
        }),

        panel_evidencias(df_imagenes_f3),

        nota_metodologica(
            "Limitaciones del modelado avanzado",
            "La validación externa contiene únicamente "
            "demanda alta. Se empleó validación cruzada "
            "temporal con cuatro folds utilizables. "
            "Los coeficientes de silueta evidencian "
            "una separación débil de los clústeres.",
            "warning"
        )
    ])


# ==========================================================
# 8. PESTAÑA: FASE 4 - PREPROCESAMIENTO Y BASELINE
# ==========================================================

def vista_fase4():

    return html.Div([

        encabezado_seccion(
            "Fase 4 — Preprocesamiento y baseline",
            "Ingeniería de características, "
            "transformaciones sin fuga de información "
            "y evaluación de modelos de referencia."
        ),

        fila_kpis([
            (
                "Características predictoras",
                "29",
                "7 numéricas y 22 codificadas",
                "#2563EB"
            ),
            (
                "Accuracy logística",
                formato_porcentaje(
                    accuracy_logistica_f4 * 100, 1
                ),
                "Prueba aleatoria estratificada",
                "#16A34A"
            ),
            (
                "AUC-ROC",
                formato_decimal(
                    auc_logistica_f4, 4
                ),
                "Regresión logística",
                "#0D9488"
            ),
            (
                "Cumplimiento aplicable",
                formato_porcentaje(
                    cumplimiento_pct_f4, 0
                ),
                "Verificación interna",
                "#7C3AED"
            )
        ]),

        cuadricula_graficas(
            figuras_fase4,
            "fase4"
        ),

        encabezado_seccion(
            "Preparación y evaluación de datos"
        ),

        panel_tablas({
            "Resumen de preparación":
                df_preparacion_f4,

            "Métricas baseline de regresión":
                df_regresion_f4,

            "Métricas baseline de clasificación":
                df_clasificacion_f4,

            "Mejoras de los modelos":
                df_mejoras_f4,

            "Valores atípicos":
                df_outliers_f4,

            "Límites de winsorization":
                df_limites_f4,

            "Resultados de winsorization":
                df_winsorization_f4,

            "Codificación de variables":
                df_codificacion_f4,

            "Verificación de StandardScaler":
                df_estandarizacion_f4,

            "Estrategia de balanceo":
                df_balanceo_f4,

            "Dimensiones de matrices finales":
                df_matrices_f4,

            "Cumplimiento de requerimientos":
                df_cumplimiento_f4
        }),

        panel_evidencias(df_imagenes_f4),

        nota_metodologica(
            "Protocolo de evaluación",
            "La regresión utiliza una partición "
            "cronológica y la clasificación una "
            "partición aleatoria estratificada. "
            "El umbral de 3974 alquileres fue heredado "
            "de Fase 3 y existe posible solapamiento "
            "entre los datos usados para estimarlo "
            "y las particiones de Fase 4.",
            "warning"
        )
    ])


# ==========================================================
# 9. ENCABEZADO PRINCIPAL
# ==========================================================

encabezado_dashboard = html.Div([

    dbc.Container([

        html.Div(
            "UNIVERSIDAD DE LA SALLE",
            style={
                "fontSize": "12px",
                "letterSpacing": "2px",
                "color": "#BFDBFE"
            }
        ),

        html.H1(
            "Bike Sharing Analytics",
            style={
                "fontWeight": "700",
                "color": "#FFFFFF",
                "marginTop": "10px"
            }
        ),

        html.P(
            "Dashboard global — Proyecto integrador "
            "de Ciencia de Datos",
            style={
                "fontSize": "17px",
                "color": "#DBEAFE"
            }
        ),

        html.Div(
            "Maestría en Inteligencia Artificial | "
            "Adriana Patricia Fernández Infante",
            style={
                "fontSize": "13px",
                "color": "#CBD5E1"
            }
        ),

        html.Div([
            dbc.Badge(
                "Dataset UCI",
                color="primary",
                className="me-2"
            ),

            dbc.Badge(
                "2011–2012",
                color="secondary",
                className="me-2"
            ),

            dbc.Badge(
                "4 fases integradas",
                color="success"
            )
        ], className="mt-3")

    ], fluid=True)

], style={
    "backgroundColor": ESTILO_ENCABEZADO,
    "padding": "30px 20px",
    "borderBottom": "5px solid #2563EB"
})


# ==========================================================
# 10. NAVEGACIÓN PRINCIPAL
# ==========================================================

navegacion_dashboard = dbc.Tabs([

    dbc.Tab(
        label="Resumen ejecutivo",
        tab_id="resumen"
    ),

    dbc.Tab(
        label="Fase 1 · EDA",
        tab_id="fase1"
    ),

    dbc.Tab(
        label="Fase 2 · Regresión",
        tab_id="fase2"
    ),

    dbc.Tab(
        label="Fase 3 · Modelado avanzado",
        tab_id="fase3"
    ),

    dbc.Tab(
        label="Fase 4 · Baseline",
        tab_id="fase4"
    )

], id="tabs-dashboard",
   active_tab="resumen",
   className="mb-4 mt-4")


# ==========================================================
# 11. PIE DE PÁGINA
# ==========================================================

pie_dashboard = html.Footer([

    html.Hr(),

    html.P(
        "Proyecto Integrador de Ciencia de Datos "
        "— Universidad de La Salle",
        className="mb-1"
    ),

    html.P(
        "Dataset: Bike Sharing Dataset — UCI "
        "Machine Learning Repository.",
        className="mb-1"
    ),

    html.A(
        "Referencia del dataset: DOI 10.24432/C5W894",
        href="https://doi.org/10.24432/C5W894",
        target="_blank"
    ),

    html.P(
        "Resultados recuperados de evidencias "
        "originales. No se reentrenaron modelos.",
        className="mt-2"
    )

], style={
    "fontSize": "12px",
    "color": "#64748B",
    "textAlign": "center",
    "padding": "20px"
})


# ==========================================================
# 12. LAYOUT PRINCIPAL
# ==========================================================

app.layout = html.Div([

    encabezado_dashboard,

    dbc.Container([

        navegacion_dashboard,

        dcc.Loading(
            html.Div(
                id="contenido-dashboard",
                children=vista_resumen()
            ),
            type="circle"
        ),

        pie_dashboard

    ], fluid=True, className="px-3 px-lg-4")

], style={
    "backgroundColor": ESTILO_FONDO,
    "minHeight": "100vh",
    "fontFamily": "Arial, sans-serif",
    "color": ESTILO_TEXTO
})


# ==========================================================
# 13. REGISTRO DE VISTAS
# ==========================================================

vistas_dashboard = {
    "resumen": vista_resumen,
    "fase1": vista_fase1,
    "fase2": vista_fase2,
    "fase3": vista_fase3,
    "fase4": vista_fase4
}


# ==========================================================
# 14. VALIDACIÓN DE COMPONENTES
# ==========================================================

def recorrer_componentes(componente):

    if isinstance(componente, (list, tuple)):

        for elemento in componente:
            yield from recorrer_componentes(elemento)

    elif hasattr(componente, "to_plotly_json"):

        yield componente

        hijos = getattr(
            componente,
            "children",
            None
        )

        if hijos is not None:
            yield from recorrer_componentes(hijos)


inventario_vistas = []

for nombre, funcion_vista in vistas_dashboard.items():

    vista = funcion_vista()

    componentes = list(
        recorrer_componentes(vista)
    )

    ids = [
        componente.id
        for componente in componentes
        if isinstance(
            getattr(componente, "id", None),
            str
        )
    ]

    assert len(ids) == len(set(ids)), (
        f"Identificadores duplicados en {nombre}"
    )

    inventario_vistas.append({
        "Vista": nombre,

        "Componentes": len(componentes),

        "Graficas": sum(
            isinstance(c, dcc.Graph)
            for c in componentes
        ),

        "Tablas": sum(
            isinstance(c, dash_table.DataTable)
            for c in componentes
        ),

        "Imagenes": sum(
            isinstance(c, html.Img)
            for c in componentes
        ),

        "Estado": "OK"
    })


df_inventario_vistas = pd.DataFrame(
    inventario_vistas
)

# ==========================================================
# 15. VALIDACIONES GLOBALES
# ==========================================================

assert len(vistas_dashboard) == 5

assert df_inventario_vistas[
    "Graficas"
].sum() == 46

assert df_inventario_vistas[
    "Imagenes"
].sum() == 25

assert (
    df_inventario_vistas["Estado"] == "OK"
).all()

df_inventario_vistas.to_csv(
    RESULTADOS / "inventario_vistas_dashboard.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 16. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("DASHBOARD GLOBAL - INTERFAZ GRÁFICA DASH")
print("=" * 60)

print("\n=== INVENTARIO DE VISTAS ===")

print(
    df_inventario_vistas.to_string(index=False)
)

print("\n=== COMPONENTES INTEGRADOS ===")

print("Pestañas:", len(vistas_dashboard))

print(
    "Gráficas interactivas:",
    df_inventario_vistas["Graficas"].sum()
)

print(
    "Tablas interactivas:",
    df_inventario_vistas["Tablas"].sum()
)

print(
    "Imágenes originales:",
    df_inventario_vistas["Imagenes"].sum()
)

print(
    "Componentes de interfaz:",
    df_inventario_vistas["Componentes"].sum()
)

print("\n=== VALIDACIONES ===")

print("Aplicación Dash creada: OK")
print("Layout principal: OK")
print("Cinco vistas construidas: OK")
print("Identificadores únicos por vista: OK")
print("Integración de gráficas: OK")
print("Integración de imágenes: OK")
print("Tablas interactivas: OK")

print("\nCallbacks: pendientes de Celda 16")
print("Servidor Dash: pendiente de ejecución")

print(
    "\nInterfaz gráfica construida correctamente."
)