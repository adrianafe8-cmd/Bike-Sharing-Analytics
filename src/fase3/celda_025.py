
# ==========================================================
# FASE 3 - CELDA 15
# Comparación KNN vs Random Forest Classifier
# ==========================================================

# Recuperar mejores configuraciones
mejor_knn_fila = tabla_knn.iloc[0]
mejor_rf_fila = tabla_rf_clf.iloc[0]

metricas_clf = [
    "Accuracy", "Precision", "Recall", "F1", "AUC_ROC"
]

comparacion_clasificacion = pd.DataFrame([
    {
        "Modelo": "KNN",
        **{
            metrica: float(mejor_knn_fila[metrica])
            for metrica in metricas_clf
        }
    },
    {
        "Modelo": "Random Forest",
        **{
            metrica: float(mejor_rf_fila[metrica])
            for metrica in metricas_clf
        }
    }
])

display(
    comparacion_clasificacion.style.format(
        {m: "{:.4f}" for m in metricas_clf}
    )
)

# Gráfico comparativo
datos_grafico = comparacion_clasificacion.melt(
    id_vars="Modelo",
    value_vars=metricas_clf,
    var_name="Métrica",
    value_name="Valor"
)

plt.figure(figsize=(12, 5))

sns.barplot(
    data=datos_grafico,
    x="Métrica",
    y="Valor",
    hue="Modelo"
)

plt.title(
    "Comparación de modelos de clasificación"
)
plt.ylabel("Puntuación promedio")
plt.ylim(0, 1)
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

ruta_grafico_clf = (
    RESULTADOS / "comparacion_clasificacion.png"
)

plt.savefig(
    ruta_grafico_clf,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Selección por F1-Score
indice_mejor = (
    comparacion_clasificacion["F1"].idxmax()
)

mejor_nombre_clf = (
    comparacion_clasificacion.loc[
        indice_mejor, "Modelo"
    ]
)

print("Mejor clasificador:", mejor_nombre_clf)
print("Gráfico guardado en:", ruta_grafico_clf)

assert mejor_nombre_clf == "KNN"

print("Comparación de clasificación completada.")
