# ==========================================================
# DASHBOARD GLOBAL - CELDA 18
# Complementos académicos de la Fase 1
# ==========================================================

import pandas as pd
import numpy as np
import zipfile
from scipy.stats import zscore

# ==========================================================
# 1. FORMULACIÓN DEL PROBLEMA
# ==========================================================

contexto_fase1 = """
Los sistemas de bicicletas compartidas requieren una
planificación eficiente de sus recursos para responder
a las variaciones de la demanda.

La demanda de alquileres puede estar asociada con factores
meteorológicos, estacionales y temporales. Comprender estas
relaciones permite apoyar la planificación operativa,
la disponibilidad de bicicletas y la toma de decisiones
basada en datos.

El proyecto analiza 731 observaciones diarias del sistema
Capital Bikeshare durante los años 2011 y 2012.
"""

preguntas_fase1 = pd.DataFrame([
    {
        "Tipo": "Principal",
        "Pregunta": (
            "¿Cómo se relacionan las condiciones "
            "meteorológicas y temporales con la demanda "
            "diaria de bicicletas compartidas?"
        )
    },
    {
        "Tipo": "Secundaria 1",
        "Pregunta": (
            "¿Qué patrones temporales y estacionales "
            "presenta la demanda durante 2011 y 2012?"
        )
    },
    {
        "Tipo": "Secundaria 2",
        "Pregunta": (
            "¿Qué variables meteorológicas presentan "
            "mayor asociación estadística con la demanda?"
        )
    },
    {
        "Tipo": "Secundaria 3",
        "Pregunta": (
            "¿Qué problemas de calidad y valores atípicos "
            "deben considerarse antes del modelado?"
        )
    }
])

# ==========================================================
# 2. OBJETIVOS DE INVESTIGACIÓN
# ==========================================================

objetivo_general_fase1 = """
Caracterizar la demanda diaria de bicicletas compartidas
durante 2011 y 2012 mediante técnicas de análisis
exploratorio, estadística descriptiva y evaluación de
calidad de datos, con el propósito de establecer una base
analítica para las fases posteriores de modelado predictivo.
"""

df_objetivos_fase1 = pd.DataFrame([
    {
        "Objetivo": "Específico 1",
        "Descripcion": (
            "Caracterizar las 731 observaciones y las "
            "16 variables originales mediante estadísticas "
            "descriptivas, frecuencias y visualizaciones "
            "durante la Fase 1."
        ),
        "Indicador": "16 variables caracterizadas",
        "Plazo": "Finalización de la Fase 1"
    },
    {
        "Objetivo": "Específico 2",
        "Descripcion": (
            "Cuantificar la asociación entre las variables "
            "meteorológicas y la demanda mediante Pearson, "
            "Spearman y pruebas exploratorias Chi-cuadrado."
        ),
        "Indicador": (
            "2 matrices de correlación y 4 pruebas "
            "Chi-cuadrado"
        ),
        "Plazo": "Finalización de la Fase 1"
    },
    {
        "Objetivo": "Específico 3",
        "Descripcion": (
            "Evaluar la calidad de las 731 observaciones "
            "mediante la identificación de valores "
            "faltantes, duplicados, inconsistencias y "
            "outliers utilizando IQR y Z-score."
        ),
        "Indicador": (
            "100 % de los registros evaluados y "
            "2 métodos de detección de outliers"
        ),
        "Plazo": "Antes del modelado predictivo"
    }
])

# ==========================================================
# 3. RECUPERAR DOCUMENTACIÓN ORIGINAL DEL DATASET
# ==========================================================

with zipfile.ZipFile(RUTA_ZIP, "r") as archivo_zip:

    archivos_readme = [
        nombre
        for nombre in archivo_zip.namelist()
        if "readme" in nombre.lower()
    ]

    assert archivos_readme, (
        "No se encontró la documentación original."
    )

    readme_dataset = archivo_zip.read(
        archivos_readme[0]
    ).decode("utf-8", errors="replace")

print("=== DOCUMENTACIÓN ORIGINAL DEL DATASET ===")
print(readme_dataset)

# ==========================================================
# 4. FICHA TÉCNICA
# ==========================================================

