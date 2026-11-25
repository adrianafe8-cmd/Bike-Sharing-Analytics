
# ==========================================================
# FASE 3 - CELDA 7
# Entrenamiento y optimización de Ridge
# ==========================================================

from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Valores de regularización que vamos a comparar
alphas = [0.01, 0.1, 1, 10, 100, 1000]

resultados_ridge = []
modelos_ridge = {}

for alpha in alphas:

    # Entrenar exclusivamente con entrenamiento
    modelo = Ridge(alpha=alpha)

    modelo.fit(
        X_train_procesado,
        y_train
    )

    # Predicciones sobre validación
    predicciones = modelo.predict(
        X_val_procesado
    )

    # Calcular métricas
    mae = mean_absolute_error(
        y_val,
        predicciones
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_val,
            predicciones
        )
    )

    r2 = r2_score(
        y_val,
        predicciones
    )

    resultados_ridge.append({
        "alpha": alpha,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    modelos_ridge[alpha] = modelo

# Crear tabla de comparación
tabla_ridge = pd.DataFrame(
    resultados_ridge
).sort_values("RMSE").reset_index(drop=True)

display(
    tabla_ridge.style.format({
        "alpha": "{:.2f}",
        "MAE": "{:.2f}",
        "RMSE": "{:.2f}",
        "R2": "{:.4f}"
    })
)

# Seleccionar mejor alpha usando validación
mejor_alpha = float(
    tabla_ridge.iloc[0]["alpha"]
)

mejor_ridge = modelos_ridge[
    mejor_alpha
]

print("Mejor alpha:", mejor_alpha)

print(
    "RMSE de validación:",
    round(tabla_ridge.iloc[0]["RMSE"], 2)
)

# Verificaciones automáticas
assert len(tabla_ridge) == len(alphas)
assert np.isfinite(
    tabla_ridge[["MAE", "RMSE", "R2"]].to_numpy()
).all()

assert mejor_alpha in modelos_ridge

print("Optimización Ridge completada.")
