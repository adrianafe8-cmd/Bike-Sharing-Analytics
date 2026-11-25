
# ==========================================================
# FASE 4 - CELDA 6
# Análisis detallado y decisión de tratamiento de outliers
# ==========================================================

variables_tratamiento = [
    "hum",
    "windspeed"
]

detalle_outliers = []

for variable in variables_tratamiento:

    # Recuperar los límites IQR del diagnóstico descriptivo
    fila = tabla_outliers.loc[
        tabla_outliers["Variable"] == variable
    ].iloc[0]

    limite_inferior = fila["Limite_inferior"]
    limite_superior = fila["Limite_superior"]

    # Identificar observaciones atípicas
    mascara = (
        (df_limpio[variable] < limite_inferior) |
        (df_limpio[variable] > limite_superior)
    )

    # Recuperar información contextual
    casos = df_limpio.loc[
        mascara,
        [
            "dteday",
            "season",
            "weathersit",
            "temp",
            "hum",
            "windspeed",
            "cnt"
        ]
    ].copy()

    casos.insert(
        0,
        "Variable_atipica",
        variable
    )

    detalle_outliers.append(casos)

# Consolidar observaciones identificadas
tabla_detalle_outliers = pd.concat(
    detalle_outliers,
    ignore_index=True
)

print("=== DETALLE DE VALORES ATÍPICOS ===")

display(tabla_detalle_outliers.round(4))

# Verificar rangos de variables normalizadas
print("\n=== RANGOS OBSERVADOS ===")

display(
    df_limpio[variables_tratamiento]
    .agg(["min", "max", "mean", "median"])
    .round(4)
)

# Documentar estrategia seleccionada
estrategia_outliers = pd.DataFrame([
    {
        "Variable": "temp",
        "Tratamiento": "Conservar"
    },
    {
        "Variable": "atemp",
        "Tratamiento": "Conservar"
    },
    {
        "Variable": "hum",
        "Tratamiento": "Winsorization P1-P99"
    },
    {
        "Variable": "windspeed",
        "Tratamiento": "Winsorization P1-P99"
    },
    {
        "Variable": "cnt",
        "Tratamiento": "Conservar"
    }
])

print("\n=== ESTRATEGIA DE TRATAMIENTO ===")

display(estrategia_outliers)

# Guardar evidencias
tabla_detalle_outliers.to_csv(
    RESULTADOS / "detalle_outliers.csv",
    index=False
)

estrategia_outliers.to_csv(
    RESULTADOS / "estrategia_outliers.csv",
    index=False
)

# Verificar que los datos originales siguen intactos
assert df_limpio.shape == (731, 16)

assert df_limpio[
    variables_tratamiento
].ge(0).all().all()

assert df_limpio[
    variables_tratamiento
].le(1).all().all()

print("\nRegistros conservados:", len(df_limpio))

print(
    "Tratamiento seleccionado:",
    "Winsorization P1-P99"
)

print(
    "Estado: pendiente de aplicación "
    "después de la partición de datos."
)

print("\nAnálisis detallado completado.")
