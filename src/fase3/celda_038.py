
# ==========================================================
# FASE 3 - CELDA 21
# Interpretabilidad: importancia por permutación
# ==========================================================

from sklearn.inspection import permutation_importance

# Mejor modelo de regresión ya seleccionado
assert mejor_nombre == "Random Forest"

# Importancia sobre validación, no sobre prueba
importancias = permutation_importance(
    mejor_rf,
    X_val_procesado,
    y_val,
    scoring="neg_root_mean_squared_error",
    n_repeats=10,
    random_state=SEMILLA,
    n_jobs=-1
)

# Nombres de las características transformadas
nombres_variables = (
    preprocesador.get_feature_names_out()
)

tabla_importancias = pd.DataFrame({
    "Variable": nombres_variables,
    "Importancia_RMSE": importancias.importances_mean,
    "Desviacion": importancias.importances_std
}).sort_values(
    "Importancia_RMSE",
    ascending=False
).reset_index(drop=True)

print("Importancia por permutación:")
display(tabla_importancias.head(12).round(3))

# Visualización de las 10 variables más importantes
top_importancias = (
    tabla_importancias.head(10)
    .sort_values("Importancia_RMSE")
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_importancias["Variable"],
    top_importancias["Importancia_RMSE"]
)

plt.axvline(0, color="black", linewidth=0.8)
plt.title(
    "Importancia por permutación - Random Forest"
)
plt.xlabel(
    "Incremento promedio del RMSE al permutar"
)
plt.ylabel("Característica transformada")
plt.tight_layout()

ruta_importancias = (
    RESULTADOS / "importancia_variables_regresion.png"
)

plt.savefig(
    ruta_importancias,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

assert len(tabla_importancias) == (
    X_val_procesado.shape[1]
)

assert np.isfinite(
    tabla_importancias["Importancia_RMSE"]
).all()

print("Análisis de interpretabilidad completado.")
