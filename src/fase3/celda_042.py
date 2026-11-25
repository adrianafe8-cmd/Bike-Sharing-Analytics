
# ==========================================================
# FASE 3 - CELDA 23
# Evaluación final de clasificación
# ==========================================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Reconstruir modelos con los parámetros seleccionados
modelos_clasificacion_final = {
    "KNN": Pipeline([
        ("preprocesamiento", clone(preprocesador)),
        ("clasificador", KNeighborsClassifier(
            n_neighbors=mejor_k
        ))
    ]),
    "Random Forest": Pipeline([
        ("preprocesamiento", clone(preprocesador)),
        ("clasificador", RandomForestClassifier(
            n_estimators=int(
                mejor_config_rf_clf["n_estimators"]
            ),
            max_depth=(
                None
                if mejor_config_rf_clf["max_depth"] == "None"
                else int(mejor_config_rf_clf["max_depth"])
            ),
            min_samples_leaf=int(
                mejor_config_rf_clf["min_samples_leaf"]
            ),
            random_state=SEMILLA,
            n_jobs=-1
        ))
    ])
}

resultados_clasificacion_test = []
predicciones_clasificacion_test = {}

# Entrenar únicamente con el conjunto de entrenamiento
for nombre, modelo in modelos_clasificacion_final.items():

    modelo.fit(X_train, y_train_clf)

    pred = modelo.predict(X_test)
    prob = modelo.predict_proba(X_test)[:, 1]

    predicciones_clasificacion_test[nombre] = pred

    resultados_clasificacion_test.append({
        "Modelo": nombre,
        "Accuracy": accuracy_score(y_test_clf, pred),
        "Precision": precision_score(
            y_test_clf, pred, zero_division=0
        ),
        "Recall": recall_score(
            y_test_clf, pred, zero_division=0
        ),
        "F1": f1_score(
            y_test_clf, pred, zero_division=0
        ),
        "AUC_ROC": roc_auc_score(
            y_test_clf, prob
        )
    })

tabla_clasificacion_test = pd.DataFrame(
    resultados_clasificacion_test
).sort_values(
    "F1",
    ascending=False
).reset_index(drop=True)

print("Evaluación final de clasificación:")
display(
    tabla_clasificacion_test.style.format({
        "Accuracy": "{:.4f}",
        "Precision": "{:.4f}",
        "Recall": "{:.4f}",
        "F1": "{:.4f}",
        "AUC_ROC": "{:.4f}"
    })
)

# Matrices de confusión
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, (nombre, pred) in zip(
    axes,
    predicciones_clasificacion_test.items()
):
    matriz = confusion_matrix(
        y_test_clf,
        pred,
        labels=[0, 1]
    )

    ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=["Baja", "Alta"]
    ).plot(
        ax=ax,
        cmap="Blues",
        colorbar=False
    )

    ax.set_title(nombre)

plt.suptitle(
    "Matrices de confusión - Conjunto de prueba"
)
plt.tight_layout()

ruta_clasificacion_test = (
    RESULTADOS / "evaluacion_final_clasificacion.png"
)

plt.savefig(
    ruta_clasificacion_test,
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# Verificaciones
assert len(y_test_clf) == 111
assert y_test_clf.nunique() == 2
assert len(tabla_clasificacion_test) == 2

assert np.isfinite(
    tabla_clasificacion_test[
        ["Accuracy", "Precision", "Recall", "F1", "AUC_ROC"]
    ].to_numpy()
).all()

print("Evaluación final de clasificación completada.")
