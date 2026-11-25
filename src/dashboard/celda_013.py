# ==========================================================
# DASHBOARD GLOBAL - CELDA 13
# FASE 4: Consolidación y visualizaciones interactivas
# ==========================================================

import hashlib
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 1. VALIDAR IDENTIDAD DEL DATASET
# ==========================================================

hash_actual_f4 = hashlib.sha256(
    RUTA_CSV.read_bytes()
).hexdigest()

hash_original_f4 = metadatos_f4[
    "identificacion_dataset"
]["sha256"]

assert hash_actual_f4 == hash_original_f4, (
    "El dataset no coincide con el utilizado en Fase 4."
)

print("Identidad del dataset: OK")

# ==========================================================
# 2. CONSOLIDAR INDICADORES PRINCIPALES
# ==========================================================

indicadores_preparacion_f4 = (
    df_preparacion_f4
    .set_index("Indicador")["Resultado"]
    .to_dict()
)

regresion_test_f4 = (
    df_regresion_f4.loc[
        df_regresion_f4["Conjunto"] == "Prueba"
    ]
    .set_index("Modelo")
)

clasificacion_test_f4 = (
    df_clasificacion_f4.loc[
        df_clasificacion_f4["Conjunto"] == "Prueba"
    ]
    .set_index("Modelo")
)

rmse_lineal_f4 = regresion_test_f4.loc[
    "Regresión Lineal Simple", "RMSE"
]

rmse_dummy_f4 = regresion_test_f4.loc[
    "Dummy Regressor", "RMSE"
]

accuracy_logistica_f4 = clasificacion_test_f4.loc[
    "Regresión Logística", "Accuracy"
]

accuracy_dummy_f4 = clasificacion_test_f4.loc[
    "Dummy Classifier", "Accuracy"
]

auc_logistica_f4 = clasificacion_test_f4.loc[
    "Regresión Logística", "AUC_ROC"
]

mejora_rmse_f4 = (
    1 - rmse_lineal_f4 / rmse_dummy_f4
) * 100

mejora_accuracy_f4 = (
    accuracy_logistica_f4 - accuracy_dummy_f4
) * 100

mejora_f1_macro_f4 = (
    clasificacion_test_f4.loc[
        "Regresión Logística", "F1_Macro"
    ]
    -
    clasificacion_test_f4.loc[
        "Dummy Classifier", "F1_Macro"
    ]
) * 100

# ==========================================================
# 3. CUMPLIMIENTO DE REQUERIMIENTOS
# ==========================================================

df_estados_f4 = (
    df_cumplimiento_f4["Estado"]
    .value_counts()
    .rename_axis("Estado")
    .reset_index(name="Cantidad")
)

cumplidos_f4 = int(
    (df_cumplimiento_f4["Estado"] == "Cumplido").sum()
)

no_aplica_f4 = int(
    (df_cumplimiento_f4["Estado"] == "No aplica").sum()
)

total_requerimientos_f4 = len(df_cumplimiento_f4)

aplicables_f4 = (
    total_requerimientos_f4 - no_aplica_f4
)

cumplimiento_pct_f4 = (
    cumplidos_f4 / aplicables_f4 * 100
)

# ==========================================================
# 4. CONFIGURAR VISUALIZACIONES
# ==========================================================

figuras_fase4 = {}

orden_conjuntos_f4 = [
    "Entrenamiento",
    "Validación",
    "Prueba"
]

colores_modelos_f4 = {
    "Regresión Lineal Simple": COLORES["principal"],
    "Regresión Logística": COLORES["principal"],
    "Dummy Regressor": "#94A3B8",
    "Dummy Classifier": "#94A3B8"
}

# ==========================================================
# 5. BASELINE DE REGRESIÓN
# ==========================================================

# 5.1 Comparación de MAE y RMSE.

df_regresion_largo_f4 = df_regresion_f4.melt(
    id_vars=["Modelo", "Conjunto"],
    value_vars=["MAE", "RMSE"],
    var_name="Metrica",
    value_name="Valor"
)

figuras_fase4["regresion_errores"] = px.bar(
    df_regresion_largo_f4,
    x="Conjunto",
    y="Valor",
    color="Modelo",
    facet_col="Metrica",
    barmode="group",
    text_auto=".1f",
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_map=colores_modelos_f4,
    title="Baseline de regresión: MAE y RMSE"
)

# 5.2 Comparación de R².

figuras_fase4["regresion_r2"] = px.bar(
    df_regresion_f4,
    x="Conjunto",
    y="R2",
    color="Modelo",
    barmode="group",
    text_auto=".3f",
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_map=colores_modelos_f4,
    title="Baseline de regresión: coeficiente R²"
)

