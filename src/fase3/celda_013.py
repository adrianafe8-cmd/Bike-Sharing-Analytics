
# ==========================================================
# FASE 3 - CELDA 9
# Comparación Ridge vs Random Forest
# ==========================================================

# Recuperar las métricas de los mejores modelos
comparacion_regresion = pd.DataFrame([
    {
        "Modelo": "Ridge",
        "MAE": tabla_ridge.iloc[0]["MAE"],
        "RMSE": tabla_ridge.iloc[0]["RMSE"],
        "R2": tabla_ridge.iloc[0]["R2"]
    },
    {
        "Modelo": "Random Forest",
        "MAE": tabla_rf.iloc[0]["MAE"],
        "RMSE": tabla_rf.iloc[0]["RMSE"],
        "R2": tabla_rf.iloc[0]["R2"]
    }
])

display(comparacion_regresion.round(4))

# Gráficos comparativos
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, metrica in zip(
    axes,
    ["MAE", "RMSE", "R2"]
):
    sns.barplot(
        data=comparacion_regresion,
        x="Modelo",
        y=metrica,
        ax=ax
    )

    ax.set_title(f"Comparación de {metrica}")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)

plt.suptitle(
    "Fase 3 - Comparación de regresión avanzada"
)

plt.tight_layout()

ruta_grafico = (
    RESULTADOS / "comparacion_regresion.png"
)

plt.savefig(
    ruta_grafico,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Selección del mejor modelo por RMSE
mejor_nombre = comparacion_regresion.loc[
    comparacion_regresion["RMSE"].idxmin(),
    "Modelo"
]

mejor_modelo_regresion = (
    mejor_rf
    if mejor_nombre == "Random Forest"
    else mejor_ridge
)

print("Mejor modelo:", mejor_nombre)
print("Gráfico guardado en:", ruta_grafico)

assert mejor_nombre == "Random Forest"
print("Comparación completada.")
