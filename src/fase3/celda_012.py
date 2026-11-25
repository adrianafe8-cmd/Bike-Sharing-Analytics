
# ==========================================================
# FASE 3 - CELDA 8
# Entrenamiento y optimización Random Forest Regressor
# ==========================================================

from sklearn.ensemble import RandomForestRegressor

resultados_rf = []
modelos_rf = {}

# Hiperparámetros a evaluar
n_estimators_opciones = [100, 200]
max_depth_opciones = [5, 10, None]
min_samples_leaf_opciones = [1, 3]

for n_arboles in n_estimators_opciones:
    for profundidad in max_depth_opciones:
        for min_hoja in min_samples_leaf_opciones:

            modelo = RandomForestRegressor(
                n_estimators=n_arboles,
                max_depth=profundidad,
                min_samples_leaf=min_hoja,
                random_state=SEMILLA,
                n_jobs=-1
            )

            # Entrenamiento
            modelo.fit(
                X_train_procesado,
                y_train
            )

            # Validación
            predicciones = modelo.predict(
                X_val_procesado
            )

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

            configuracion = (
                n_arboles,
                profundidad,
                min_hoja
            )

            resultados_rf.append({
                "n_estimators": n_arboles,
                "max_depth": str(profundidad),
                "min_samples_leaf": min_hoja,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
                "configuracion": configuracion
            })

            modelos_rf[configuracion] = modelo

# Tabla ordenada por menor RMSE
tabla_rf = pd.DataFrame(
    resultados_rf
).sort_values(
    "RMSE"
).reset_index(drop=True)

display(
    tabla_rf.drop(
        columns="configuracion"
    ).style.format({
        "MAE": "{:.2f}",
        "RMSE": "{:.2f}",
        "R2": "{:.4f}"
    })
)

# Seleccionar mejor modelo
mejor_config_rf = tabla_rf.iloc[0]["configuracion"]

mejor_rf = modelos_rf[
    mejor_config_rf
]

print("\nMejor configuración:", mejor_config_rf)

print(
    "RMSE de validación:",
    round(tabla_rf.iloc[0]["RMSE"], 2)
)

# Verificaciones
assert len(tabla_rf) == 12
assert np.isfinite(
    tabla_rf[["MAE", "RMSE", "R2"]].to_numpy()
).all()

print("Optimización Random Forest completada.")