figuras_fase4["regresion_r2"].add_hline(
    y=0,
    line_dash="dash",
    line_color=COLORES["negativo"]
)

# ==========================================================
# 6. BASELINE DE CLASIFICACIÓN
# ==========================================================

# 6.1 Comparación de métricas en prueba.

metricas_clasificacion_f4 = [
    "Accuracy",
    "Balanced_Accuracy",
    "Precision",
    "Recall",
    "F1",
    "F1_Macro",
    "AUC_ROC"
]

df_clasificacion_largo_f4 = (
    df_resumen_clasificacion_f4.melt(
        id_vars="Modelo",
        value_vars=metricas_clasificacion_f4,
        var_name="Metrica",
        value_name="Valor"
    )
)

figuras_fase4["clasificacion_prueba"] = px.bar(
    df_clasificacion_largo_f4,
    x="Metrica",
    y="Valor",
    color="Modelo",
    barmode="group",
    text_auto=".3f",
    range_y=[0, 1.12],
    color_discrete_map=colores_modelos_f4,
    title="Baseline de clasificación: métricas en prueba"
)

# 6.2 Accuracy por conjunto.

figuras_fase4["clasificacion_accuracy"] = px.bar(
    df_clasificacion_f4,
    x="Conjunto",
    y="Accuracy",
    color="Modelo",
    barmode="group",
    text_auto=".1%",
    range_y=[0, 1.12],
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_map=colores_modelos_f4,
    title="Accuracy por conjunto de evaluación"
)

figuras_fase4[
    "clasificacion_accuracy"
].update_yaxes(tickformat=".0%")

# 6.3 F1 Macro por conjunto.

figuras_fase4["clasificacion_f1_macro"] = px.bar(
    df_clasificacion_f4,
    x="Conjunto",
    y="F1_Macro",
    color="Modelo",
    barmode="group",
    text_auto=".3f",
    range_y=[0, 1.12],
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_map=colores_modelos_f4,
    title="F1 Macro por conjunto de evaluación"
)

# 6.4 AUC-ROC por conjunto.

figuras_fase4["clasificacion_auc"] = px.bar(
    df_clasificacion_f4,
    x="Conjunto",
    y="AUC_ROC",
    color="Modelo",
    barmode="group",
    text_auto=".3f",
    range_y=[0, 1.12],
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_map=colores_modelos_f4,
    title="AUC-ROC por conjunto de evaluación"
)

figuras_fase4["clasificacion_auc"].add_hline(
    y=0.5,
    line_dash="dash",
    annotation_text="Referencia aleatoria"
)

# ==========================================================
# 7. PREPARACIÓN Y CALIDAD DE DATOS
# ==========================================================

# 7.1 Completitud de los datos.

total_celdas_f4 = (
    indicadores_preparacion_f4["Registros originales"]
    *
    indicadores_preparacion_f4["Variables originales"]
)

faltantes_f4 = indicadores_preparacion_f4[
    "Valores faltantes"
]

completitud_f4 = (
    1 - faltantes_f4 / total_celdas_f4
) * 100

figuras_fase4["completitud"] = go.Figure(
    go.Indicator(
        mode="number+gauge",
        value=completitud_f4,
        number={
            "suffix": "%",
            "valueformat": ".1f"
        },
        title={
            "text": "Completitud del dataset"
        },
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {
                "color": COLORES["secundario"]
            }
        }
    )
)

# 7.2 Outliers detectados por variable.

df_conteo_outliers_f4 = (
    df_outliers_f4["Variable_atipica"]
    .value_counts()
    .rename_axis("Variable")
    .reset_index(name="Outliers")
)

df_conteo_outliers_f4["Porcentaje"] = (
    df_conteo_outliers_f4["Outliers"]
    / len(df) * 100
)

figuras_fase4["outliers"] = px.bar(
    df_conteo_outliers_f4,
    x="Variable",
    y="Outliers",
    color="Variable",
    text_auto=True,
    hover_data=["Porcentaje"],
    title="Valores atípicos detectados mediante IQR"
)

figuras_fase4["outliers"].update_layout(
    showlegend=False
)

# 7.3 Valores modificados mediante winsorization.

figuras_fase4["winsorization"] = px.bar(
    df_winsorization_f4,
    x="Conjunto",
    y="Valores_modificados",
    color="Variable",
    facet_col="Problema",
    barmode="group",
    text_auto=True,
    hover_data=["Porcentaje", "Registros"],
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    title="Valores modificados mediante winsorization"
)

