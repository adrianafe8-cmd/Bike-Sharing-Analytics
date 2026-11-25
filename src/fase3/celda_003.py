
# ==========================================================
# FASE 3 - CELDA 3
# Validación y control de calidad
# ==========================================================

# Copia de trabajo para no modificar los datos originales
df_modelo = df.copy()

# Convertir fecha y ordenar cronológicamente
df_modelo["dteday"] = pd.to_datetime(
    df_modelo["dteday"]
)

df_modelo = (
    df_modelo
    .sort_values("dteday")
    .reset_index(drop=True)
)

# Diagnóstico de calidad
print("Dimensiones:", df_modelo.shape)
print("Valores faltantes:", df_modelo.isna().sum().sum())
print("Fechas duplicadas:", df_modelo["dteday"].duplicated().sum())

print(
    "Periodo:",
    df_modelo["dteday"].min().date(),
    "a",
    df_modelo["dteday"].max().date()
)

print(
    "Promedio de alquileres:",
    round(df_modelo["cnt"].mean(), 2)
)

# Validaciones automáticas
assert df_modelo.shape == (731, 16)
assert df_modelo.isna().sum().sum() == 0
assert df_modelo["dteday"].duplicated().sum() == 0
assert (df_modelo["cnt"] == (
    df_modelo["casual"] + df_modelo["registered"]
)).all()

print("Validación de calidad superada.")
