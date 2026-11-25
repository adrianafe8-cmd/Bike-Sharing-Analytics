
# ==========================================================
# DASHBOARD GLOBAL - CELDA 5
# Construcción de indicadores globales (KPI)
# ==========================================================

# 1. Indicadores generales del dataset

total_registros = len(df)
total_variables = df.shape[1]

total_alquileres = int(df["cnt"].sum())

promedio_diario = df["cnt"].mean()

mediana_diaria = df["cnt"].median()

demanda_maxima = int(df["cnt"].max())

demanda_minima = int(df["cnt"].min())

fecha_maxima = df.loc[
    df["cnt"].idxmax(), "dteday"
].date()

fecha_minima = df.loc[
    df["cnt"].idxmin(), "dteday"
].date()

# 2. Indicadores de calidad de datos

total_celdas = df.size

total_faltantes = int(df.isna().sum().sum())

porcentaje_completitud = (
    1 - total_faltantes / total_celdas
) * 100

total_duplicados = int(df.duplicated().sum())

# 3. Distribución de usuarios

total_casuales = int(df["casual"].sum())

total_registrados = int(df["registered"].sum())

porcentaje_casuales = (
    total_casuales / total_alquileres
) * 100

porcentaje_registrados = (
    total_registrados / total_alquileres
) * 100

# 4. Evolución anual de la demanda

demanda_anual = (
    df.assign(Año=df["dteday"].dt.year)
    .groupby("Año", as_index=False)
    .agg(
        Alquileres=("cnt", "sum"),
        Promedio_diario=("cnt", "mean"),
        Usuarios_casuales=("casual", "sum"),
        Usuarios_registrados=("registered", "sum"),
        Dias_observados=("cnt", "size")
    )
)

demanda_2011 = demanda_anual.loc[
    demanda_anual["Año"] == 2011,
    "Alquileres"
].iloc[0]

demanda_2012 = demanda_anual.loc[
    demanda_anual["Año"] == 2012,
    "Alquileres"
].iloc[0]

crecimiento_anual = (
    (demanda_2012 / demanda_2011) - 1
) * 100

# 5. Evolución mensual de la demanda

demanda_mensual = (
    df.assign(
        Mes=df["dteday"].dt.to_period("M")
    )
    .groupby("Mes", as_index=False)
    .agg(
        Alquileres=("cnt", "sum"),
        Promedio_diario=("cnt", "mean"),
        Casuales=("casual", "sum"),
        Registrados=("registered", "sum")
    )
)

demanda_mensual["Mes"] = (
    demanda_mensual["Mes"].dt.to_timestamp()
)

# 6. Consolidar indicadores globales

kpi_globales = {
    "Registros": total_registros,
    "Variables originales": total_variables,
    "Total de alquileres": total_alquileres,
    "Promedio diario": round(promedio_diario, 2),
    "Mediana diaria": round(mediana_diaria, 2),
    "Demanda máxima diaria": demanda_maxima,
    "Fecha demanda máxima": str(fecha_maxima),
    "Demanda mínima diaria": demanda_minima,
    "Fecha demanda mínima": str(fecha_minima),
    "Completitud (%)": round(
        porcentaje_completitud, 2
    ),
    "Valores faltantes": total_faltantes,
    "Registros duplicados": total_duplicados,
    "Alquileres casuales": total_casuales,
    "Alquileres registrados": total_registrados,
    "Participación casuales (%)": round(
        porcentaje_casuales, 2
    ),
    "Participación registrados (%)": round(
        porcentaje_registrados, 2
    ),
    "Crecimiento anual (%)": round(
        crecimiento_anual, 2
    )
}

df_kpi_globales = pd.DataFrame(
    list(kpi_globales.items()),
    columns=["Indicador", "Valor"]
)

# 7. Validaciones de integridad

assert total_alquileres == (
    total_casuales + total_registrados
)

assert demanda_anual["Alquileres"].sum() == (
    total_alquileres
)

assert demanda_mensual["Alquileres"].sum() == (
    total_alquileres
)

assert len(demanda_mensual) == 24

assert np.isclose(
    porcentaje_casuales + porcentaje_registrados,
    100
)

# 8. Guardar resultados para el dashboard

df_kpi_globales.to_csv(
    RESULTADOS / "kpi_globales.csv",
    index=False
)

demanda_anual.to_csv(
    RESULTADOS / "demanda_anual.csv",
    index=False
)

demanda_mensual.to_csv(
    RESULTADOS / "demanda_mensual.csv",
    index=False
)

# 9. Presentar resultados

print("=" * 60)
print("DASHBOARD GLOBAL - INDICADORES PRINCIPALES")
print("=" * 60)

display(df_kpi_globales)

print("\n=== EVOLUCIÓN ANUAL DE LA DEMANDA ===")

display(demanda_anual.round(2))

print("\n=== EVOLUCIÓN MENSUAL DE LA DEMANDA ===")

display(demanda_mensual.round(2))

print("\n=== VALIDACIONES ===")

print("Integridad de alquileres: OK")
print("Consolidación anual: OK")
print("Consolidación mensual: OK")
print("Distribución de usuarios: OK")

print("\nIndicadores globales generados correctamente.")