# ==========================================================
# 8. INGENIERÍA DE CARACTERÍSTICAS
# ==========================================================

# 8.1 Composición de las características finales.

df_caracteristicas_f4 = pd.DataFrame({
    "Tipo": [
        "Variables numéricas estandarizadas",
        "Columnas One-Hot Encoding"
    ],
    "Cantidad": [
        indicadores_preparacion_f4[
            "Variables numéricas estandarizadas"
        ],
        indicadores_preparacion_f4[
            "Columnas One-Hot Encoding"
        ]
    ]
})

figuras_fase4["caracteristicas"] = px.pie(
    df_caracteristicas_f4,
    names="Tipo",
    values="Cantidad",
    hole=0.55,
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ],
    title="Composición de las características predictoras"
)

figuras_fase4["caracteristicas"].update_traces(
    textinfo="label+value"
)

figuras_fase4["caracteristicas"].add_annotation(
    text="29<br>Características",
    x=0.5,
    y=0.5,
    showarrow=False,
    font_size=17
)

# 8.2 Verificación de StandardScaler.

df_scaler_grafico_f4 = (
    df_estandarizacion_f4.melt(
        id_vars=["Problema", "Variable"],
        value_vars=[
            "Media_transformada",
            "Desviacion_transformada"
        ],
        var_name="Estadistico",
        value_name="Valor"
    )
)

figuras_fase4["estandarizacion"] = px.scatter(
    df_scaler_grafico_f4,
    x="Variable",
    y="Valor",
    color="Estadistico",
    facet_col="Problema",
    title="Verificación de StandardScaler en entrenamiento"
)

figuras_fase4["estandarizacion"].update_traces(
    marker_size=10
)

figuras_fase4["estandarizacion"].update_xaxes(
    tickangle=-45
)

figuras_fase4["estandarizacion"].add_hline(
    y=0,
    line_dash="dot",
    line_color="#94A3B8"
)

figuras_fase4["estandarizacion"].add_hline(
    y=1,
    line_dash="dot",
    line_color="#94A3B8"
)

# ==========================================================
# 9. PARTICIONES DEL DATASET
# ==========================================================

figuras_fase4["particiones"] = px.bar(
    df_matrices_f4,
    x="Problema",
    y="Registros",
    color="Conjunto",
    barmode="stack",
    text_auto=True,
    category_orders={
        "Conjunto": orden_conjuntos_f4
    },
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"],
        COLORES["acento"]
    ],
    title="Particiones de regresión y clasificación",
    hover_data=[
        "Caracteristicas",
        "Valores_faltantes"
    ]
)

# ==========================================================
# 10. CUMPLIMIENTO DE REQUERIMIENTOS
# ==========================================================

figuras_fase4["cumplimiento"] = px.pie(
    df_estados_f4,
    names="Estado",
    values="Cantidad",
    hole=0.55,
    color="Estado",
    color_discrete_map={
        "Cumplido": "#16A34A",
        "No aplica": "#94A3B8"
    },
    title="Cumplimiento de requerimientos técnicos"
)

figuras_fase4["cumplimiento"].update_traces(
    textinfo="label+value"
)

figuras_fase4["cumplimiento"].add_annotation(
    text=f"{cumplimiento_pct_f4:.0f}%<br>Aplicables",
    x=0.5,
    y=0.5,
    showarrow=False,
    font_size=17
)

# ==========================================================
# 11. ESTILO VISUAL UNIFICADO
# ==========================================================

for nombre, figura in figuras_fase4.items():

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
            l=45, r=35, t=70, b=90
        ),
        height=450
    )

# ==========================================================
# 12. CONSOLIDAR INDICADORES DE FASE 4
# ==========================================================

df_indicadores_f4 = pd.DataFrame({
    "Indicador": [
        "Completitud del dataset (%)",
        "Características predictoras",
        "Variables derivadas",
        "RMSE regresión lineal en prueba",
        "RMSE Dummy Regressor en prueba",
        "Reducción relativa RMSE (%)",
        "Accuracy regresión logística",
        "AUC-ROC regresión logística",
        "Mejora Accuracy (pp)",
        "Mejora F1 Macro (pp)",
        "Requerimientos cumplidos",
        "Requerimientos no aplicables",
        "Cumplimiento aplicable (%)"
    ],
    "Valor": [
        completitud_f4,
        indicadores_preparacion_f4[
            "Características predictoras finales"
        ],
        indicadores_preparacion_f4[
            "Variables derivadas"
        ],
        rmse_lineal_f4,
        rmse_dummy_f4,
        mejora_rmse_f4,
        accuracy_logistica_f4,
        auc_logistica_f4,
        mejora_accuracy_f4,
        mejora_f1_macro_f4,
        cumplidos_f4,
        no_aplica_f4,
        cumplimiento_pct_f4
    ]
})

