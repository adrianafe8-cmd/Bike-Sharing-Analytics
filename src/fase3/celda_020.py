
# ==========================================================
# FASE 3 - CELDA 12
# Diagnóstico de validación temporal interna
# ==========================================================

from sklearn.model_selection import TimeSeriesSplit

# Cinco particiones temporales progresivas
tscv_clf = TimeSeriesSplit(n_splits=5)

resultados_folds = []

for numero, (idx_train, idx_val) in enumerate(
    tscv_clf.split(X_train),
    start=1
):
    y_fold_train = y_train_clf.iloc[idx_train]
    y_fold_val = y_train_clf.iloc[idx_val]

    clases_train = y_fold_train.nunique()
    clases_val = y_fold_val.nunique()

    resultados_folds.append({
        "Fold": numero,
        "N_entrenamiento": len(idx_train),
        "N_validacion": len(idx_val),
        "Clases_entrenamiento": clases_train,
        "Clases_validacion": clases_val,
        "AUC_calculable": clases_val == 2,
        "Fold_utilizable": (
            clases_train == 2 and clases_val == 2
        )
    })

tabla_folds = pd.DataFrame(resultados_folds)

display(tabla_folds)

folds_validos = tabla_folds[
    tabla_folds["Fold_utilizable"]
]

print(
    "Particiones utilizables:",
    len(folds_validos),
    "de",
    len(tabla_folds)
)

assert len(tabla_folds) == 5

print("Diagnóstico temporal completado.")