df_ficha_tecnica = pd.DataFrame([
    ("Nombre", "Bike Sharing Dataset"),
    ("Repositorio", "UCI Machine Learning Repository"),
    ("Autor", "Hadi Fanaee-T"),
    ("DOI", "10.24432/C5W894"),
    (
        "URL del repositorio",
        "https://archive.ics.uci.edu/dataset/275/"
        "bike+sharing+dataset"
    ),
    ("URL de descarga", URL_DATASET),
    ("Archivo analizado", "day.csv"),
    ("Formato", "CSV"),
    ("Registros", str(len(df))),
    ("Variables", str(df.shape[1])),
    ("Granularidad", "Diaria"),
    (
        "Periodo inicial",
        str(df["dteday"].min().date())
    ),
    (
        "Periodo final",
        str(df["dteday"].max().date())
    ),
    ("Variable objetivo", "cnt"),
    (
        "Fecha de extracción",
        "Pendiente de confirmar fecha original"
    ),
    (
        "Licencia",
        "Pendiente de verificación en el repositorio UCI"
    ),
    ("Valores faltantes", str(df.isna().sum().sum())),
    ("Duplicados", str(df.duplicated().sum())),
    (
        "Procedencia del análisis",
        "EDA reconstruido desde el dataset original"
    )
], columns=["Campo", "Valor"])

# ==========================================================
# 5. DICCIONARIO DE DATOS
# ==========================================================

def rango_observado(variable):

    return (
        f"{df[variable].min()} — "
        f"{df[variable].max()}"
    )


df_diccionario_fase1 = pd.DataFrame([
    (
        "instant",
        "Identificador",
        "Índice único del registro",
        rango_observado("instant")
    ),
    (
        "dteday",
        "Temporal",
        "Fecha de observación",
        "2011-01-01 a 2012-12-31"
    ),
    (
        "season",
        "Cualitativa nominal",
        "Estación del año codificada",
        "1, 2, 3, 4"
    ),
    (
        "yr",
        "Cualitativa ordinal",
        "Año de observación",
        "0: 2011; 1: 2012"
    ),
    (
        "mnth",
        "Cualitativa ordinal cíclica",
        "Mes del año",
        "1 a 12"
    ),
    (
        "holiday",
        "Cualitativa nominal binaria",
        "Indicador de día festivo",
        "0: No; 1: Sí"
    ),
    (
        "weekday",
        "Cualitativa nominal cíclica",
        "Día de la semana",
        "0 a 6"
    ),
    (
        "workingday",
        "Cualitativa nominal binaria",
        "Día laboral, excluye festivos y fines de semana",
        "0: No; 1: Sí"
    ),
    (
        "weathersit",
        "Cualitativa ordinal",
        "Categoría de condiciones meteorológicas",
        "1 a 4; observadas: 1, 2 y 3"
    ),
    (
        "temp",
        "Cuantitativa continua",
        "Temperatura normalizada",
        rango_observado("temp")
    ),
    (
        "atemp",
        "Cuantitativa continua",
        "Sensación térmica normalizada",
        rango_observado("atemp")
    ),
    (
        "hum",
        "Cuantitativa continua",
        "Humedad relativa normalizada",
        rango_observado("hum")
    ),
    (
        "windspeed",
        "Cuantitativa continua",
        "Velocidad del viento normalizada",
        rango_observado("windspeed")
    ),
    (
        "casual",
        "Cuantitativa discreta",
        "Alquileres de usuarios casuales",
        rango_observado("casual")
    ),
    (
        "registered",
        "Cuantitativa discreta",
        "Alquileres de usuarios registrados",
        rango_observado("registered")
    ),
    (
        "cnt",
        "Cuantitativa discreta",
        "Total diario de alquileres; variable objetivo",
        rango_observado("cnt")
    )
], columns=[
    "Variable",
    "Tipo",
    "Descripcion",
    "Rango_o_valores"
])

# ==========================================================
# 6. DETECCIÓN DE OUTLIERS MEDIANTE Z-SCORE
# ==========================================================

# Se utiliza un umbral convencional de |Z| > 3.
# El análisis es descriptivo y no modifica el dataset.

UMBRAL_Z = 3

resultados_zscore = []
detalle_zscore = []

for variable in variables_cuantitativas:

    valores = df[variable].astype(float)

    if valores.std(ddof=0) == 0:

        puntuaciones = np.zeros(len(valores))

    else:

        puntuaciones = zscore(
            valores,
            ddof=0,
            nan_policy="omit"
        )

    mascara = np.abs(puntuaciones) > UMBRAL_Z

    cantidad = int(mascara.sum())

    resultados_zscore.append({
        "Variable": variable,
        "Outliers_Zscore": cantidad,
        "Porcentaje_Zscore": (
            cantidad / len(df) * 100
        ),
        "Umbral": UMBRAL_Z
    })

    for posicion in np.flatnonzero(mascara):

        detalle_zscore.append({
            "Variable": variable,
            "Fecha": df["dteday"].iloc[posicion],
            "Valor": valores.iloc[posicion],
            "Zscore": float(puntuaciones[posicion])
        })

df_zscore_fase1 = pd.DataFrame(resultados_zscore)

df_detalle_zscore = pd.DataFrame(
    detalle_zscore,
    columns=["Variable", "Fecha", "Valor", "Zscore"]
)

