
# ==========================================================
# FASE 4 - CELDA 15
# Consolidación y evaluación final de resultados
# ==========================================================

print("=" * 65)
print("RESUMEN FINAL - FASE 4")
print("=" * 65)

# ----------------------------------------------------------
# 1. Resumen de preparación de datos
# ----------------------------------------------------------

resumen_preparacion = pd.DataFrame([
    ["Registros originales", 731],
    ["Variables originales", 16],
    ["Valores faltantes", 0],
    ["Registros duplicados", 0],
    ["Registros eliminados", 0],
    ["Variables derivadas", 4],
    ["Variables numéricas estandarizadas", 7],
    ["Columnas One-Hot Encoding", 22],
    ["Características predictoras finales", 29],
    ["Datos sintéticos generados", 0],
    ["Umbral de clasificación", 3974]
], columns=["Indicador", "Resultado"])

print("\n1. RESUMEN DE PREPARACIÓN DE DATOS")

display(resumen_preparacion)

# ----------------------------------------------------------
# 2. Resultados finales de regresión
# ----------------------------------------------------------

resumen_regresion = (
    tabla_baseline_reg[
        tabla_baseline_reg["Conjunto"] == "Prueba"
    ]
    .drop(columns="Conjunto")
    .sort_values("RMSE")
    .reset_index(drop=True)
)

print("\n2. BASELINE DE REGRESIÓN - PRUEBA")

display(resumen_regresion.round(4))

# ----------------------------------------------------------
# 3. Resultados finales de clasificación
# ----------------------------------------------------------

resumen_clasificacion = (
    tabla_baseline_clf[
        tabla_baseline_clf["Conjunto"] == "Prueba"
    ]
    .drop(columns="Conjunto")
    .sort_values("F1_Macro", ascending=False)
    .reset_index(drop=True)
)

print("\n3. BASELINE DE CLASIFICACIÓN - PRUEBA")

display(resumen_clasificacion.round(4))

# ----------------------------------------------------------
# 4. Mejoras frente a los modelos Dummy
# ----------------------------------------------------------

resumen_mejoras = pd.DataFrame([
    {
        "Problema": "Regresión",
        "Indicador": "Reducción relativa del RMSE (%)",
        "Resultado": mejora_rmse
    },
    {
        "Problema": "Clasificación",
        "Indicador": "Mejora F1 Macro (pp)",
        "Resultado": diferencia_f1_macro
    },
    {
        "Problema": "Clasificación",
        "Indicador": "Mejora Accuracy (pp)",
        "Resultado": (
            resultados_prueba_clf.loc[
                "Regresión Logística", "Accuracy"
            ]
            -
            resultados_prueba_clf.loc[
                "Dummy Classifier", "Accuracy"
            ]
        ) * 100
    }
])

print("\n4. MEJORAS FRENTE A MODELOS DUMMY")

display(resumen_mejoras.round(4))

# ----------------------------------------------------------
# 5. Verificación de requerimientos técnicos
# ----------------------------------------------------------

cumplimiento = pd.DataFrame([
    [
        "Diagnóstico de valores faltantes",
        "Cumplido",
        "No se identificaron valores faltantes"
    ],
    [
        "Análisis MCAR, MAR y MNAR",
        "Cumplido",
        "No aplica imputación por ausencia de datos faltantes"
    ],
    [
        "Tratamiento de outliers",
        "Cumplido",
        "Winsorization P1-P99"
    ],
    [
        "Ingeniería de características",
        "Cumplido",
        "Cuatro variables derivadas"
    ],
    [
        "Codificación categórica",
        "Cumplido",
        "One-Hot Encoding"
    ],
    [
        "Escalamiento",
        "Cumplido",
        "StandardScaler"
    ],
    [
        "Prevención de fuga en preprocesamiento",
        "Cumplido",
        "Ajuste de transformadores solo en entrenamiento"
    ],
    [
        "Partición de regresión",
        "Cumplido",
        "División cronológica 70-15-15 aproximada"
    ],
    [
        "Partición de clasificación",
        "Cumplido",
        "División estratificada 70-15-15 aproximada"
    ],
    [
        "Análisis de desbalance",
        "Cumplido",
        "Imbalance Ratio de 1.6477"
    ],
    [
        "Tratamiento de desbalance severo",
        "No aplica",
        "No se identificó desbalance severo"
    ],
    [
        "Baseline de regresión",
        "Cumplido",
        "LinearRegression y DummyRegressor"
    ],
    [
        "Baseline de clasificación",
        "Cumplido",
        "LogisticRegression y DummyClassifier"
    ]
], columns=[
    "Requerimiento",
    "Estado",
    "Evidencia"
])

