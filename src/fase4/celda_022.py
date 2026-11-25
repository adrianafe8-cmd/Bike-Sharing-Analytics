
# ==========================================================
# FASE 4 - CELDA 12
# Estandarización y consolidación de características
# ==========================================================

from sklearn.preprocessing import StandardScaler

# ----------------------------------------------------------
# 1. Crear escaladores independientes
# ----------------------------------------------------------

scaler_reg = StandardScaler()
scaler_clf = StandardScaler()

# ----------------------------------------------------------
# 2. Ajustar exclusivamente sobre entrenamiento
# ----------------------------------------------------------

scaler_reg.fit(
    X_train_reg_w[numericas]
)

scaler_clf.fit(
    X_train_clf_w[numericas]
)

# ----------------------------------------------------------
# 3. Función de estandarización
# ----------------------------------------------------------

def estandarizar_numericas(datos, scaler):

    matriz = scaler.transform(
        datos[numericas]
    )

    return pd.DataFrame(
        matriz,
        columns=numericas,
        index=datos.index
    )

# ----------------------------------------------------------
# 4. Estandarización para regresión
# ----------------------------------------------------------

X_train_reg_num = estandarizar_numericas(
    X_train_reg_w, scaler_reg
)

X_val_reg_num = estandarizar_numericas(
    X_val_reg_w, scaler_reg
)

X_test_reg_num = estandarizar_numericas(
    X_test_reg_w, scaler_reg
)

# ----------------------------------------------------------
# 5. Estandarización para clasificación
# ----------------------------------------------------------

X_train_clf_num = estandarizar_numericas(
    X_train_clf_w, scaler_clf
)

X_val_clf_num = estandarizar_numericas(
    X_val_clf_w, scaler_clf
)

X_test_clf_num = estandarizar_numericas(
    X_test_clf_w, scaler_clf
)

# ----------------------------------------------------------
# 6. Parámetros aprendidos en entrenamiento
# ----------------------------------------------------------

tabla_scaler = pd.DataFrame([
    {
        "Problema": problema,
        "Variable": variable,
        "Media_entrenamiento": media,
        "Desviacion_entrenamiento": desviacion
    }
    for problema, scaler in [
        ("Regresión", scaler_reg),
        ("Clasificación", scaler_clf)
    ]
    for variable, media, desviacion in zip(
        numericas,
        scaler.mean_,
        scaler.scale_
    )
])

print("=== PARÁMETROS DE STANDARD SCALER ===")

display(tabla_scaler.round(6))

# ----------------------------------------------------------
# 7. Verificar medias y desviaciones transformadas
# ----------------------------------------------------------

tabla_estandarizacion = pd.DataFrame([
    {
        "Problema": problema,
        "Variable": variable,
        "Media_transformada": datos[variable].mean(),
        "Desviacion_transformada":
            datos[variable].std(ddof=0)
    }
    for problema, datos in [
        ("Regresión", X_train_reg_num),
        ("Clasificación", X_train_clf_num)
    ]
    for variable in numericas
])

print("\n=== VERIFICACIÓN DE ESTANDARIZACIÓN ===")

display(tabla_estandarizacion.round(6))

# ----------------------------------------------------------
# 8. Consolidar variables numéricas y categóricas
# ----------------------------------------------------------

def consolidar_caracteristicas(
    datos_numericos,
    datos_categoricos
):

    assert datos_numericos.index.equals(
        datos_categoricos.index
    )

    return pd.concat(
        [datos_numericos, datos_categoricos],
        axis=1
    )

# Regresión

X_train_reg_final = consolidar_caracteristicas(
    X_train_reg_num, X_train_reg_cat
)

X_val_reg_final = consolidar_caracteristicas(
    X_val_reg_num, X_val_reg_cat
)

X_test_reg_final = consolidar_caracteristicas(
    X_test_reg_num, X_test_reg_cat
)

# Clasificación

X_train_clf_final = consolidar_caracteristicas(
    X_train_clf_num, X_train_clf_cat
)

X_val_clf_final = consolidar_caracteristicas(
    X_val_clf_num, X_val_clf_cat
)

