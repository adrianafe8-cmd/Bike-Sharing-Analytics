# ==========================================================
# DASHBOARD GLOBAL - CELDA 11
# FASE 3: Consolidación y visualizaciones
# ==========================================================

import re

# ==========================================================
# 1. FUNCIONES PARA RECUPERAR RESULTADOS ORIGINALES
# ==========================================================

def recuperar_texto_f3(celda, salida=None):

    filtro = df_salidas_f3["Celda"] == celda

    if salida is not None:
        filtro &= df_salidas_f3["Salida"] == salida

    return "\n".join(
        df_salidas_f3.loc[filtro, "Resultado"].tolist()
    )


def extraer_tabla_f3(texto, modelos, columnas):

    # Extraer filas numéricas de las tablas originales.
    numero = r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)"

    patron = (
        r"(?m)^\s*\d+\s+("
        + "|".join(re.escape(m) for m in modelos)
        + r")"
        + (r"\s+" + numero) * (len(columnas) - 1)
        + r"\s*$"
    )

    coincidencias = re.findall(patron, texto)

    assert len(coincidencias) == len(modelos), (
        f"No se recuperaron todos los modelos: {modelos}"
    )

    tabla = pd.DataFrame(
        coincidencias,
        columns=columnas
    )

    for columna in columnas[1:]:
        tabla[columna] = pd.to_numeric(
            tabla[columna],
            errors="raise"
        )

    assert tabla[columnas[0]].is_unique

    return tabla


# ==========================================================
# 2. MÉTRICAS DE REGRESIÓN
# ==========================================================

# Resultados originales de validación: celda 13.

df_regresion_val_f3 = extraer_tabla_f3(
    recuperar_texto_f3(13, 1),
    ["Ridge", "Random Forest"],
    ["Modelo", "MAE", "RMSE", "R2"]
)

df_regresion_val_f3["Conjunto"] = "Validación"

# Resultados originales de prueba: celda 44.

df_regresion_test_f3 = extraer_tabla_f3(
    recuperar_texto_f3(44, 2),
    ["Ridge", "Random Forest"],
    ["Modelo", "MAE", "RMSE", "R2"]
)

df_regresion_test_f3["Conjunto"] = "Prueba"

df_regresion_f3 = pd.concat(
    [
        df_regresion_val_f3,
        df_regresion_test_f3
    ],
    ignore_index=True
)

# Seleccionar exclusivamente según validación.

mejor_regresion_f3 = (
    df_regresion_val_f3.loc[
        df_regresion_val_f3["RMSE"].idxmin(),
        "Modelo"
    ]
)

# ==========================================================
# 3. MÉTRICAS DE CLASIFICACIÓN
# ==========================================================

df_clasificacion_test_f3 = extraer_tabla_f3(
    recuperar_texto_f3(44, 4),
    ["Random Forest", "KNN"],
    [
        "Modelo",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "AUC_ROC"
    ]
)

# Recuperar F1 promedio de validación temporal.

texto_knn_f3 = recuperar_texto_f3(22, 2)
texto_rf_f3 = recuperar_texto_f3(24, 2)

f1_knn_f3 = re.search(
    r"F1 promedio:\s*([\d.]+)",
    texto_knn_f3
)

f1_rf_f3 = re.search(
    r"F1 promedio:\s*([\d.]+)",
    texto_rf_f3
)

assert f1_knn_f3 is not None
assert f1_rf_f3 is not None

df_clasificacion_cv_f3 = pd.DataFrame({
    "Modelo": ["KNN", "Random Forest"],
    "F1_promedio": [
        float(f1_knn_f3.group(1)),
        float(f1_rf_f3.group(1))
    ]
})

mejor_clasificacion_f3 = (
    df_clasificacion_cv_f3.loc[
        df_clasificacion_cv_f3[
            "F1_promedio"
        ].idxmax(),
        "Modelo"
    ]
)

# ==========================================================
# 4. RESULTADOS DE CLUSTERING
# ==========================================================

df_clustering_f3 = extraer_tabla_f3(
    recuperar_texto_f3(44, 6),
    ["K-Means", "Agglomerative"],
    ["Algoritmo", "Clusters", "Silueta"]
)

df_clustering_f3["Clusters"] = (
    df_clustering_f3["Clusters"].astype(int)
)

texto_ari_f3 = recuperar_texto_f3(34, 3)

resultado_ari_f3 = re.search(
    r"ARI\):\s*([\d.]+)",
    texto_ari_f3
)

