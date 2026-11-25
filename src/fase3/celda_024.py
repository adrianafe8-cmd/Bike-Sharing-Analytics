
# ==========================================================
# FASE 3 - CELDA 14
# Optimización de Random Forest Classifier
# ==========================================================

from sklearn.ensemble import RandomForestClassifier

resultados_rf_clf = []

# Configuraciones a evaluar
n_estimators_clf = [100, 200]
max_depth_clf = [5, 10, None]
min_samples_leaf_clf = [1, 3]

for n_arboles in n_estimators_clf:
    for profundidad in max_depth_clf:
        for min_hoja in min_samples_leaf_clf:

            metricas_folds = []

            for idx_train, idx_val in folds_clf_validos:

                X_fold_train = X_train.iloc[idx_train]
                X_fold_val = X_train.iloc[idx_val]

                y_fold_train = y_train_clf.iloc[idx_train]
                y_fold_val = y_train_clf.iloc[idx_val]

                # Pipeline ajustado dentro de cada fold
                pipeline_rf = Pipeline([
                    (
                        "preprocesamiento",
                        clone(preprocesador)
                    ),
                    (
                        "clasificador",
                        RandomForestClassifier(
                            n_estimators=n_arboles,
                            max_depth=profundidad,
                            min_samples_leaf=min_hoja,
                            random_state=SEMILLA,
                            n_jobs=-1
                        )
                    )
                ])

                pipeline_rf.fit(
                    X_fold_train,
                    y_fold_train
                )

                pred = pipeline_rf.predict(
                    X_fold_val
                )

                prob = pipeline_rf.predict_proba(
                    X_fold_val
                )[:, 1]

                metricas_folds.append({
                    "Accuracy": accuracy_score(
                        y_fold_val, pred
                    ),
                    "Precision": precision_score(
                        y_fold_val, pred,
                        zero_division=0
                    ),
                    "Recall": recall_score(
                        y_fold_val, pred,
                        zero_division=0
                    ),
                    "F1": f1_score(
                        y_fold_val, pred,
                        zero_division=0
                    ),
                    "AUC_ROC": roc_auc_score(
                        y_fold_val, prob
                    )
                })

            promedios = pd.DataFrame(
                metricas_folds
            ).mean()

            resultados_rf_clf.append({
                "n_estimators": n_arboles,
                "max_depth": str(profundidad),
                "min_samples_leaf": min_hoja,
                "Accuracy": promedios["Accuracy"],
                "Precision": promedios["Precision"],
                "Recall": promedios["Recall"],
                "F1": promedios["F1"],
                "AUC_ROC": promedios["AUC_ROC"]
            })

# Tabla comparativa
tabla_rf_clf = pd.DataFrame(
    resultados_rf_clf
).sort_values(
    ["F1", "AUC_ROC"],
    ascending=False
).reset_index(drop=True)

display(
    tabla_rf_clf.style.format({
        "Accuracy": "{:.4f}",
        "Precision": "{:.4f}",
        "Recall": "{:.4f}",
        "F1": "{:.4f}",
        "AUC_ROC": "{:.4f}"
    })
)

# Seleccionar mejor configuración
mejor_config_rf_clf = tabla_rf_clf.iloc[0]

print(
    "Mejor configuración:",
    int(mejor_config_rf_clf["n_estimators"]),
    mejor_config_rf_clf["max_depth"],
    int(mejor_config_rf_clf["min_samples_leaf"])
)

print(
    "F1 promedio:",
    round(mejor_config_rf_clf["F1"], 4)
)

# Verificaciones automáticas
assert len(tabla_rf_clf) == 12

assert np.isfinite(
    tabla_rf_clf[
        ["Accuracy", "Precision", "Recall", "F1", "AUC_ROC"]
    ].to_numpy()
).all()

print("Optimización Random Forest Classifier completada.")