X_test_clf_final = consolidar_caracteristicas(
    X_test_clf_num, X_test_clf_cat
)

# ----------------------------------------------------------
# 9. Resumen de matrices finales
# ----------------------------------------------------------

conjuntos_finales = [
    ("Regresión", "Entrenamiento",
     X_train_reg_final, y_train_reg),

    ("Regresión", "Validación",
     X_val_reg_final, y_val_reg),

    ("Regresión", "Prueba",
     X_test_reg_final, y_test_reg),

    ("Clasificación", "Entrenamiento",
     X_train_clf_final, y_train_clf),

    ("Clasificación", "Validación",
     X_val_clf_final, y_val_clf),

    ("Clasificación", "Prueba",
     X_test_clf_final, y_test_clf)
]

tabla_matrices_finales = pd.DataFrame([
    {
        "Problema": problema,
        "Conjunto": conjunto,
        "Registros": X_final.shape[0],
        "Caracteristicas": X_final.shape[1],
        "Valores_faltantes":
            X_final.isna().sum().sum()
    }
    for problema, conjunto, X_final, y_final
    in conjuntos_finales
])

print("\n=== MATRICES FINALES ===")

display(tabla_matrices_finales)

print("\n=== EJEMPLO DE MATRIZ FINAL ===")

display(X_train_reg_final.head().round(4))

# ----------------------------------------------------------
# 10. Visualización antes y después
# ----------------------------------------------------------

fig, axes = plt.subplots(
    2, 1,
    figsize=(13, 9)
)

sns.boxplot(
    data=X_train_reg_w[numericas],
    ax=axes[0],
    color="steelblue"
)

axes[0].set_title(
    "Antes de StandardScaler - Regresión"
)

sns.boxplot(
    data=X_train_reg_num,
    ax=axes[1],
    color="darkorange"
)

axes[1].set_title(
    "Después de StandardScaler - Regresión"
)

for ax in axes:

    ax.tick_params(
        axis="x",
        labelrotation=25
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

plt.tight_layout()

plt.savefig(
    RESULTADOS / "comparacion_estandarizacion.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()

# ----------------------------------------------------------
# 11. Verificaciones de integridad
# ----------------------------------------------------------

for datos in [
    X_train_reg_num,
    X_train_clf_num
]:

    assert np.allclose(
        datos.mean().to_numpy(),
        0,
        atol=1e-8
    )

    assert np.allclose(
        datos.std(ddof=0).to_numpy(),
        1,
        atol=1e-8
    )

for problema, conjunto, X_final, y_final in (
    conjuntos_finales
):

    assert X_final.shape[1] == 29

    assert len(X_final) == len(y_final)

    assert X_final.index.equals(
        y_final.index
    )

    assert X_final.isna().sum().sum() == 0

    assert np.isfinite(
        X_final.to_numpy()
    ).all()

    assert not {
        "cnt", "casual", "registered"
    }.intersection(X_final.columns)

# Verificar consistencia de columnas

assert X_train_reg_final.columns.equals(
    X_val_reg_final.columns
)

assert X_train_reg_final.columns.equals(
    X_test_reg_final.columns
)

assert X_train_clf_final.columns.equals(
    X_val_clf_final.columns
)

assert X_train_clf_final.columns.equals(
    X_test_clf_final.columns
)

# ----------------------------------------------------------
# 12. Guardar evidencias
# ----------------------------------------------------------

tabla_scaler.to_csv(
    RESULTADOS / "parametros_standardscaler.csv",
    index=False
)

tabla_estandarizacion.to_csv(
    RESULTADOS / "verificacion_estandarizacion.csv",
    index=False
)

tabla_matrices_finales.to_csv(
    RESULTADOS / "matrices_finales.csv",
    index=False
)

print("\n=== VERIFICACIÓN FINAL ===")

print("Escaladores independientes: 2")
print("Ajuste exclusivo en entrenamiento: Sí")
print("Variables numéricas estandarizadas: 7")
print("Columnas categóricas binarias: 22")
print("Características finales: 29")
print("Valores faltantes generados: 0")
print("Estandarización completada correctamente.")
