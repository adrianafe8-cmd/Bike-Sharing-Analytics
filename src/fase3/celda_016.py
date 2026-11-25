
# ==========================================================
# FASE 3 - CELDA 10
# Crear variable objetivo para clasificación
# ==========================================================

# Calcular el umbral SOLO con entrenamiento
umbral_demanda = float(y_train.median())

print(
    "Umbral de demanda:",
    round(umbral_demanda, 2),
    "alquileres diarios"
)

# Crear etiquetas binarias
# 0 = demanda baja; 1 = demanda alta
y_train_clf = (
    y_train >= umbral_demanda
).astype(int)

y_val_clf = (
    y_val >= umbral_demanda
).astype(int)

y_test_clf = (
    y_test >= umbral_demanda
).astype(int)

# Mostrar distribución de clases
distribucion_clases = pd.DataFrame({
    "Entrenamiento": y_train_clf.value_counts(),
    "Validación": y_val_clf.value_counts(),
    "Prueba": y_test_clf.value_counts()
}).fillna(0).astype(int)

distribucion_clases.index = (
    distribucion_clases.index.map({
        0: "Demanda baja",
        1: "Demanda alta"
    })
)

display(distribucion_clases)

# Verificaciones automáticas
assert set(y_train_clf.unique()) == {0, 1}
assert len(y_train_clf) == 511
assert len(y_val_clf) == 109
assert len(y_test_clf) == 111

assert (
    y_train_clf.index.equals(X_train.index)
    and y_val_clf.index.equals(X_val.index)
    and y_test_clf.index.equals(X_test.index)
)

print("Variable objetivo de clasificación creada.")