print("\n5. CUMPLIMIENTO DE REQUERIMIENTOS")

display(cumplimiento)

# ----------------------------------------------------------
# 6. Guardar resultados consolidados
# ----------------------------------------------------------

resumen_preparacion.to_csv(
    RESULTADOS / "resumen_preparacion.csv",
    index=False
)

resumen_regresion.to_csv(
    RESULTADOS / "resumen_final_regresion.csv",
    index=False
)

resumen_clasificacion.to_csv(
    RESULTADOS / "resumen_final_clasificacion.csv",
    index=False
)

resumen_mejoras.to_csv(
    RESULTADOS / "resumen_mejoras.csv",
    index=False
)

cumplimiento.to_csv(
    RESULTADOS / "cumplimiento_requerimientos.csv",
    index=False
)

# ----------------------------------------------------------
# 7. Verificación de archivos generados
# ----------------------------------------------------------

archivos_esperados = [
    "deteccion_outliers.png",
    "comparacion_estandarizacion.png",
    "comparacion_baseline_regresion.png",
    "predicciones_baseline_regresion.png",
    "comparacion_baseline_clasificacion.png",
    "matrices_baseline_clasificacion.png",
    "curvas_roc_baseline.png",
    "resumen_preparacion.csv",
    "resumen_final_regresion.csv",
    "resumen_final_clasificacion.csv",
    "resumen_mejoras.csv",
    "cumplimiento_requerimientos.csv"
]

archivos_faltantes = []

print("\n6. VERIFICACIÓN DE EVIDENCIAS")

for archivo in archivos_esperados:

    ruta = RESULTADOS / archivo

    if ruta.exists():
        print("OK:", archivo)
    else:
        print("FALTA:", archivo)
        archivos_faltantes.append(archivo)

# ----------------------------------------------------------
# 8. Inventario completo de resultados
# ----------------------------------------------------------

inventario = pd.DataFrame([
    {
        "Archivo": archivo.name,
        "Formato": archivo.suffix,
        "Tamano_KB": round(
            archivo.stat().st_size / 1024, 2
        )
    }
    for archivo in sorted(RESULTADOS.iterdir())
    if archivo.is_file()
])

print("\n7. INVENTARIO DE ARCHIVOS GENERADOS")

display(inventario)

# ----------------------------------------------------------
# 9. Verificaciones finales
# ----------------------------------------------------------

assert len(archivos_faltantes) == 0

assert X_train_reg_final.shape == (511, 29)
assert X_train_clf_final.shape == (511, 29)

assert len(resumen_regresion) == 2
assert len(resumen_clasificacion) == 2

print("\n" + "=" * 65)
print("VERIFICACIÓN FINAL")
print("=" * 65)

print("Requerimientos evaluados:", len(cumplimiento))

print(
    "Requerimientos cumplidos:",
    (cumplimiento["Estado"] == "Cumplido").sum()
)

print(
    "Requerimientos no aplicables:",
    (cumplimiento["Estado"] == "No aplica").sum()
)

print("Archivos faltantes:", len(archivos_faltantes))

print("Consolidación de resultados completada.")