# ==========================================================
# 13. EXPORTAR TABLAS Y GRÁFICAS
# ==========================================================

tablas_consolidadas_f4 = {
    "indicadores_fase4": df_indicadores_f4,
    "conteo_outliers": df_conteo_outliers_f4,
    "composicion_caracteristicas": df_caracteristicas_f4,
    "resumen_cumplimiento": df_estados_f4
}

for nombre, tabla in tablas_consolidadas_f4.items():

    tabla.to_csv(
        FASE4 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

CARPETA_GRAFICAS_F4 = FASE4 / "graficas"

CARPETA_GRAFICAS_F4.mkdir(
    parents=True,
    exist_ok=True
)

for nombre, figura in figuras_fase4.items():

    figura.write_html(
        str(CARPETA_GRAFICAS_F4 / f"{nombre}.html"),
        include_plotlyjs=True
    )

    figura.write_json(
        str(CARPETA_GRAFICAS_F4 / f"{nombre}.json")
    )

# ==========================================================
# 14. VALIDACIONES DE INTEGRIDAD
# ==========================================================

assert len(df_regresion_f4) == 6
assert len(df_clasificacion_f4) == 6

assert np.isclose(
    rmse_lineal_f4, 2568.032012
)

assert np.isclose(
    accuracy_logistica_f4, 0.90
)

assert np.isclose(
    auc_logistica_f4, 0.975140,
    atol=0.000001
)

assert np.isclose(
    mejora_rmse_f4, 4.150970,
    atol=0.0001
)

assert np.isclose(
    mejora_accuracy_f4, 28.181818,
    atol=0.0001
)

assert np.isclose(
    mejora_f1_macro_f4, 51.156648,
    atol=0.0001
)

assert completitud_f4 == 100

assert df_caracteristicas_f4[
    "Cantidad"
].sum() == 29

assert (
    df_matrices_f4["Caracteristicas"] == 29
).all()

assert (
    df_matrices_f4["Valores_faltantes"] == 0
).all()

assert (
    df_matrices_f4.groupby("Problema")[
        "Registros"
    ].sum() == 731
).all()

assert np.allclose(
    df_estandarizacion_f4["Media_transformada"],
    0,
    atol=1e-10
)

assert np.allclose(
    df_estandarizacion_f4[
        "Desviacion_transformada"
    ],
    1,
    atol=1e-10
)

assert cumplidos_f4 == 12
assert no_aplica_f4 == 1
assert cumplimiento_pct_f4 == 100

assert len(figuras_fase4) == 13

assert all(
    (CARPETA_GRAFICAS_F4 / f"{nombre}.html").exists()
    and
    (CARPETA_GRAFICAS_F4 / f"{nombre}.json").exists()
    for nombre in figuras_fase4
)

# ==========================================================
# 15. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 4 - CONSOLIDACIÓN Y VISUALIZACIONES")
print("=" * 60)

print("\n=== INDICADORES PRINCIPALES ===")

print(
    df_indicadores_f4.round(6).to_string(
        index=False
    )
)

print("\n=== OUTLIERS POR VARIABLE ===")

print(
    df_conteo_outliers_f4.round(4).to_string(
        index=False
    )
)

print("\n=== CARACTERÍSTICAS PREDICTORAS ===")

print(
    df_caracteristicas_f4.to_string(
        index=False
    )
)

print("\n=== DIMENSIONES DE MATRICES FINALES ===")

print(
    df_matrices_f4.to_string(index=False)
)

print("\n=== CUMPLIMIENTO ===")

print(
    df_estados_f4.to_string(index=False)
)

print("\n=== GRÁFICAS INTERACTIVAS ===")

for nombre in figuras_fase4:
    print(f"{nombre}: OK")

print("\n=== VALIDACIONES ===")

print("Identidad del dataset: OK")
print("Integridad de métricas originales: OK")
print("Composición de características: OK")
print("Particiones del dataset: OK")
print("Verificación de StandardScaler: OK")
print("Cumplimiento de requerimientos: OK")
print("Modelos reentrenados: 0")

print(
    "Tablas consolidadas nuevas:",
    len(tablas_consolidadas_f4)
)

print(
    "Gráficas interactivas:",
    len(figuras_fase4)
)

print(
    "Imágenes originales conservadas:",
    len(df_imagenes_f4)
)

print(
    "\nFase 4 - Consolidación finalizada correctamente."
)