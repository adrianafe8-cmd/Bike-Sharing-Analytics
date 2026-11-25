# ==========================================================
# DASHBOARD GLOBAL - CELDA 14
# Integración del resumen ejecutivo
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 1. CONFIGURAR DIRECTORIOS
# ==========================================================

RESUMEN = RESULTADOS / "Resumen_Ejecutivo"

RESUMEN.mkdir(
    parents=True,
    exist_ok=True
)

CARPETA_GRAFICAS_RESUMEN = RESUMEN / "graficas"

CARPETA_GRAFICAS_RESUMEN.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# 2. INVENTARIO GLOBAL DE LAS CUATRO FASES
# ==========================================================

inventario_fases = pd.DataFrame({
    "Fase": [
        "Fase 1",
        "Fase 2",
        "Fase 3",
        "Fase 4"
    ],
    "Componente": [
        "Análisis exploratorio de datos",
        "Regresión simple y múltiple",
        "Modelado avanzado",
        "Preprocesamiento y baseline"
    ],
    "Graficas_interactivas": [
        len(figuras_fase1),
        len(figuras_fase2),
        len(figuras_fase3),
        len(figuras_fase4)
    ],
    "Imagenes_originales": [
        0,
        len(df_imagenes_f2),
        len(df_imagenes_f3),
        len(df_imagenes_f4)
    ],
    "Procedencia": [
        "EDA reconstruido desde el dataset",
        "Notebook original",
        "Notebook original",
        "Archivos CSV originales"
    ],
    "Estado": [
        "Consolidado",
        "Consolidado",
        "Consolidado",
        "Consolidado"
    ]
})

total_graficas_fases = int(
    inventario_fases[
        "Graficas_interactivas"
    ].sum()
)

total_imagenes_fases = int(
    inventario_fases[
        "Imagenes_originales"
    ].sum()
)

# ==========================================================
# 3. CONSOLIDAR MÉTRICAS DE REGRESIÓN
# ==========================================================

# Las métricas se recuperan de las tablas originales.
# Se conservan las diferencias metodológicas entre fases.

regresion_global_f2 = (
    df_evaluacion_f2.loc[
        df_evaluacion_f2["Conjunto"] == "Prueba",
        ["MAE", "RMSE", "R2"]
    ].copy()
)

regresion_global_f2["Modelo"] = (
    modelo_seleccionado_f2
)

regresion_global_f2["Fase"] = "Fase 2"

regresion_global_f3 = (
    df_regresion_f3.loc[
        df_regresion_f3["Conjunto"] == "Prueba",
        ["Modelo", "MAE", "RMSE", "R2"]
    ].copy()
)

regresion_global_f3["Fase"] = "Fase 3"

regresion_global_f4 = (
    df_regresion_f4.loc[
        df_regresion_f4["Conjunto"] == "Prueba",
        ["Modelo", "MAE", "RMSE", "R2"]
    ].copy()
)

regresion_global_f4["Fase"] = "Fase 4"

df_regresion_global = pd.concat(
    [
        regresion_global_f2,
        regresion_global_f3,
        regresion_global_f4
    ],
    ignore_index=True
)

df_regresion_global = df_regresion_global[
    ["Fase", "Modelo", "MAE", "RMSE", "R2"]
]

df_regresion_global["Etiqueta"] = (
    df_regresion_global["Fase"]
    + " | "
    + df_regresion_global["Modelo"]
)

df_regresion_global["Particion"] = (
    "Cronológica"
)

# ==========================================================
# 4. CONSOLIDAR MÉTRICAS DE CLASIFICACIÓN
# ==========================================================

columnas_clasificacion_global = [
    "Modelo",
    "Accuracy",
    "Precision",
    "Recall",
    "F1",
    "AUC_ROC"
]

clasificacion_global_f3 = (
    df_clasificacion_test_f3[
        columnas_clasificacion_global
    ].copy()
)

clasificacion_global_f3["Fase"] = "Fase 3"

clasificacion_global_f3["Particion"] = (
    "Cronológica"
)

clasificacion_global_f4 = (
    df_clasificacion_f4.loc[
        df_clasificacion_f4["Conjunto"] == "Prueba",
        columnas_clasificacion_global
    ].copy()
)

clasificacion_global_f4["Fase"] = "Fase 4"