assert resultado_ari_f3 is not None

ari_f3 = float(resultado_ari_f3.group(1))

# ==========================================================
# 5. HIPERPARÁMETROS SELECCIONADOS
# ==========================================================

texto_config_f3 = recuperar_texto_f3(44, 7)

patrones_config_f3 = {
    "Ridge": r"Ridge alpha:\s*([^\n]+)",
    "Random Forest Regressor":
        r"Random Forest Regressor:\s*([^\n]+)",
    "KNN": r"KNN k:\s*([^\n]+)",
    "Random Forest Classifier":
        r"Random Forest Classifier:\s*([^\n]+)",
    "K-Means": r"K-Means K:\s*([^\n]+)"
}

nombres_parametros_f3 = {
    "Ridge": "alpha",
    "Random Forest Regressor":
        "n_estimators, max_depth, min_samples_leaf",
    "KNN": "n_neighbors",
    "Random Forest Classifier":
        "n_estimators, max_depth, min_samples_leaf",
    "K-Means": "n_clusters"
}

configuraciones_f3 = []

for modelo, patron in patrones_config_f3.items():

    resultado = re.search(
        patron,
        texto_config_f3
    )

    assert resultado is not None, (
        f"Configuración no encontrada: {modelo}"
    )

    configuraciones_f3.append({
        "Modelo": modelo,
        "Hiperparametros": nombres_parametros_f3[modelo],
        "Configuracion": resultado.group(1).strip()
    })

df_configuraciones_f3 = pd.DataFrame(
    configuraciones_f3
)

# ==========================================================
# 6. DISTRIBUCIÓN TEMPORAL DE CLASES
# ==========================================================

texto_clases_f3 = recuperar_texto_f3(16, 2)

filas_clases_f3 = re.findall(
    r"(Demanda baja|Demanda alta)"
    r"\s+(\d+)\s+(\d+)\s+(\d+)",
    texto_clases_f3
)

assert len(filas_clases_f3) == 2

df_clases_f3 = pd.DataFrame(
    filas_clases_f3,
    columns=[
        "Clase",
        "Entrenamiento",
        "Validación",
        "Prueba"
    ]
)

for columna in [
    "Entrenamiento",
    "Validación",
    "Prueba"
]:

    df_clases_f3[columna] = (
        df_clases_f3[columna].astype(int)
    )

df_clases_largo_f3 = df_clases_f3.melt(
    id_vars="Clase",
    var_name="Conjunto",
    value_name="Registros"
)

# Recuperar umbral original de clasificación.

texto_umbral_f3 = recuperar_texto_f3(16, 1)

resultado_umbral_f3 = re.search(
    r"Umbral de demanda:\s*([\d.]+)",
    texto_umbral_f3
)

assert resultado_umbral_f3 is not None

umbral_demanda_f3 = float(
    resultado_umbral_f3.group(1)
)

# ==========================================================
# 7. VALIDACIÓN CRUZADA TEMPORAL
# ==========================================================

texto_folds_f3 = recuperar_texto_f3(20, 1)

filas_folds_f3 = re.findall(
    r"(?m)^\s*\d+\s+(\d+)\s+(\d+)"
    r"\s+(\d+)\s+(\d+)\s*\\?\s*$",
    texto_folds_f3
)

estados_folds_f3 = re.findall(
    r"(?m)^\s*\d+\s+(\d+)"
    r"\s+(True|False)\s+(True|False)\s*$",
    texto_folds_f3
)

assert len(filas_folds_f3) == 5
assert len(estados_folds_f3) == 5

df_folds_f3 = pd.DataFrame(
    filas_folds_f3,
    columns=[
        "Fold",
        "N_entrenamiento",
        "N_validacion",
        "Clases_entrenamiento"
    ]
).astype(int)

df_folds_f3["Clases_validacion"] = [
    int(fila[0])
    for fila in estados_folds_f3
]

df_folds_f3["AUC_calculable"] = [
    fila[1] == "True"
    for fila in estados_folds_f3
]

df_folds_f3["Fold_utilizable"] = [
    fila[2] == "True"
    for fila in estados_folds_f3
]

folds_validos_f3 = int(
    df_folds_f3["Fold_utilizable"].sum()
)

# ==========================================================
# 8. VISUALIZACIONES INTERACTIVAS
# ==========================================================

figuras_fase3 = {}

# 8.1. Comparación de errores de regresión.

df_regresion_largo_f3 = df_regresion_f3.melt(
    id_vars=["Modelo", "Conjunto"],
    value_vars=["MAE", "RMSE"],
    var_name="Metrica",
    value_name="Valor"
)

