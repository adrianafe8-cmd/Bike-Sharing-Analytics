
# ==========================================================
# FASE 4 - CELDA 11
# Codificación categórica sin Data Leakage
# ==========================================================

from sklearn.preprocessing import OneHotEncoder

# ----------------------------------------------------------
# 1. Crear codificadores independientes
# ----------------------------------------------------------

encoder_reg = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

encoder_clf = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

# ----------------------------------------------------------
# 2. Ajustar exclusivamente sobre entrenamiento
# ----------------------------------------------------------

encoder_reg.fit(
    X_train_reg_w[categoricas]
)

encoder_clf.fit(
    X_train_clf_w[categoricas]
)

# ----------------------------------------------------------
# 3. Función para transformar variables categóricas
# ----------------------------------------------------------

def codificar_categoricas(datos, encoder):

    matriz = encoder.transform(
        datos[categoricas]
    )

    nombres = encoder.get_feature_names_out(
        categoricas
    )

    return pd.DataFrame(
        matriz,
        columns=nombres,
        index=datos.index
    )

# ----------------------------------------------------------
# 4. Codificación para regresión
# ----------------------------------------------------------

X_train_reg_cat = codificar_categoricas(
    X_train_reg_w, encoder_reg
)

X_val_reg_cat = codificar_categoricas(
    X_val_reg_w, encoder_reg
)

X_test_reg_cat = codificar_categoricas(
    X_test_reg_w, encoder_reg
)

# ----------------------------------------------------------
# 5. Codificación para clasificación
# ----------------------------------------------------------

X_train_clf_cat = codificar_categoricas(
    X_train_clf_w, encoder_clf
)

X_val_clf_cat = codificar_categoricas(
    X_val_clf_w, encoder_clf
)

X_test_clf_cat = codificar_categoricas(
    X_test_clf_w, encoder_clf
)

# ----------------------------------------------------------
# 6. Categorías aprendidas en entrenamiento
# ----------------------------------------------------------

tabla_categorias = pd.DataFrame([
    {
        "Problema": problema,
        "Variable": variable,
        "Categorias": list(categorias),
        "Columnas_generadas": len(categorias)
    }
    for problema, encoder in [
        ("Regresión", encoder_reg),
        ("Clasificación", encoder_clf)
    ]
    for variable, categorias in zip(
        categoricas, encoder.categories_
    )
])

print("=== CATEGORÍAS APRENDIDAS ===")

display(tabla_categorias)

# ----------------------------------------------------------
# 7. Dimensiones de los conjuntos codificados
# ----------------------------------------------------------

conjuntos_codificados = [
    ("Regresión", "Entrenamiento",
     X_train_reg_w, X_train_reg_cat),

    ("Regresión", "Validación",
     X_val_reg_w, X_val_reg_cat),

    ("Regresión", "Prueba",
     X_test_reg_w, X_test_reg_cat),

    ("Clasificación", "Entrenamiento",
     X_train_clf_w, X_train_clf_cat),

    ("Clasificación", "Validación",
     X_val_clf_w, X_val_clf_cat),

    ("Clasificación", "Prueba",
     X_test_clf_w, X_test_clf_cat)
]

tabla_codificacion = pd.DataFrame([
    {
        "Problema": problema,
        "Conjunto": conjunto,
        "Registros": len(codificado),
        "Variables_originales": len(categoricas),
        "Columnas_codificadas": codificado.shape[1]
    }
    for problema, conjunto, original, codificado
    in conjuntos_codificados
])

print("\n=== DIMENSIONES DESPUÉS DE CODIFICAR ===")

display(tabla_codificacion)

# ----------------------------------------------------------
# 8. Ejemplo de transformación
# ----------------------------------------------------------

print("\n=== EJEMPLO DE CODIFICACIÓN ===")

display(
    X_train_reg_cat.head().astype(int)
)

# ----------------------------------------------------------
# 9. Verificaciones de integridad
# ----------------------------------------------------------

for problema, conjunto, original, codificado in (
    conjuntos_codificados
):

    assert len(original) == len(codificado)

    assert original.index.equals(
        codificado.index
    )

    assert codificado.isna().sum().sum() == 0

    assert np.isin(
        codificado.to_numpy(),
        [0, 1]
    ).all()

# Verificar consistencia de columnas en regresión
assert X_train_reg_cat.columns.equals(
    X_val_reg_cat.columns
)

assert X_train_reg_cat.columns.equals(
    X_test_reg_cat.columns
)

# Verificar consistencia de columnas en clasificación
assert X_train_clf_cat.columns.equals(
    X_val_clf_cat.columns
)

assert X_train_clf_cat.columns.equals(
    X_test_clf_cat.columns
)

# ----------------------------------------------------------
# 10. Verificar categorías desconocidas
# ----------------------------------------------------------

resultados_desconocidas = []

for problema, conjunto, original, codificado in (
    conjuntos_codificados
):

    encoder = (
        encoder_reg
        if problema == "Regresión"
        else encoder_clf
    )

    for variable, categorias in zip(
        categoricas, encoder.categories_
    ):

        cantidad = int(
            (~original[variable].isin(categorias)).sum()
        )

        resultados_desconocidas.append({
            "Problema": problema,
            "Conjunto": conjunto,
            "Variable": variable,
            "Categorias_desconocidas": cantidad
        })

tabla_desconocidas = pd.DataFrame(
    resultados_desconocidas
)

print("\n=== CATEGORÍAS DESCONOCIDAS ===")

display(
    tabla_desconocidas.groupby(
        ["Problema", "Conjunto"]
    )["Categorias_desconocidas"]
    .sum()
    .reset_index()
)

# ----------------------------------------------------------
# 11. Guardar evidencias
# ----------------------------------------------------------

tabla_categorias.to_csv(
    RESULTADOS / "categorias_aprendidas.csv",
    index=False
)

tabla_codificacion.to_csv(
    RESULTADOS / "resultados_codificacion.csv",
    index=False
)

tabla_desconocidas.to_csv(
    RESULTADOS / "categorias_desconocidas.csv",
    index=False
)

print("\n=== VERIFICACIÓN FINAL ===")

print("Codificadores independientes: 2")
print("Ajuste exclusivo en entrenamiento: Sí")
print("Registros eliminados: 0")
print("Valores faltantes generados: 0")
print("Codificación One-Hot completada.")