# ==========================================================
# 7. COMPARACIÓN IQR VS Z-SCORE
# ==========================================================

df_comparacion_outliers = (
    df_outliers_eda[
        ["Variable", "Outliers", "Porcentaje"]
    ]
    .rename(columns={
        "Outliers": "Outliers_IQR",
        "Porcentaje": "Porcentaje_IQR"
    })
    .merge(
        df_zscore_fase1,
        on="Variable",
        how="inner",
        validate="one_to_one"
    )
)

df_outliers_largo = df_comparacion_outliers.melt(
    id_vars="Variable",
    value_vars=[
        "Outliers_IQR",
        "Outliers_Zscore"
    ],
    var_name="Metodo",
    value_name="Cantidad"
)

df_outliers_largo["Metodo"] = (
    df_outliers_largo["Metodo"].map({
        "Outliers_IQR": "IQR",
        "Outliers_Zscore": "Z-score"
    })
)

fig_comparacion_outliers = px.bar(
    df_outliers_largo,
    x="Variable",
    y="Cantidad",
    color="Metodo",
    barmode="group",
    text="Cantidad",
    title="Comparación de outliers: IQR vs Z-score",
    color_discrete_map={
        "IQR": "#2563EB",
        "Z-score": "#0D9488"
    },
    template="plotly_white"
)

fig_comparacion_outliers.update_layout(
    height=450,
    xaxis_title="Variable",
    yaxis_title="Cantidad de valores atípicos",
    legend_title_text="Método"
)

fig_comparacion_outliers.update_traces(
    textposition="outside"
)

# ==========================================================
# 8. EXPORTAR COMPLEMENTOS ACADÉMICOS
# ==========================================================

complementos_fase1 = {
    "preguntas_investigacion": preguntas_fase1,
    "objetivos_smart": df_objetivos_fase1,
    "ficha_tecnica": df_ficha_tecnica,
    "diccionario_datos": df_diccionario_fase1,
    "outliers_zscore": df_zscore_fase1,
    "detalle_zscore": df_detalle_zscore,
    "comparacion_outliers": df_comparacion_outliers
}

for nombre, tabla in complementos_fase1.items():

    tabla.to_csv(
        FASE1 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

(FASE1 / "formulacion_problema.txt").write_text(
    contexto_fase1,
    encoding="utf-8"
)

(FASE1 / "objetivo_general.txt").write_text(
    objetivo_general_fase1,
    encoding="utf-8"
)

(FASE1 / "documentacion_original.txt").write_text(
    readme_dataset,
    encoding="utf-8"
)

fig_comparacion_outliers.write_html(
    CARPETA_GRAFICAS_F1 / "comparacion_outliers.html"
)

fig_comparacion_outliers.write_json(
    CARPETA_GRAFICAS_F1 / "comparacion_outliers.json"
)

# ==========================================================
# 9. VALIDACIONES
# ==========================================================

assert len(df_diccionario_fase1) == 16

assert set(df_diccionario_fase1["Variable"]) == set(df.columns)

assert len(preguntas_fase1) == 4

assert len(df_objetivos_fase1) == 3

assert len(df_zscore_fase1) == len(variables_cuantitativas)

assert len(df_comparacion_outliers) == len(variables_cuantitativas)

assert len(df) == 731

assert int(df["cnt"].sum()) == total_alquileres

assert all(
    (FASE1 / f"{nombre}.csv").exists()
    for nombre in complementos_fase1
)

# ==========================================================
# 10. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 1 - COMPLEMENTOS ACADÉMICOS")
print("=" * 60)

print("\n=== FICHA TÉCNICA ===")
print(df_ficha_tecnica.to_string(index=False))

print("\n=== DICCIONARIO DE DATOS ===")
print(df_diccionario_fase1.to_string(index=False))

print("\n=== COMPARACIÓN IQR VS Z-SCORE ===")
print(
    df_comparacion_outliers.round(4)
    .to_string(index=False)
)

print("\n=== DETALLE DE OUTLIERS Z-SCORE ===")
print(df_detalle_zscore.to_string(index=False))

print("\n=== VALIDACIONES ===")
print("Preguntas de investigación: 4 - OK")
print("Objetivo general: 1 - OK")
print("Objetivos específicos SMART: 3 - OK")
print("Diccionario de variables: 16/16 - OK")
print("Detección mediante IQR: OK")
print("Detección mediante Z-score: OK")
print("Integridad del dataset: OK")
print("Archivos CSV generados: 7")
print("Modelos reentrenados: 0")

print("\nPendiente: verificar licencia y fecha de extracción.")
print("Pendiente: integrar complementos en la interfaz Dash.")

fig_comparacion_outliers.show()