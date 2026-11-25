
# ==========================================================
# DASHBOARD GLOBAL - CELDA 6
# FASE 1: Análisis Exploratorio de Datos (EDA)
# ==========================================================

from scipy.stats import chi2_contingency
from itertools import combinations

# 1. Clasificación de variables según su naturaleza

variables_cuantitativas = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "casual",
    "registered",
    "cnt"
]

variables_cualitativas = [
    "season",
    "yr",
    "mnth",
    "holiday",
    "weekday",
    "workingday",
    "weathersit"
]

# instant es un identificador.
# dteday es una variable temporal.
# Se excluyen de las estadísticas cuantitativas.

# ==========================================================
# 2. ANÁLISIS UNIVARIADO CUANTITATIVO
# ==========================================================

datos_numericos = df[variables_cuantitativas]

estadisticas_eda = pd.DataFrame({
    "Observaciones": datos_numericos.count(),
    "Media": datos_numericos.mean(),
    "Mediana": datos_numericos.median(),
    "Moda": datos_numericos.mode().iloc[0],
    "Desviacion_estandar": datos_numericos.std(),
    "Varianza": datos_numericos.var(),
    "Minimo": datos_numericos.min(),
    "Maximo": datos_numericos.max(),
    "Rango": (
        datos_numericos.max() -
        datos_numericos.min()
    ),
    "Q1": datos_numericos.quantile(0.25),
    "Q3": datos_numericos.quantile(0.75),
    "IQR": (
        datos_numericos.quantile(0.75) -
        datos_numericos.quantile(0.25)
    ),
    "Asimetria": datos_numericos.skew(),
    "Curtosis": datos_numericos.kurt()
})

estadisticas_eda.index.name = "Variable"

estadisticas_eda = (
    estadisticas_eda.reset_index()
)

# ==========================================================
# 3. ANÁLISIS UNIVARIADO CUALITATIVO
# ==========================================================

frecuencias = []

for variable in variables_cualitativas:

    conteos = (
        df[variable]
        .value_counts()
        .sort_index()
    )

    for categoria, cantidad in conteos.items():

        frecuencias.append({
            "Variable": variable,
            "Categoria": categoria,
            "Frecuencia": int(cantidad),
            "Porcentaje": round(
                cantidad / len(df) * 100, 4
            )
        })

df_frecuencias = pd.DataFrame(frecuencias)

# ==========================================================
# 4. ANÁLISIS DE CORRELACIONES
# ==========================================================

correlacion_pearson = (
    datos_numericos.corr(method="pearson")
)

correlacion_spearman = (
    datos_numericos.corr(method="spearman")
)

# Correlaciones de factores meteorológicos
# con la demanda total.

correlacion_demanda = pd.DataFrame({
    "Pearson": correlacion_pearson["cnt"],
    "Spearman": correlacion_spearman["cnt"]
})

correlacion_demanda = (
    correlacion_demanda
    .drop(index=["cnt", "casual", "registered"])
    .sort_values("Pearson", ascending=False)
)

# ==========================================================
# 5. PRUEBAS DE INDEPENDENCIA CHI-CUADRADO
# ==========================================================

# Se seleccionan pares con relevancia para el dominio.
# No se prueban relaciones deterministas del calendario,
# como mes frente a estación.

pares_chi2 = [
    ("season", "weathersit"),
    ("workingday", "weathersit"),
    ("yr", "weathersit"),
    ("weekday", "weathersit")
]

resultados_chi2 = []

for variable_1, variable_2 in pares_chi2:

    tabla_contingencia = pd.crosstab(
        df[variable_1],
        df[variable_2]
    )

    chi2, p_valor, gl, esperadas = (
        chi2_contingency(
            tabla_contingencia,
            correction=False
        )
    )

    n = tabla_contingencia.to_numpy().sum()

    filas, columnas = tabla_contingencia.shape

    # V de Cramér: magnitud de la asociación.

    v_cramer = np.sqrt(
        chi2 / (
            n * min(filas - 1, columnas - 1)
        )
    )

    porcentaje_esperadas_menores_5 = (
        np.mean(esperadas < 5) * 100
    )

    supuestos_validos = (
        esperadas.min() >= 1
        and porcentaje_esperadas_menores_5 <= 20
    )

    resultados_chi2.append({
        "Variable_1": variable_1,
        "Variable_2": variable_2,
        "Chi2": chi2,
        "Grados_libertad": gl,
        "P_valor": p_valor,
        "V_Cramer": v_cramer,
        "Esperada_minima": esperadas.min(),
        "Esperadas_menores_5_pct":
            porcentaje_esperadas_menores_5,
        "Frecuencias_esperadas_validas":
            supuestos_validos
    })