clasificacion_global_f4["Particion"] = (
    "Aleatoria estratificada"
)

df_clasificacion_global = pd.concat(
    [
        clasificacion_global_f3,
        clasificacion_global_f4
    ],
    ignore_index=True
)

df_clasificacion_global = df_clasificacion_global[
    [
        "Fase",
        "Modelo",
        "Particion",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "AUC_ROC"
    ]
]

# No se establece un ranking global de clasificación
# porque los conjuntos de evaluación son diferentes.

# ==========================================================
# 5. INDICADORES EJECUTIVOS
# ==========================================================

df_indicadores_ejecutivos = pd.DataFrame([
    {
        "Indicador": "Total de alquileres",
        "Valor": total_alquileres,
        "Unidad": "Alquileres",
        "Fuente": "Dataset original"
    },
    {
        "Indicador": "Promedio diario",
        "Valor": promedio_diario,
        "Unidad": "Alquileres/día",
        "Fuente": "Dataset original"
    },
    {
        "Indicador": "Crecimiento anual",
        "Valor": crecimiento_anual,
        "Unidad": "%",
        "Fuente": "Dataset original"
    },
    {
        "Indicador": "Completitud",
        "Valor": porcentaje_completitud,
        "Unidad": "%",
        "Fuente": "Fase 1"
    },
    {
        "Indicador": "Reducción MAE regresión múltiple",
        "Valor": mejora_mae_f2,
        "Unidad": "%",
        "Fuente": "Fase 2 - Validación"
    },
    {
        "Indicador": "R2 regresión múltiple",
        "Valor": metricas_test_f2["R2"],
        "Unidad": "Coeficiente",
        "Fuente": "Fase 2 - Prueba"
    },
    {
        "Indicador": "Silueta K-Means",
        "Valor": df_clustering_f3.loc[
            df_clustering_f3["Algoritmo"] == "K-Means",
            "Silueta"
        ].iloc[0],
        "Unidad": "Coeficiente",
        "Fuente": "Fase 3"
    },
    {
        "Indicador": "Accuracy regresión logística",
        "Valor": accuracy_logistica_f4 * 100,
        "Unidad": "%",
        "Fuente": "Fase 4 - Prueba estratificada"
    },
    {
        "Indicador": "AUC-ROC regresión logística",
        "Valor": auc_logistica_f4,
        "Unidad": "Coeficiente",
        "Fuente": "Fase 4 - Prueba estratificada"
    },
    {
        "Indicador": "Características predictoras",
        "Valor": indicadores_preparacion_f4[
            "Características predictoras finales"
        ],
        "Unidad": "Características",
        "Fuente": "Fase 4"
    },
    {
        "Indicador": "Cumplimiento aplicable",
        "Valor": cumplimiento_pct_f4,
        "Unidad": "%",
        "Fuente": "Fase 4 - Verificación interna"
    }
])

# ==========================================================
# 6. VISUALIZACIONES DEL RESUMEN EJECUTIVO
# ==========================================================

figuras_resumen = {}

# 6.1 Evolución mensual de alquileres.

df_mensual_ejecutivo = demanda_mensual.copy()

df_mensual_ejecutivo["Año"] = (
    df_mensual_ejecutivo["Mes"].dt.year.astype(str)
)

df_mensual_ejecutivo["Numero_mes"] = (
    df_mensual_ejecutivo["Mes"].dt.month
)

nombres_meses = {
    1: "Ene", 2: "Feb", 3: "Mar",
    4: "Abr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Sep",
    10: "Oct", 11: "Nov", 12: "Dic"
}

df_mensual_ejecutivo["Nombre_mes"] = (
    df_mensual_ejecutivo["Numero_mes"]
    .map(nombres_meses)
)

figuras_resumen["demanda_mensual"] = px.line(
    df_mensual_ejecutivo,
    x="Nombre_mes",
    y="Alquileres",
    color="Año",
    markers=True,
    category_orders={
        "Nombre_mes": list(nombres_meses.values())
    },
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ],
    title="Evolución mensual de la demanda"
)

figuras_resumen["demanda_mensual"].update_traces(
    line_width=3,
    marker_size=7
)

# 6.2 Demanda anual.

figuras_resumen["demanda_anual"] = px.bar(
    demanda_anual.assign(
        Año=demanda_anual["Año"].astype(str)
    ),
    x="Año",
    y="Alquileres",
    color="Año",
    text_auto=".3s",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ],
    title="Total de alquileres por año"
)

