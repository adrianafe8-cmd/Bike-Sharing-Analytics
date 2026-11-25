
# ==========================================================
# FASE 3 - CELDA 22
# Evaluación final de modelos de regresión
# ==========================================================

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Modelos previamente seleccionados
modelos_regresion_final = {
    "Ridge": mejor_ridge,
    "Random Forest": mejor_rf
}

resultados_regresion_test = []
predicciones_regresion_test = {}

for nombre, modelo in modelos_regresion_final.items():

    # Evaluación sobre los 111 días reservados
    pred = modelo.predict(X_test_procesado)

    predicciones_regresion_test[nombre] = pred

    resultados_regresion_test.append({
        "Modelo": nombre,
        "MAE": mean_absolute_error(y_test, pred),
        "RMSE": np.sqrt(
            mean_squared_error(y_test, pred)
        ),
        "R2": r2_score(y_test, pred)
    })

tabla_regresion_test = pd.DataFrame(
    resultados_regresion_test
).sort_values(
    "RMSE"
).reset_index(drop=True)

print("Evaluación final de regresión:")
display(
    tabla_regresion_test.style.format({
        "MAE": "{:.2f}",
        "RMSE": "{:.2f}",
        "R2": "{:.4f}"
    })
)

# Comparación visual de predicciones
fig, axes = plt.subplots(
    1, 2,
    figsize=(13, 5)
)

for ax, (nombre, pred) in zip(
    axes,
    predicciones_regresion_test.items()
):

    ax.scatter(
        y_test,
        pred,
        alpha=0.65
    )

    minimo = min(y_test.min(), pred.min())
    maximo = max(y_test.max(), pred.max())

    ax.plot(
        [minimo, maximo],
        [minimo, maximo],
        linestyle="--",
        color="red"
    )

    ax.set_title(nombre)
    ax.set_xlabel("Demanda real")
    ax.set_ylabel("Demanda predicha")
    ax.grid(alpha=0.25)

plt.suptitle(
    "Evaluación final de regresión - Datos de prueba"
)

plt.tight_layout()

ruta_regresion_test = (
    RESULTADOS / "evaluacion_final_regresion.png"
)

plt.savefig(
    ruta_regresion_test,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones
assert len(y_test) == 111

assert len(tabla_regresion_test) == 2

assert np.isfinite(
    tabla_regresion_test[
        ["MAE", "RMSE", "R2"]
    ].to_numpy()
).all()

print("Evaluación final de regresión completada.")