df_chi2 = pd.DataFrame(resultados_chi2)

# Corrección de Bonferroni por pruebas múltiples.

df_chi2["P_ajustado"] = (
    df_chi2["P_valor"] * len(pares_chi2)
).clip(upper=1)

df_chi2["Conclusion"] = np.where(
    ~df_chi2["Frecuencias_esperadas_validas"],
    "Interpretar con precaución",
    np.where(
        df_chi2["P_ajustado"] < 0.05,
        "Evidencia de asociación",
        "No se rechaza independencia"
    )
)

# ==========================================================
# 6. DETECCIÓN DE OUTLIERS MEDIANTE IQR
# ==========================================================

resultados_outliers = []

for variable in variables_cuantitativas:

    q1 = df[variable].quantile(0.25)
    q3 = df[variable].quantile(0.75)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    mascara = (
        (df[variable] < limite_inferior) |
        (df[variable] > limite_superior)
    )

    cantidad = int(mascara.sum())

    resultados_outliers.append({
        "Variable": variable,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Limite_inferior": limite_inferior,
        "Limite_superior": limite_superior,
        "Outliers": cantidad,
        "Porcentaje": cantidad / len(df) * 100
    })

df_outliers_eda = pd.DataFrame(
    resultados_outliers
)

# ==========================================================
# 7. DIAGNÓSTICO DE CALIDAD POR VARIABLE
# ==========================================================

df_calidad_eda = pd.DataFrame({
    "Variable": df.columns,
    "Tipo_dato": df.dtypes.astype(str).values,
    "Valores_faltantes": df.isna().sum().values,
    "Porcentaje_faltantes": (
        df.isna().mean().values * 100
    ),
    "Valores_unicos": df.nunique().values
})

# ==========================================================
# 8. VALIDACIONES DE INTEGRIDAD
# ==========================================================

assert len(df) == 731
assert df.shape[1] == 16

assert len(estadisticas_eda) == 7

assert (
    df_frecuencias.groupby("Variable")
    ["Frecuencia"].sum() == len(df)
).all()

assert len(df_calidad_eda) == 16

assert np.isfinite(
    correlacion_pearson.to_numpy()
).all()

assert np.isfinite(
    correlacion_spearman.to_numpy()
).all()

# ==========================================================
# 9. GUARDAR RESULTADOS DE LA FASE 1
# ==========================================================

FASE1 = RESULTADOS / "Fase_1"
FASE1.mkdir(parents=True, exist_ok=True)

tablas_fase1 = {
    "estadisticas_descriptivas": estadisticas_eda,
    "frecuencias_categoricas": df_frecuencias,
    "pruebas_chi2": df_chi2,
    "outliers_eda": df_outliers_eda,
    "calidad_datos": df_calidad_eda
}

for nombre, tabla in tablas_fase1.items():

    tabla.to_csv(
        FASE1 / f"{nombre}.csv",
        index=False
    )

correlacion_pearson.to_csv(
    FASE1 / "correlacion_pearson.csv"
)

correlacion_spearman.to_csv(
    FASE1 / "correlacion_spearman.csv"
)

correlacion_demanda.to_csv(
    FASE1 / "correlacion_demanda.csv"
)

# ==========================================================
# 10. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 1 - ANÁLISIS EXPLORATORIO DE DATOS")
print("=" * 60)

print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
display(estadisticas_eda.round(4))

print("\n=== FRECUENCIAS CATEGÓRICAS ===")
display(df_frecuencias)

print("\n=== CORRELACIÓN DE PEARSON ===")
display(correlacion_pearson.round(4))

print("\n=== CORRELACIÓN DE SPEARMAN ===")
display(correlacion_spearman.round(4))

print("\n=== FACTORES ASOCIADOS A LA DEMANDA ===")
display(correlacion_demanda.round(4))

print("\n=== PRUEBAS CHI-CUADRADO ===")
display(df_chi2.round(6))

print("\n=== DETECCIÓN DE OUTLIERS ===")
display(df_outliers_eda.round(4))

print("\n=== CALIDAD DE DATOS ===")
display(df_calidad_eda)

print("\n=== VALIDACIONES ===")
print("Estadísticas descriptivas: OK")
print("Frecuencias categóricas: OK")
print("Matrices de correlación: OK")
print("Integridad del dataset: OK")

print("\nArchivos generados:",
      len(list(FASE1.glob("*.csv"))))

print("Fase 1 - Resultados EDA generados correctamente.")