figuras_resumen["demanda_anual"].update_layout(
    showlegend=False
)

# 6.3 Participación por tipo de usuario.

df_usuarios_global = pd.DataFrame({
    "Tipo": ["Registrados", "Casuales"],
    "Alquileres": [
        total_registrados,
        total_casuales
    ]
})

figuras_resumen["tipo_usuario"] = px.pie(
    df_usuarios_global,
    names="Tipo",
    values="Alquileres",
    hole=0.60,
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ],
    title="Participación por tipo de usuario"
)

figuras_resumen["tipo_usuario"].update_traces(
    textinfo="label+percent"
)

# 6.4 Serie temporal diaria.

figuras_resumen["demanda_diaria"] = px.line(
    df,
    x="dteday",
    y="cnt",
    title="Serie temporal de alquileres diarios",
    labels={
        "dteday": "Fecha",
        "cnt": "Alquileres"
    }
)

figuras_resumen["demanda_diaria"].update_traces(
    line_color=COLORES["principal"],
    line_width=1.5
)

figuras_resumen["demanda_diaria"].update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=[
            dict(
                count=3,
                label="3 meses",
                step="month",
                stepmode="backward"
            ),
            dict(
                count=6,
                label="6 meses",
                step="month",
                stepmode="backward"
            ),
            dict(
                count=1,
                label="1 año",
                step="year",
                stepmode="backward"
            ),
            dict(
                step="all",
                label="Todo"
            )
        ]
    )
)

# 6.5 Comparación contextual de RMSE.

figuras_resumen["regresion_global_rmse"] = px.bar(
    df_regresion_global,
    x="RMSE",
    y="Etiqueta",
    color="Fase",
    orientation="h",
    text_auto=".2f",
    title="Regresión: RMSE en prueba por fase",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"],
        COLORES["acento"]
    ]
)

figuras_resumen[
    "regresion_global_rmse"
].update_yaxes(
    categoryorder="array",
    categoryarray=(
        df_regresion_global["Etiqueta"].tolist()[::-1]
    )
)

# 6.6 Comparación contextual de R2.

figuras_resumen["regresion_global_r2"] = px.bar(
    df_regresion_global,
    x="R2",
    y="Etiqueta",
    color="Fase",
    orientation="h",
    text_auto=".4f",
    title="Regresión: R² en prueba por fase",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"],
        COLORES["acento"]
    ]
)

figuras_resumen["regresion_global_r2"].add_vline(
    x=0,
    line_dash="dash",
    line_color=COLORES["negativo"]
)

# Advertencia metodológica en las comparaciones.

