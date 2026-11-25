
# ==========================================================
# FASE 4 - CELDA 10
# Winsorization sin fuga de información
# ==========================================================

variables_winsor = ["hum", "windspeed"]

# ----------------------------------------------------------
# 1. Función para calcular límites en entrenamiento
# ----------------------------------------------------------

def calcular_limites_winsor(X_train):

    limites = {}

    for variable in variables_winsor:

        limites[variable] = {
            "P1": X_train[variable].quantile(0.01),
            "P99": X_train[variable].quantile(0.99)
        }

    return limites


# ----------------------------------------------------------
# 2. Función para aplicar Winsorization
# ----------------------------------------------------------

def aplicar_winsor(X, limites):

    datos = X.copy()

    for variable, valores in limites.items():

        datos[variable] = datos[variable].clip(
            lower=valores["P1"],
            upper=valores["P99"]
        )

    # Recalcular la interacción temperatura-humedad
    datos["temp_hum_interaccion"] = (
        datos["temp"] * datos["hum"]
    )

    return datos


# ----------------------------------------------------------
# 3. Calcular límites independientes
# ----------------------------------------------------------

limites_reg = calcular_limites_winsor(
    X_train_reg
)

limites_clf = calcular_limites_winsor(
    X_train_clf
)

tabla_limites = pd.DataFrame([
    {
        "Problema": problema,
        "Variable": variable,
        "P1": valores["P1"],
        "P99": valores["P99"]
    }
    for problema, limites in [
        ("Regresión", limites_reg),
        ("Clasificación", limites_clf)
    ]
    for variable, valores in limites.items()
])

print("=== LÍMITES DE WINSORIZATION ===")

display(tabla_limites.round(6))


# ----------------------------------------------------------
# 4. Aplicar tratamiento para regresión
# ----------------------------------------------------------

X_train_reg_w = aplicar_winsor(
    X_train_reg, limites_reg
)

X_val_reg_w = aplicar_winsor(
    X_val_reg, limites_reg
)

X_test_reg_w = aplicar_winsor(
    X_test_reg, limites_reg
)


# ----------------------------------------------------------
# 5. Aplicar tratamiento para clasificación
# ----------------------------------------------------------

X_train_clf_w = aplicar_winsor(
    X_train_clf, limites_clf
)

X_val_clf_w = aplicar_winsor(
    X_val_clf, limites_clf
)

X_test_clf_w = aplicar_winsor(
    X_test_clf, limites_clf
)


# ----------------------------------------------------------
# 6. Cuantificar valores modificados
# ----------------------------------------------------------

comparaciones = [
    ("Regresión", "Entrenamiento",
     X_train_reg, X_train_reg_w),

    ("Regresión", "Validación",
     X_val_reg, X_val_reg_w),

    ("Regresión", "Prueba",
     X_test_reg, X_test_reg_w),

    ("Clasificación", "Entrenamiento",
     X_train_clf, X_train_clf_w),

    ("Clasificación", "Validación",
     X_val_clf, X_val_clf_w),

    ("Clasificación", "Prueba",
     X_test_clf, X_test_clf_w)
]

resultados_winsor = []

for problema, conjunto, original, tratado in comparaciones:

    for variable in variables_winsor:

        modificados = int(
            (original[variable] != tratado[variable]).sum()
        )

        resultados_winsor.append({
            "Problema": problema,
            "Conjunto": conjunto,
            "Variable": variable,
            "Registros": len(original),
            "Valores_modificados": modificados,
            "Porcentaje": modificados / len(original) * 100
        })

tabla_winsor = pd.DataFrame(resultados_winsor)

print("\n=== VALORES MODIFICADOS ===")

display(tabla_winsor.round(4))


# ----------------------------------------------------------
# 7. Visualización antes y después
# ----------------------------------------------------------

fig, axes = plt.subplots(
    2, 2,
    figsize=(13, 8)
)

for i, (problema, original, tratado) in enumerate([
    ("Regresión", X_train_reg, X_train_reg_w),
    ("Clasificación", X_train_clf, X_train_clf_w)
]):

    for j, variable in enumerate(variables_winsor):

        datos_grafico = pd.DataFrame({
            "Antes": original[variable],
            "Después": tratado[variable]
        })

        sns.boxplot(
            data=datos_grafico,
            ax=axes[i, j]
        )

        axes[i, j].set_title(
            f"{problema} - {variable}"
        )

        axes[i, j].grid(alpha=0.25)

plt.suptitle(
    "Comparación antes y después de Winsorization",
    fontsize=15
)

plt.tight_layout()

plt.savefig(
    RESULTADOS / "comparacion_winsorization.png",
    dpi=160,
    bbox_inches="tight"
)

plt.show()


# ----------------------------------------------------------
# 8. Verificaciones de integridad
# ----------------------------------------------------------

for problema, conjunto, original, tratado in comparaciones:

    # Conservar dimensiones e índices
    assert original.shape == tratado.shape
    assert original.index.equals(tratado.index)

    # Verificar ausencia de valores faltantes
    assert tratado.isna().sum().sum() == 0

    # Verificar consistencia de variable derivada
    assert np.allclose(
        tratado["temp_hum_interaccion"],
        tratado["temp"] * tratado["hum"]
    )

    limites = (
        limites_reg
        if problema == "Regresión"
        else limites_clf
    )

    # Verificar límites aplicados
    for variable in variables_winsor:

        assert tratado[variable].ge(
            limites[variable]["P1"]
        ).all()

        assert tratado[variable].le(
            limites[variable]["P99"]
        ).all()

    # Verificar que las demás variables no cambiaron
    columnas_intactas = [
        c for c in original.columns
        if c not in variables_winsor
        + ["temp_hum_interaccion"]
    ]

    assert original[columnas_intactas].equals(
        tratado[columnas_intactas]
    )


# ----------------------------------------------------------
# 9. Guardar evidencias
# ----------------------------------------------------------

tabla_limites.to_csv(
    RESULTADOS / "limites_winsorization.csv",
    index=False
)

tabla_winsor.to_csv(
    RESULTADOS / "resultados_winsorization.csv",
    index=False
)

print("\n=== VERIFICACIÓN FINAL ===")
print("Registros eliminados: 0")
print("Variables objetivo modificadas: 0")
print("Valores faltantes generados: 0")
print("Límites calculados solo en entrenamiento: Sí")
print("Winsorization completada correctamente.")