figuras_fase3["regresion_errores"] = px.bar(
    df_regresion_largo_f3,
    x="Modelo",
    y="Valor",
    color="Metrica",
    facet_col="Conjunto",
    barmode="group",
    text_auto=".2f",
    title="Regresión avanzada: MAE y RMSE",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# 8.2. Comparación de R².

figuras_fase3["regresion_r2"] = px.bar(
    df_regresion_f3,
    x="Modelo",
    y="R2",
    color="Conjunto",
    barmode="group",
    text_auto=".4f",
    title="Regresión avanzada: coeficiente R²"
)

figuras_fase3["regresion_r2"].add_hline(
    y=0,
    line_dash="dash",
    line_color=COLORES["negativo"]
)

# 8.3. Clasificación en prueba.

df_clasificacion_largo_f3 = (
    df_clasificacion_test_f3.melt(
        id_vars="Modelo",
        var_name="Metrica",
        value_name="Valor"
    )
)

figuras_fase3["clasificacion_prueba"] = px.bar(
    df_clasificacion_largo_f3,
    x="Metrica",
    y="Valor",
    color="Modelo",
    barmode="group",
    text_auto=".3f",
    title="Clasificación: desempeño en prueba",
    range_y=[0, 1.12],
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# 8.4. Validación temporal de clasificadores.

figuras_fase3["clasificacion_cv"] = px.bar(
    df_clasificacion_cv_f3,
    x="Modelo",
    y="F1_promedio",
    color="Modelo",
    text_auto=".4f",
    range_y=[0, 1],
    title="F1 promedio en validación temporal"
)

figuras_fase3["clasificacion_cv"].update_layout(
    showlegend=False
)

# 8.5. Distribución temporal de clases.

figuras_fase3["distribucion_clases"] = px.bar(
    df_clases_largo_f3,
    x="Conjunto",
    y="Registros",
    color="Clase",
    barmode="stack",
    text_auto=True,
    title="Distribución temporal de la demanda",
    category_orders={
        "Conjunto": [
            "Entrenamiento",
            "Validación",
            "Prueba"
        ]
    },
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# 8.6. Comparación de algoritmos de clustering.

figuras_fase3["clustering_silueta"] = px.bar(
    df_clustering_f3,
    x="Algoritmo",
    y="Silueta",
    color="Algoritmo",
    text_auto=".4f",
    range_y=[0, 1],
    title="Clustering: coeficiente de silueta"
)

figuras_fase3["clustering_silueta"].update_layout(
    showlegend=False
)

# 8.7. Concordancia entre algoritmos.

figuras_fase3["clustering_ari"] = go.Figure(
    go.Indicator(
        mode="number+gauge",
        value=ari_f3,
        number={"valueformat": ".4f"},
        title={"text": "Índice Rand ajustado"},
        gauge={
            "axis": {"range": [-1, 1]},
            "bar": {
                "color": COLORES["principal"]
            }
        }
    )
)

# 8.8. Validación cruzada temporal.

df_folds_grafico_f3 = df_folds_f3.copy()

df_folds_grafico_f3["Estado"] = np.where(
    df_folds_grafico_f3["Fold_utilizable"],
    "Utilizable",
    "No utilizable"
)

figuras_fase3["validacion_temporal"] = px.bar(
    df_folds_grafico_f3,
    x="Fold",
    y="N_entrenamiento",
    color="Estado",
    text_auto=True,
    title="Particiones de validación temporal",
    hover_data=[
        "N_validacion",
        "Clases_entrenamiento",
        "Clases_validacion"
    ],
    color_discrete_map={
        "Utilizable": COLORES["secundario"],
        "No utilizable": COLORES["negativo"]
    }
)

figuras_fase3["validacion_temporal"].update_xaxes(
    dtick=1
)

# ==========================================================
# 9. APLICAR ESTILO VISUAL UNIFICADO
# ==========================================================

for nombre, figura in figuras_fase3.items():

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
        margin=dict(l=45, r=35, t=70, b=65),
        height=420
    )

# ==========================================================
# 10. GUARDAR TABLAS Y GRÁFICAS
# ==========================================================

df_indicadores_f3 = pd.DataFrame({
    "Indicador": [
        "Modelo regresión seleccionado en validación",
        "Clasificador seleccionado en validación temporal",
        "Umbral de demanda",
        "Folds totales",
        "Folds utilizables",
        "ARI"
    ],
    "Valor": [
        mejor_regresion_f3,
        mejor_clasificacion_f3,
        umbral_demanda_f3,
        len(df_folds_f3),
        folds_validos_f3,
        ari_f3
    ]
})

tablas_fase3 = {
    "metricas_regresion": df_regresion_f3,
    "metricas_clasificacion_prueba":
        df_clasificacion_test_f3,
    "metricas_clasificacion_cv":
        df_clasificacion_cv_f3,
    "metricas_clustering": df_clustering_f3,
    "hiperparametros": df_configuraciones_f3,
    "distribucion_clases": df_clases_f3,
    "validacion_temporal": df_folds_f3,
    "indicadores_fase3": df_indicadores_f3
}

for nombre, tabla in tablas_fase3.items():

    tabla.to_csv(
        FASE3 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

CARPETA_GRAFICAS_F3 = FASE3 / "graficas"

CARPETA_GRAFICAS_F3.mkdir(
    parents=True,
    exist_ok=True
)

for nombre, figura in figuras_fase3.items():

    figura.write_html(
        str(CARPETA_GRAFICAS_F3 / f"{nombre}.html"),
        include_plotlyjs=True
    )

    figura.write_json(
        str(CARPETA_GRAFICAS_F3 / f"{nombre}.json")
    )

# ==========================================================
# 11. VALIDACIONES DE INTEGRIDAD
# ==========================================================

assert mejor_regresion_f3 == "Random Forest"
assert mejor_clasificacion_f3 == "KNN"

assert len(df_regresion_f3) == 4
assert len(df_clasificacion_test_f3) == 2
assert len(df_clustering_f3) == 2

assert np.isclose(umbral_demanda_f3, 3974)
assert np.isclose(ari_f3, 0.4276)

assert folds_validos_f3 == 4

assert df_clases_f3[
    ["Entrenamiento", "Validación", "Prueba"]
].sum().tolist() == [511, 109, 111]

assert df_clases_f3["Validación"].tolist() == [
    0, 109
]

assert np.isclose(
    df_regresion_test_f3.set_index(
        "Modelo"
    ).loc["Ridge", "R2"],
    0.6215
)

assert np.isclose(
    df_clasificacion_test_f3.set_index(
        "Modelo"
    ).loc["Random Forest", "AUC_ROC"],
    0.9011
)

assert len(figuras_fase3) == 8

assert all(
    (CARPETA_GRAFICAS_F3 / f"{nombre}.html").exists()
    and
    (CARPETA_GRAFICAS_F3 / f"{nombre}.json").exists()
    for nombre in figuras_fase3
)

# ==========================================================
# 12. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 3 - CONSOLIDACIÓN Y VISUALIZACIONES")
print("=" * 60)

print("\n=== REGRESIÓN ===")
print(df_regresion_f3.to_string(index=False))

print("\nModelo seleccionado en validación:",
      mejor_regresion_f3)

print("\n=== CLASIFICACIÓN EN PRUEBA ===")
print(df_clasificacion_test_f3.to_string(index=False))

print("\n=== CLASIFICACIÓN - VALIDACIÓN TEMPORAL ===")
print(df_clasificacion_cv_f3.to_string(index=False))

print("\nClasificador seleccionado:",
      mejor_clasificacion_f3)

print("\n=== CLUSTERING ===")
print(df_clustering_f3.to_string(index=False))

print("\nARI:", ari_f3)

print("\n=== HIPERPARÁMETROS ===")
print(df_configuraciones_f3.to_string(index=False))

print("\n=== DISTRIBUCIÓN DE CLASES ===")
print(df_clases_f3.to_string(index=False))

print("\nUmbral de demanda:", umbral_demanda_f3)

print("\n=== VALIDACIÓN CRUZADA TEMPORAL ===")
print(df_folds_f3.to_string(index=False))

print("\nFolds utilizables:", folds_validos_f3)

print("\n=== GRÁFICAS INTERACTIVAS ===")

for nombre in figuras_fase3:
    print(f"{nombre}: OK")

print("\n=== VALIDACIONES ===")
print("Integridad de métricas originales: OK")
print("Distribución de clases: OK")
print("Validación temporal: OK")
print("Selección de modelos: OK")
print("Modelos reentrenados: 0")
print("Tablas consolidadas:", len(tablas_fase3))
print("Gráficas interactivas:", len(figuras_fase3))
print("Imágenes originales:", len(df_imagenes_f3))

print("\nFase 3 - Consolidación finalizada correctamente.")