for nombre in [
    "regresion_global_rmse",
    "regresion_global_r2"
]:

    figuras_resumen[nombre].add_annotation(
        text=(
            "Comparación contextual: "
            "diferentes características y preprocesamientos."
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=-0.22,
        showarrow=False,
        font=dict(size=11),
        align="left"
    )

# 6.7 Clasificación separada por protocolo.

df_clasificacion_ejecutivo = (
    df_clasificacion_global.melt(
        id_vars=[
            "Fase",
            "Modelo",
            "Particion"
        ],
        value_vars=[
            "Accuracy",
            "F1",
            "AUC_ROC"
        ],
        var_name="Metrica",
        value_name="Valor"
    )
)

figuras_resumen["clasificacion_por_fase"] = px.bar(
    df_clasificacion_ejecutivo,
    x="Metrica",
    y="Valor",
    color="Modelo",
    facet_col="Fase",
    barmode="group",
    text_auto=".3f",
    range_y=[0, 1.12],
    hover_data=["Particion"],
    title="Clasificación por protocolo de evaluación"
)

figuras_resumen[
    "clasificacion_por_fase"
].add_annotation(
    text=(
        "Fase 3: cronológica. "
        "Fase 4: aleatoria estratificada. "
        "No son directamente comparables."
    ),
    xref="paper",
    yref="paper",
    x=0,
    y=-0.22,
    showarrow=False,
    font=dict(size=11),
    align="left"
)

# 6.8 Inventario de visualizaciones.

figuras_resumen["evidencias_por_fase"] = px.bar(
    inventario_fases,
    x="Fase",
    y=[
        "Graficas_interactivas",
        "Imagenes_originales"
    ],
    barmode="group",
    text_auto=True,
    title="Evidencias visuales por fase",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# ==========================================================
# 7. APLICAR ESTILO VISUAL
# ==========================================================

for nombre, figura in figuras_resumen.items():

    figura.update_layout(
        template="plotly_white",
        font=dict(
            family="Arial",
            size=12,
            color=COLORES["texto"]
        ),
        title_font_size=17,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            l=50,
            r=40,
            t=85,
            b=110
        ),
        height=450
    )

# ==========================================================
# 8. HALLAZGOS Y CONCLUSIONES GLOBALES
# ==========================================================

df_hallazgos_globales = pd.DataFrame([
    {
        "Fase": "Global",
        "Hallazgo": (
            f"La demanda aumentó {crecimiento_anual:.2f}% "
            "entre 2011 y 2012."
        ),
        "Implicacion": (
            "Considerar crecimiento y estacionalidad "
            "en la planificación de capacidad."
        )
    },
    {
        "Fase": "Fase 1",
        "Hallazgo": (
            "La temperatura y la sensación térmica "
            "presentan asociación positiva con la demanda."
        ),
        "Implicacion": (
            "Incorporar variables meteorológicas "
            "en los modelos predictivos."
        )
    },
    {
        "Fase": "Fase 2",
        "Hallazgo": (
            f"La regresión múltiple redujo el MAE "
            f"de validación en {mejora_mae_f2:.2f}%."
        ),
        "Implicacion": (
            "Las variables adicionales aportan "
            "capacidad predictiva frente al modelo simple."
        )
    },
    {
        "Fase": "Fase 3",
        "Hallazgo": (
            "Random Forest fue seleccionado en regresión "
            "por RMSE de validación y KNN en clasificación "
            "por F1 de validación temporal."
        ),
        "Implicacion": (
            "La selección debe respetar el protocolo "
            "de validación definido previamente."
        )
    },
    {
        "Fase": "Fase 3",
        "Hallazgo": (
            "Los coeficientes de silueta de ambos "
            "algoritmos de clustering son bajos."
        ),
        "Implicacion": (
            "No se evidencia una separación fuerte "
            "entre los grupos identificados."
        )
    },
    {
        "Fase": "Fase 4",
        "Hallazgo": (
            f"La regresión logística alcanzó "
            f"{accuracy_logistica_f4:.1%} de Accuracy "
            "en prueba estratificada."
        ),
        "Implicacion": (
            "El baseline supervisado supera al "
            "clasificador de referencia en este protocolo."
        )
    }
])

# ==========================================================
# 9. LIMITACIONES METODOLÓGICAS
# ==========================================================

df_limitaciones_globales = pd.DataFrame([
    {
        "Ambito": "Procedencia",
        "Limitacion": (
            "La Fase 1 fue reconstruida a partir "
            "del dataset original."
        )
    },
    {
        "Ambito": "Representatividad",
        "Limitacion": (
            "El dataset corresponde exclusivamente "
            "al periodo 2011-2012."
        )
    },
    {
        "Ambito": "Correlación",
        "Limitacion": (
            "Las asociaciones estadísticas no "
            "demuestran causalidad."
        )
    },
    {
        "Ambito": "Fuga de información",
        "Limitacion": (
            "casual y registered no deben utilizarse "
            "para predecir cnt, porque su suma define "
            "directamente la variable objetivo."
        )
    },
    {
        "Ambito": "Regresión",
        "Limitacion": (
            "Las fases utilizan diferentes características "
            "y estrategias de preprocesamiento."
        )
    },
    {
        "Ambito": "Regresión en R",
        "Limitacion": (
            "Se identificaron cinco coeficientes "
            "no estimables por singularidades."
        )
    },
    {
        "Ambito": "Clasificación temporal",
        "Limitacion": (
            "La validación externa de Fase 3 "
            "contiene exclusivamente demanda alta."
        )
    },
    {
        "Ambito": "Comparabilidad",
        "Limitacion": (
            "La clasificación de Fase 3 es cronológica "
            "y la de Fase 4 aleatoria estratificada."
        )
    },
    {
        "Ambito": "Umbral de clasificación",
        "Limitacion": (
            "El umbral de 3974 alquileres fue heredado "
            "de Fase 3. Existe posible solapamiento "
            "entre su conjunto de estimación y las "
            "particiones aleatorias de Fase 4."
        )
    },
    {
        "Ambito": "Generalización",
        "Limitacion": (
            "El desempeño de clasificación de Fase 4 "
            "no demuestra capacidad de predicción "
            "sobre periodos futuros."
        )
    },
    {
        "Ambito": "Evidencias",
        "Limitacion": (
            "Los modelos de las fases anteriores "
            "no fueron reentrenados en este dashboard."
        )
    }
])

# ==========================================================
# 10. EXPORTAR TABLAS CONSOLIDADAS
# ==========================================================

tablas_resumen = {
    "inventario_fases": inventario_fases,
    "indicadores_ejecutivos": df_indicadores_ejecutivos,
    "regresion_global": df_regresion_global,
    "clasificacion_global": df_clasificacion_global,
    "hallazgos_globales": df_hallazgos_globales,
    "limitaciones_globales": df_limitaciones_globales
}

for nombre, tabla in tablas_resumen.items():

    tabla.to_csv(
        RESUMEN / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

for nombre, figura in figuras_resumen.items():

    figura.write_html(
        str(
            CARPETA_GRAFICAS_RESUMEN /
            f"{nombre}.html"
        ),
        include_plotlyjs=True
    )

    figura.write_json(
        str(
            CARPETA_GRAFICAS_RESUMEN /
            f"{nombre}.json"
        )
    )

# ==========================================================
# 11. VALIDACIONES GLOBALES
# ==========================================================

assert len(inventario_fases) == 4

assert total_graficas_fases == 38

assert total_imagenes_fases == 25

assert len(df_regresion_global) == 5

assert len(df_clasificacion_global) == 4

assert (
    df_clasificacion_global["Particion"].nunique()
    == 2
)

assert total_alquileres == int(df["cnt"].sum())

assert (
    total_casuales + total_registrados
    == total_alquileres
)

assert np.isclose(
    porcentaje_casuales + porcentaje_registrados,
    100
)

assert len(figuras_resumen) == 8

assert all(
    (RESUMEN / f"{nombre}.csv").exists()
    for nombre in tablas_resumen
)

assert all(
    (
        CARPETA_GRAFICAS_RESUMEN /
        f"{nombre}.html"
    ).exists()
    and
    (
        CARPETA_GRAFICAS_RESUMEN /
        f"{nombre}.json"
    ).exists()
    for nombre in figuras_resumen
)

# ==========================================================
# 12. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("DASHBOARD GLOBAL - RESUMEN EJECUTIVO")
print("=" * 60)

print("\n=== INVENTARIO DE FASES ===")

print(
    inventario_fases.to_string(index=False)
)

print("\n=== INDICADORES EJECUTIVOS ===")

print(
    df_indicadores_ejecutivos.round(4)
    .to_string(index=False)
)

print("\n=== REGRESIÓN GLOBAL ===")

print(
    df_regresion_global[
        ["Fase", "Modelo", "MAE", "RMSE", "R2"]
    ].round(4).to_string(index=False)
)

print("\n=== CLASIFICACIÓN POR PROTOCOLO ===")

print(
    df_clasificacion_global.round(4)
    .to_string(index=False)
)

print("\n=== GRÁFICAS DEL RESUMEN EJECUTIVO ===")

for nombre in figuras_resumen:

    print(f"{nombre}: OK")

print("\n=== VALIDACIONES ===")

print("Integración de las cuatro fases: OK")
print("Integridad de indicadores: OK")
print("Trazabilidad de métricas: OK")
print("Separación de protocolos: OK")
print("Exportación de tablas y gráficas: OK")

print("\n=== INVENTARIO GLOBAL ===")

print("Fases consolidadas:", len(inventario_fases))

print(
    "Gráficas de las cuatro fases:",
    total_graficas_fases
)

print(
    "Gráficas del resumen ejecutivo:",
    len(figuras_resumen)
)

print(
    "Total de gráficas interactivas:",
    total_graficas_fases + len(figuras_resumen)
)

print(
    "Imágenes originales:",
    total_imagenes_fases
)

print("Hallazgos:", len(df_hallazgos_globales))

print(
    "Limitaciones documentadas:",
    len(df_limitaciones_globales)
)

print("Modelos reentrenados: 0")

print(
    "\nResumen ejecutivo consolidado correctamente."
)