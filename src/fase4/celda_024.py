
# ==========================================================
# FASE 4 - CELDA 13
# Baseline de regresión lineal simple
# ==========================================================

from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ----------------------------------------------------------
# 1. Seleccionar la variable independiente
# ----------------------------------------------------------

X_train_baseline_reg = X_train_reg_final[["temp"]]
X_val_baseline_reg = X_val_reg_final[["temp"]]
X_test_baseline_reg = X_test_reg_final[["temp"]]

print("=== CONFIGURACIÓN DEL BASELINE ===")

print("Variable independiente: temp")
print("Variable objetivo: cnt")

print(
    "Registros entrenamiento:",
    len(X_train_baseline_reg)
)

# ----------------------------------------------------------
# 2. Crear modelos de referencia
# ----------------------------------------------------------

baseline_lineal = LinearRegression()

baseline_dummy_reg = DummyRegressor(
    strategy="mean"
)

# ----------------------------------------------------------
# 3. Entrenar exclusivamente sobre entrenamiento
# ----------------------------------------------------------

baseline_lineal.fit(
    X_train_baseline_reg,
    y_train_reg
)

baseline_dummy_reg.fit(
    X_train_baseline_reg,
    y_train_reg
)

# ----------------------------------------------------------
# 4. Parámetros aprendidos
# ----------------------------------------------------------

print("\n=== PARÁMETROS DEL MODELO LINEAL ===")

print(
    "Intercepto:",
    round(baseline_lineal.intercept_, 4)
)

print(
    "Coeficiente temperatura estandarizada:",
    round(baseline_lineal.coef_[0], 4)
)

print(
    "Demanda promedio de entrenamiento:",
    round(y_train_reg.mean(), 4)
)

# ----------------------------------------------------------
# 5. Función de evaluación
# ----------------------------------------------------------

def evaluar_baseline_reg(
    nombre,
    modelo,
    conjunto,
    X_eval,
    y_eval
):

    predicciones = modelo.predict(X_eval)

    return {
        "Modelo": nombre,
        "Conjunto": conjunto,
        "MAE": mean_absolute_error(
            y_eval, predicciones
        ),
        "RMSE": np.sqrt(
            mean_squared_error(
                y_eval, predicciones
            )
        ),
        "R2": r2_score(
            y_eval, predicciones
        )
    }

# ----------------------------------------------------------
# 6. Evaluación de los modelos
# ----------------------------------------------------------

resultados_baseline_reg = []

for nombre, modelo in [
    ("Regresión Lineal Simple", baseline_lineal),
    ("Dummy Regressor", baseline_dummy_reg)
]:

    for conjunto, X_eval, y_eval in [
        (
            "Entrenamiento",
            X_train_baseline_reg,
            y_train_reg
        ),
        (
            "Validación",
            X_val_baseline_reg,
            y_val_reg
        ),
        (
            "Prueba",
            X_test_baseline_reg,
            y_test_reg
        )
    ]:

        resultados_baseline_reg.append(
            evaluar_baseline_reg(
                nombre,
                modelo,
                conjunto,
                X_eval,
                y_eval
            )
        )

tabla_baseline_reg = pd.DataFrame(
    resultados_baseline_reg
)

print("\n=== RESULTADOS BASELINE REGRESIÓN ===")

display(tabla_baseline_reg.round(4))

# ----------------------------------------------------------
# 7. Comparación de RMSE
# ----------------------------------------------------------

tabla_comparacion_reg = (
    tabla_baseline_reg.pivot(
        index="Conjunto",
        columns="Modelo",
        values="RMSE"
    )
    .reindex([
        "Entrenamiento",
        "Validación",
        "Prueba"
    ])
)

tabla_comparacion_reg.plot(
    kind="bar",
    figsize=(10, 5),
    rot=0
)

plt.title("Comparación de modelos baseline - RMSE")
plt.ylabel("RMSE - Alquileres diarios")
plt.xlabel("Conjunto de datos")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "comparacion_baseline_regresion.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 8. Predicciones sobre el conjunto de prueba
# ----------------------------------------------------------

pred_baseline_reg = baseline_lineal.predict(
    X_test_baseline_reg
)

limite_min = min(
    y_test_reg.min(),
    pred_baseline_reg.min()
)

limite_max = max(
    y_test_reg.max(),
    pred_baseline_reg.max()
)

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test_reg,
    pred_baseline_reg,
    alpha=0.65,
    color="steelblue"
)

plt.plot(
    [limite_min, limite_max],
    [limite_min, limite_max],
    "r--",
    label="Predicción perfecta"
)

plt.title(
    "Regresión lineal simple: valores reales vs. predichos"
)

plt.xlabel("Demanda real")
plt.ylabel("Demanda predicha")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "predicciones_baseline_regresion.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 9. Mejora frente al modelo Dummy
# ----------------------------------------------------------

resultados_prueba_reg = (
    tabla_baseline_reg[
        tabla_baseline_reg["Conjunto"] == "Prueba"
    ]
    .set_index("Modelo")
)

rmse_lineal = resultados_prueba_reg.loc[
    "Regresión Lineal Simple", "RMSE"
]

rmse_dummy = resultados_prueba_reg.loc[
    "Dummy Regressor", "RMSE"
]

mejora_rmse = (
    (rmse_dummy - rmse_lineal) / rmse_dummy
) * 100

print("\n=== COMPARACIÓN FINAL ===")

print("RMSE regresión lineal:", round(rmse_lineal, 4))
print("RMSE Dummy:", round(rmse_dummy, 4))
print("Mejora relativa RMSE:", round(mejora_rmse, 2), "%")

# ----------------------------------------------------------
# 10. Guardar resultados
# ----------------------------------------------------------

tabla_baseline_reg.to_csv(
    RESULTADOS / "metricas_baseline_regresion.csv",
    index=False
)

# ----------------------------------------------------------
# 11. Verificaciones
# ----------------------------------------------------------

assert X_train_baseline_reg.shape == (511, 1)
assert X_val_baseline_reg.shape == (109, 1)
assert X_test_baseline_reg.shape == (111, 1)

assert baseline_lineal.n_features_in_ == 1

assert len(pred_baseline_reg) == 111

assert np.isfinite(pred_baseline_reg).all()

assert np.isfinite(
    tabla_baseline_reg[
        ["MAE", "RMSE", "R2"]
    ].to_numpy()
).all()

print("\n=== VERIFICACIÓN FINAL ===")
print("Modelos entrenados: 2")
print("Predictor utilizado: temperatura")
print("Entrenamiento exclusivo: Sí")
print("Métricas calculadas: MAE, RMSE y R2")
print("Baseline de regresión completado.")
