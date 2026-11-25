
# ==========================================================
# FASE 4 - CELDA 8
# Partición de entrenamiento, validación y prueba
# ==========================================================

from sklearn.model_selection import train_test_split

# ----------------------------------------------------------
# 1. Definir predictores
# ----------------------------------------------------------

numericas = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "temp_hum_interaccion",
    "mes_sin",
    "mes_cos"
]

categoricas = [
    "season",
    "yr",
    "holiday",
    "weekday",
    "workingday",
    "weathersit",
    "fin_de_semana"
]

predictores = numericas + categoricas

X = df_features[predictores].copy()

# Variable objetivo de regresión
y_reg = df_features["cnt"].copy()

# Variable objetivo de clasificación
# Umbral previamente establecido en la Fase 3
UMBRAL_DEMANDA = 3974

y_clf = (
    y_reg >= UMBRAL_DEMANDA
).astype(int)

# ----------------------------------------------------------
# 2. Partición cronológica para regresión
# ----------------------------------------------------------

n = len(df_features)

n_train = int(n * 0.70)
n_val = int(n * 0.15)

X_train_reg = X.iloc[:n_train].copy()

X_val_reg = X.iloc[
    n_train:n_train + n_val
].copy()

X_test_reg = X.iloc[
    n_train + n_val:
].copy()

y_train_reg = y_reg.loc[X_train_reg.index]
y_val_reg = y_reg.loc[X_val_reg.index]
y_test_reg = y_reg.loc[X_test_reg.index]

# ----------------------------------------------------------
# 3. Partición estratificada para clasificación
# ----------------------------------------------------------

X_train_clf, X_temp_clf, y_train_clf, y_temp_clf = (
    train_test_split(
        X,
        y_clf,
        test_size=0.30,
        random_state=SEMILLA,
        stratify=y_clf
    )
)

# Dividir el 30 % restante en validación y prueba
X_val_clf, X_test_clf, y_val_clf, y_test_clf = (
    train_test_split(
        X_temp_clf,
        y_temp_clf,
        test_size=0.50,
        random_state=SEMILLA,
        stratify=y_temp_clf
    )
)

# ----------------------------------------------------------
# 4. Resumen de particiones
# ----------------------------------------------------------

tabla_particiones = pd.DataFrame([
    {
        "Problema": "Regresión",
        "Entrenamiento": len(X_train_reg),
        "Validación": len(X_val_reg),
        "Prueba": len(X_test_reg)
    },
    {
        "Problema": "Clasificación",
        "Entrenamiento": len(X_train_clf),
        "Validación": len(X_val_clf),
        "Prueba": len(X_test_clf)
    }
])

print("=== DISTRIBUCIÓN DE PARTICIONES ===")
display(tabla_particiones)

# ----------------------------------------------------------
# 5. Cobertura temporal de regresión
# ----------------------------------------------------------

print("\n=== COBERTURA TEMPORAL DE REGRESIÓN ===")

for nombre, conjunto in [
    ("Entrenamiento", X_train_reg),
    ("Validación", X_val_reg),
    ("Prueba", X_test_reg)
]:

    fechas = df_features.loc[
        conjunto.index, "dteday"
    ]

    print(
        nombre,
        "| Desde:", fechas.min().date(),
        "| Hasta:", fechas.max().date()
    )

# ----------------------------------------------------------
# 6. Distribución de clases
# ----------------------------------------------------------

distribucion_clases = pd.DataFrame({
    "Entrenamiento": y_train_clf.value_counts(),
    "Validación": y_val_clf.value_counts(),
    "Prueba": y_test_clf.value_counts()
}).sort_index()

distribucion_clases.index = [
    "Demanda baja",
    "Demanda alta"
]

print("\n=== DISTRIBUCIÓN DE CLASES ===")
print("Umbral de demanda:", UMBRAL_DEMANDA)

display(distribucion_clases)

# Proporciones porcentuales
proporciones_clases = (
    distribucion_clases.div(
        distribucion_clases.sum(axis=0),
        axis=1
    ) * 100
)

print("\n=== PROPORCIÓN DE CLASES (%) ===")
display(proporciones_clases.round(2))

# ----------------------------------------------------------
# 7. Visualización del balance de clases
# ----------------------------------------------------------

proporciones_clases.T.plot(
    kind="bar",
    figsize=(10, 5),
    rot=0
)

plt.title("Distribución estratificada de clases")
plt.ylabel("Porcentaje de observaciones")
plt.xlabel("Conjunto de datos")
plt.ylim(0, 100)
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()

plt.savefig(
    RESULTADOS / "particion_estratificada.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 8. Verificaciones contra Data Leakage
# ----------------------------------------------------------

for train, val, test in [
    (X_train_reg, X_val_reg, X_test_reg),
    (X_train_clf, X_val_clf, X_test_clf)
]:

    assert len(train) + len(val) + len(test) == 731

    assert set(train.index).isdisjoint(val.index)
    assert set(train.index).isdisjoint(test.index)
    assert set(val.index).isdisjoint(test.index)

# Verificar orden cronológico en regresión
assert X_train_reg.index.max() < X_val_reg.index.min()

assert X_val_reg.index.max() < X_test_reg.index.min()

# Verificar presencia de ambas clases
for conjunto in [
    y_train_clf,
    y_val_clf,
    y_test_clf
]:
    assert conjunto.nunique() == 2

# Verificar exclusión de variables que generan fuga
assert not {
    "cnt", "casual", "registered"
}.intersection(predictores)

print("\nPredictores seleccionados:", len(predictores))
print("Verificación de particiones: correcta.")
print("Partición de datos completada.")
