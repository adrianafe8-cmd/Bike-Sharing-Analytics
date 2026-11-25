
# ==========================================================
# FASE 3 - CELDA 11
# Diagnóstico de distribución de clases
# ==========================================================

from sklearn.metrics import roc_auc_score

conjuntos_clf = {
    "Entrenamiento": y_train_clf,
    "Validación": y_val_clf,
    "Prueba": y_test_clf
}

for nombre, etiquetas in conjuntos_clf.items():

    conteos = etiquetas.value_counts().sort_index()
    clases = etiquetas.nunique()

    print(f"\n{nombre}")
    print("Clases presentes:", clases)
    print("Distribución:", conteos.to_dict())

    if clases < 2:
        print(
            "ADVERTENCIA: AUC-ROC no está definida "
            "porque solo existe una clase real."
        )
    else:
        print(
            "AUC-ROC podrá calcularse cuando "
            "dispongamos de probabilidades del modelo."
        )

# Verificar el desequilibrio detectado
assert y_train_clf.nunique() == 2
assert y_val_clf.nunique() == 1
assert y_test_clf.nunique() == 2

print("\nDiagnóstico de clasificación completado.")
