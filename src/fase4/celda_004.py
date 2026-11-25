
# ==========================================================
# FASE 4 - CELDA 3
# Diagnóstico inicial de calidad de datos
# ==========================================================

# Crear una copia para preservar los datos originales
df_limpio = df.copy()

# Convertir la fecha al tipo datetime
df_limpio["dteday"] = pd.to_datetime(
    df_limpio["dteday"],
    errors="coerce"
)

# Ordenar cronológicamente
df_limpio = (
    df_limpio
    .sort_values("dteday")
    .reset_index(drop=True)
)

# Tabla de diagnóstico por variable
diagnostico = pd.DataFrame({
    "Tipo_dato": df_limpio.dtypes.astype(str),
    "Valores_validos": df_limpio.notna().sum(),
    "Valores_faltantes": df_limpio.isna().sum(),
    "Porcentaje_faltantes": (
        df_limpio.isna().mean() * 100
    ),
    "Valores_unicos": df_limpio.nunique()
})

print("=== DIAGNÓSTICO POR VARIABLE ===")
display(diagnostico.round(2))

# Identificar registros duplicados
duplicados = df_limpio.duplicated().sum()

# Identificar fechas duplicadas
fechas_duplicadas = (
    df_limpio["dteday"].duplicated().sum()
)

# Identificar valores infinitos
columnas_numericas = df_limpio.select_dtypes(
    include=np.number
)

infinitos = np.isinf(
    columnas_numericas.to_numpy()
).sum()

# Total de valores faltantes
total_faltantes = (
    df_limpio.isna().sum().sum()
)

# Verificar consistencia de la variable objetivo
inconsistencias_cnt = (
    df_limpio["cnt"] !=
    df_limpio["casual"] + df_limpio["registered"]
).sum()

# Verificar continuidad temporal
fechas_esperadas = pd.date_range(
    start=df_limpio["dteday"].min(),
    end=df_limpio["dteday"].max(),
    freq="D"
)

fechas_faltantes = fechas_esperadas.difference(
    df_limpio["dteday"]
)

# Resumen general
print("\n=== RESUMEN DE CALIDAD ===")
print("Total de registros:", len(df_limpio))
print("Valores faltantes:", total_faltantes)
print("Registros duplicados:", duplicados)
print("Fechas duplicadas:", fechas_duplicadas)
print("Valores infinitos:", infinitos)
print("Fechas faltantes:", len(fechas_faltantes))
print("Inconsistencias en cnt:", inconsistencias_cnt)

print("\n=== COBERTURA TEMPORAL ===")
print("Fecha inicial:", df_limpio["dteday"].min())
print("Fecha final:", df_limpio["dteday"].max())

print("\nDiagnóstico de calidad completado.")
