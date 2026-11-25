# ==========================================================
# DASHBOARD GLOBAL - CELDA 16
# Callbacks, filtros y navegación dinámica
# ==========================================================

from dash import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# ==========================================================
# 1. FUNCIÓN DE NAVEGACIÓN ENTRE PESTAÑAS
# ==========================================================

def seleccionar_vista(pestana):

    # Recuperar la función asociada a la pestaña.
    # Si no existe, mostrar el resumen ejecutivo.

    funcion_vista = vistas_dashboard.get(
        pestana,
        vista_resumen
    )

    return funcion_vista()


# ==========================================================
# 2. FUNCIÓN DE FILTRADO DE DATOS
# ==========================================================

def filtrar_demanda(anio, usuario, granularidad):

    # Validar los parámetros recibidos.

    assert anio in ["todos", "2011", "2012"]

    assert usuario in [
        "cnt",
        "registered",
        "casual"
    ]

    assert granularidad in [
        "diaria",
        "mensual"
    ]

    # Trabajar sobre una copia para no modificar
    # el dataset original.

    datos_filtrados = df.copy()

    # Aplicar filtro de año.

    if anio != "todos":

        datos_filtrados = datos_filtrados.loc[
            datos_filtrados["dteday"].dt.year
            == int(anio)
        ].copy()

    # Orden cronológico.

    datos_filtrados = (
        datos_filtrados
        .sort_values("dteday")
        .reset_index(drop=True)
    )

    assert not datos_filtrados.empty, (
        "No existen registros para la selección."
    )

    # ======================================================
    # 3. CALCULAR INDICADORES DINÁMICOS
    # ======================================================

    alquileres_filtrados = int(
        datos_filtrados[usuario].sum()
    )

    promedio_filtrado = float(
        datos_filtrados[usuario].mean()
    )

    dias_filtrados = int(
        datos_filtrados["dteday"].nunique()
    )

    participacion_filtrada = (
        alquileres_filtrados
        / total_alquileres
        * 100
    )

    indicadores = {
        "Alquileres": alquileres_filtrados,
        "Promedio_diario": promedio_filtrado,
        "Dias_observados": dias_filtrados,
        "Participacion_global": participacion_filtrada
    }

    # ======================================================
    # 4. PREPARAR SERIE TEMPORAL
    # ======================================================

    etiquetas_usuario = {
        "cnt": "Todos los usuarios",
        "registered": "Usuarios registrados",
        "casual": "Usuarios casuales"
    }

    etiqueta_usuario = etiquetas_usuario[usuario]

    if granularidad == "mensual":

        serie = (
            datos_filtrados
            .assign(
                Fecha=datos_filtrados["dteday"]
                .dt.to_period("M")
                .dt.to_timestamp()
            )
            .groupby("Fecha", as_index=False)
            .agg(
                Alquileres=(usuario, "sum")
            )
        )

        titulo_granularidad = "mensual"

    else:

        serie = (
            datos_filtrados[
                ["dteday", usuario]
            ]
            .rename(columns={
                "dteday": "Fecha",
                usuario: "Alquileres"
            })
            .copy()
        )

        titulo_granularidad = "diaria"

    serie["Año"] = (
        serie["Fecha"].dt.year.astype(str)
    )

    # Validar que la agregación conserve los totales.

    assert int(
        serie["Alquileres"].sum()
    ) == alquileres_filtrados

    # ======================================================
    # 5. GENERAR GRÁFICA DINÁMICA
    # ======================================================

    figura = px.line(
        serie,
        x="Fecha",
        y="Alquileres",
        color="Año",
        markers=(granularidad == "mensual"),

        color_discrete_map={
            "2011": COLORES["principal"],
            "2012": COLORES["secundario"]
        },

        title=(
            f"Demanda {titulo_granularidad} "
            f"— {etiqueta_usuario}"
        ),

        labels={
            "Fecha": "Periodo",
            "Alquileres": "Cantidad de alquileres"
        }
    )

    figura.update_traces(
        line_width=(
            3 if granularidad == "mensual"
            else 1.5
        ),

        hovertemplate=(
            "Fecha: %{x|%Y-%m-%d}"
            "<br>Alquileres: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    figura.update_layout(
        template="plotly_white",

        font=dict(
            family="Arial",
            size=12,
            color=COLORES["texto"]
        ),

        title_font_size=17,

        hovermode="x unified",

        height=450,

        margin=dict(
            l=50,
            r=35,
            t=75,
            b=60
        ),

        legend_title_text="Año",

        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    figura.update_xaxes(
        rangeslider_visible=(
            granularidad == "diaria"
        )
    )

    figura.update_yaxes(
        rangemode="tozero"
    )

    return indicadores, figura, serie


# ==========================================================
# 6. FUNCIÓN PARA TARJETAS KPI FILTRADAS
# ==========================================================

def construir_kpis_filtrados(indicadores):

    return fila_kpis([
        (
            "Alquileres seleccionados",
            formato_entero(
                indicadores["Alquileres"]
            ),
            "Según los filtros aplicados",
            "#2563EB"
        ),
        (
            "Promedio diario",
            formato_decimal(
                indicadores["Promedio_diario"]
            ),
            "Alquileres por día observado",
            "#0D9488"
        ),
        (
            "Días observados",
            formato_entero(
                indicadores["Dias_observados"]
            ),
            "Registros del periodo seleccionado",
            "#7C3AED"
        ),
        (
            "Participación global",
            formato_porcentaje(
                indicadores["Participacion_global"]
            ),
            "Sobre el total histórico de alquileres",
            "#16A34A"
        )
    ])


# ==========================================================
# 7. CALLBACK DE NAVEGACIÓN
# ==========================================================

@app.callback(
    Output(
        "contenido-dashboard",
        "children"
    ),

    Input(
        "tabs-dashboard",
        "active_tab"
    )
)

def actualizar_pestana(pestana):

    return seleccionar_vista(pestana)


# ==========================================================
# 8. CALLBACK DE FILTROS INTERACTIVOS
# ==========================================================

@app.callback(
    Output(
        "grafica-demanda-filtrada",
        "figure"
    ),

    Output(
        "kpis-filtrados",
        "children"
    ),

    Input(
        "filtro-anio",
        "value"
    ),

    Input(
        "filtro-usuario",
        "value"
    ),

    Input(
        "filtro-granularidad",
        "value"
    )
)

def actualizar_demanda(
    anio,
    usuario,
    granularidad
):

    indicadores, figura, serie = filtrar_demanda(
        anio,
        usuario,
        granularidad
    )

    tarjetas = construir_kpis_filtrados(
        indicadores
    )

    return figura, tarjetas


# ==========================================================
# 9. PRUEBAS FUNCIONALES DE LOS FILTROS
# ==========================================================

# Se evalúan todas las combinaciones posibles:
#
# 3 opciones de año
# 3 tipos de usuario
# 2 granularidades
#
# Total: 18 combinaciones.

from itertools import product

opciones_anio = [
    "todos",
    "2011",
    "2012"
]

opciones_usuario = [
    "cnt",
    "registered",
    "casual"
]

opciones_granularidad = [
    "diaria",
    "mensual"
]

resultados_pruebas_filtros = []

for anio, usuario, granularidad in product(
    opciones_anio,
    opciones_usuario,
    opciones_granularidad
):

    indicadores, figura, serie = filtrar_demanda(
        anio,
        usuario,
        granularidad
    )

    # Verificación independiente de los resultados.

    if anio == "todos":

        datos_referencia = df

    else:

        datos_referencia = df.loc[
            df["dteday"].dt.year == int(anio)
        ]

    total_esperado = int(
        datos_referencia[usuario].sum()
    )

    dias_esperados = len(datos_referencia)

    promedio_esperado = (
        datos_referencia[usuario].mean()
    )

    if granularidad == "diaria":

        puntos_esperados = dias_esperados

    else:

        puntos_esperados = (
            datos_referencia["dteday"]
            .dt.to_period("M")
            .nunique()
        )

    assert indicadores[
        "Alquileres"
    ] == total_esperado

    assert indicadores[
        "Dias_observados"
    ] == dias_esperados

    assert np.isclose(
        indicadores["Promedio_diario"],
        promedio_esperado
    )

    assert len(serie) == puntos_esperados

    assert int(
        serie["Alquileres"].sum()
    ) == total_esperado

    assert len(figura.data) > 0

    resultados_pruebas_filtros.append({
        "Año": anio,
        "Usuario": usuario,
        "Granularidad": granularidad,
        "Alquileres": indicadores["Alquileres"],
        "Promedio_diario": indicadores[
            "Promedio_diario"
        ],
        "Dias": indicadores["Dias_observados"],
        "Puntos_grafica": len(serie),
        "Estado": "OK"
    })

df_pruebas_filtros = pd.DataFrame(
    resultados_pruebas_filtros
)

# ==========================================================
# 10. PRUEBAS DE NAVEGACIÓN
# ==========================================================

resultados_pruebas_navegacion = []

for pestana in vistas_dashboard:

    vista = seleccionar_vista(pestana)

    componentes = list(
        recorrer_componentes(vista)
    )

    cantidad_graficas = sum(
        isinstance(componente, dcc.Graph)
        for componente in componentes
    )

    cantidad_esperada = (
        df_inventario_vistas.loc[
            df_inventario_vistas["Vista"]
            == pestana,
            "Graficas"
        ].iloc[0]
    )

    assert cantidad_graficas == cantidad_esperada

    resultados_pruebas_navegacion.append({
        "Pestana": pestana,
        "Graficas_esperadas": cantidad_esperada,
        "Graficas_recuperadas": cantidad_graficas,
        "Estado": "OK"
    })

df_pruebas_navegacion = pd.DataFrame(
    resultados_pruebas_navegacion
)

# ==========================================================
# 11. VERIFICAR REGISTRO DE CALLBACKS
# ==========================================================

callbacks_registrados = list(
    app.callback_map.keys()
)

assert len(callbacks_registrados) == 2

assert len(df_pruebas_filtros) == 18

assert len(df_pruebas_navegacion) == 5

assert (
    df_pruebas_filtros["Estado"] == "OK"
).all()

assert (
    df_pruebas_navegacion["Estado"] == "OK"
).all()

# ==========================================================
# 12. VALIDAR RESPUESTAS DE LOS CALLBACKS
# ==========================================================

# Ejecutar directamente las funciones para comprobar
# que devuelven los componentes esperados.

figura_prueba, tarjetas_prueba = actualizar_demanda(
    "todos",
    "cnt",
    "mensual"
)

assert len(figura_prueba.data) > 0

assert isinstance(
    tarjetas_prueba,
    dbc.Row
)

vista_prueba = actualizar_pestana("fase3")

assert isinstance(
    vista_prueba,
    html.Div
)

# ==========================================================
# 13. EXPORTAR EVIDENCIAS DE VALIDACIÓN
# ==========================================================

CARPETA_VALIDACIONES = (
    RESULTADOS / "Validaciones_Dashboard"
)

CARPETA_VALIDACIONES.mkdir(
    parents=True,
    exist_ok=True
)

df_pruebas_filtros.to_csv(
    CARPETA_VALIDACIONES /
    "pruebas_filtros.csv",

    index=False,
    encoding="utf-8-sig"
)

df_pruebas_navegacion.to_csv(
    CARPETA_VALIDACIONES /
    "pruebas_navegacion.csv",

    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 14. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("DASHBOARD GLOBAL - CALLBACKS E INTERACTIVIDAD")
print("=" * 60)

print("\n=== CALLBACKS REGISTRADOS ===")

for numero, callback in enumerate(
    callbacks_registrados,
    start=1
):

    print(f"{numero}. {callback}")

print("\n=== PRUEBAS DE FILTROS ===")

print(
    df_pruebas_filtros.round(2)
    .to_string(index=False)
)

print("\n=== PRUEBAS DE NAVEGACIÓN ===")

print(
    df_pruebas_navegacion.to_string(
        index=False
    )
)

print("\n=== VALIDACIONES ===")

print("Registro de callbacks: OK")
print("Filtrado por año: OK")
print("Filtrado por tipo de usuario: OK")
print("Granularidad diaria: OK")
print("Granularidad mensual: OK")
print("Indicadores dinámicos: OK")
print("Conservación de totales: OK")
print("Navegación entre pestañas: OK")
print("Exportación de evidencias: OK")

print("\n=== RESUMEN ===")

print(
    "Callbacks registrados:",
    len(callbacks_registrados)
)

print(
    "Pruebas de filtros superadas:",
    len(df_pruebas_filtros),
    "/ 18"
)

print(
    "Pruebas de navegación superadas:",
    len(df_pruebas_navegacion),
    "/ 5"
)

print(
    "Total de pruebas funcionales:",
    len(df_pruebas_filtros)
    + len(df_pruebas_navegacion)
)

print("\nServidor Dash: pendiente de ejecución")

print(
    "\nCallbacks e interactividad "
    "implementados correctamente."
)