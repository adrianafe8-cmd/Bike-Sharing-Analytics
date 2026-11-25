
# ==========================================================
# FASE 3 - CELDA 13
# Optimización de KNN con validación temporal
# ==========================================================

from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# Conservar únicamente folds con ambas clases
folds_clf_validos = []

for idx_train, idx_val in tscv_clf.split(X_train):

    etiquetas_train = y_train_clf.iloc[idx_train]
    etiquetas_val = y_train_clf.iloc[idx_val]

    if (
        etiquetas_train.nunique() == 2
        and etiquetas_val.nunique() == 2
    ):
        folds_clf_validos.append(
            (idx_train, idx_val)
        )

assert len(folds_clf_validos) == 4

# Hiperparámetros a comparar
valores_k = [3, 5, 7, 9, 11, 15]

resultados_knn = []

for k in valores_k:

    metricas_folds = []

    for idx_train, idx_val in folds_clf_validos:

        X_fold_train = X_train.iloc[idx_train]
        X_fold_val = X_train.iloc[idx_val]

        y_fold_train = y_train_clf.iloc[idx_train]
        y_fold_val = y_train_clf.iloc[idx_val]

        # Pipeline: preprocesamiento ajustado
        # exclusivamente en cada fold de entrenamiento
        pipeline_knn = Pipeline([
            (
                "preprocesamiento",
                clone(preprocesador)
            ),
            (
                "clasificador",
                KNeighborsClassifier(
                    n_neighbors=k
                )
            )
        ])

        pipeline_knn.fit(
            X_fold_train,
            y_fold_train
        )

        pred = pipeline_knn.predict(
            X_fold_val
        )

        prob = pipeline_knn.predict_proba(
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

    resultados_knn.append({
        "k": k,
        "Accuracy": promedios["Accuracy"],
        "Precision": promedios["Precision"],
        "Recall": promedios["Recall"],
        "F1": promedios["F1"],
        "AUC_ROC": promedios["AUC_ROC"]
    })

# Comparación de configuraciones
tabla_knn = pd.DataFrame(
    resultados_knn
).sort_values(
    ["F1", "AUC_ROC"],
    ascending=False
).reset_index(drop=True)

display(
    tabla_knn.style.format({
        "Accuracy": "{:.4f}",
        "Precision": "{:.4f}",
        "Recall": "{:.4f}",
        "F1": "{:.4f}",
        "AUC_ROC": "{:.4f}"
    })
)

# Mejor configuración
mejor_k = int(tabla_knn.iloc[0]["k"])

print("Mejor k:", mejor_k)
print(
    "F1 promedio:",
    round(tabla_knn.iloc[0]["F1"], 4)
)

assert len(tabla_knn) == len(valores_k)
assert np.isfinite(
    tabla_knn[
        ["Accuracy", "Precision", "Recall", "F1", "AUC_ROC"]
    ].to_numpy()
).all()

print("Optimización KNN completada.")
