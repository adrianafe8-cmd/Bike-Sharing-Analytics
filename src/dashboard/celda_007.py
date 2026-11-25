
# ==========================================================
# DASHBOARD GLOBAL - CELDA 7
# FASE 1: Visualizaciones interactivas con Plotly
# ==========================================================

# 1. Configuración visual del dashboard

import plotly.io as pio

pio.templates.default = "plotly_white"

COLORES = {
    "principal": "#2563EB",
    "secundario": "#0D9488",
    "acento": "#F59E0B",
    "negativo": "#DC2626",
    "fondo": "#F8FAFC",
    "texto": "#1E293B"
}

# Diccionario de etiquetas para facilitar la interpretación

ETIQUETAS = {
    "temp": "Temperatura normalizada",
    "atemp": "Sensación térmica normalizada",
    "hum": "Humedad normalizada",
    "windspeed": "Velocidad del viento normalizada",
    "casual": "Alquileres casuales",
    "registered": "Alquileres registrados",
    "cnt": "Demanda total",
    "dteday": "Fecha",
    "season": "Estación",
    "weathersit": "Condición meteorológica"
}

# Copia exclusiva para visualización.
# No se modifica el dataset original.

df_visual = df.copy()

df_visual["Estacion"] = df_visual["season"].map({
    1: "Invierno",
    2: "Primavera",
    3: "Verano",
    4: "Otoño"
})

df_visual["Clima"] = df_visual["weathersit"].map({
    1: "Despejado o parcialmente nublado",
    2: "Niebla o nublado",
    3: "Lluvia o nieve ligera",
    4: "Condiciones severas"
})

df_visual["Año"] = (
    df_visual["dteday"].dt.year.astype(str)
)

# Diccionario que almacenará las figuras de la Fase 1

figuras_fase1 = {}

# ==========================================================
# 2. HISTOGRAMA DE LA DEMANDA
# ==========================================================

figuras_fase1["histograma_demanda"] = px.histogram(
    df_visual,
    x="cnt",
    nbins=30,
    marginal="box",
    title="Distribución de la demanda diaria",
    labels=ETIQUETAS,
    color_discrete_sequence=[COLORES["principal"]]
)

figuras_fase1["histograma_demanda"].add_vline(
    x=df["cnt"].mean(),
    line_dash="dash",
    line_color=COLORES["negativo"],
    annotation_text="Media"
)

# ==========================================================
# 3. BOXPLOT DE VARIABLES METEOROLÓGICAS
# ==========================================================

variables_clima = [
    "temp", "atemp", "hum", "windspeed"
]

df_clima_largo = df_visual.melt(
    value_vars=variables_clima,
    var_name="Variable",
    value_name="Valor"
)

df_clima_largo["Variable"] = (
    df_clima_largo["Variable"].map(ETIQUETAS)
)

figuras_fase1["boxplot_clima"] = px.box(
    df_clima_largo,
    x="Variable",
    y="Valor",
    color="Variable",
    points="outliers",
    title="Distribución y outliers meteorológicos"
)

figuras_fase1["boxplot_clima"].update_layout(
    showlegend=False
)

# ==========================================================
# 4. MAPAS DE CALOR DE CORRELACIONES
# ==========================================================

figuras_fase1["correlacion_pearson"] = px.imshow(
    correlacion_pearson,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Matriz de correlación de Pearson"
)

figuras_fase1["correlacion_spearman"] = px.imshow(
    correlacion_spearman,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Matriz de correlación de Spearman"
)

# ==========================================================
# 5. DIAGRAMA DE DISPERSIÓN
# ==========================================================

figuras_fase1["dispersion_temperatura"] = px.scatter(
    df_visual,
    x="temp",
    y="cnt",
    color="Año",
    hover_data=[
        "dteday",
        "hum",
        "windspeed",
        "Estacion"
    ],
    labels=ETIQUETAS,
    opacity=0.65,
    title="Relación entre temperatura y demanda"
)

# ==========================================================
# 6. DEMANDA POR ESTACIÓN
# ==========================================================

figuras_fase1["demanda_estacion"] = px.box(
    df_visual,
    x="Estacion",
    y="cnt",
    color="Estacion",
    points="outliers",
    labels=ETIQUETAS,
    category_orders={
        "Estacion": [
            "Invierno",
            "Primavera",
            "Verano",
            "Otoño"
        ]
    },
    title="Distribución de la demanda por estación"
)

figuras_fase1["demanda_estacion"].update_layout(
    showlegend=False
)

# ==========================================================
# 7. DEMANDA SEGÚN CONDICIÓN METEOROLÓGICA
# ==========================================================

demanda_clima = (
    df_visual.groupby("Clima", as_index=False)
    .agg(
        Demanda_promedio=("cnt", "mean"),
        Demanda_total=("cnt", "sum"),
        Dias_observados=("cnt", "size")
    )
    .sort_values(
        "Demanda_promedio",
        ascending=False
    )
)

figuras_fase1["demanda_clima"] = px.bar(
    demanda_clima,
    x="Clima",
    y="Demanda_promedio",
    color="Clima",
    text_auto=".0f",
    hover_data=[
        "Demanda_total",
        "Dias_observados"
    ],
    title="Demanda diaria promedio según el clima"
)

figuras_fase1["demanda_clima"].update_layout(
    showlegend=False
)

# ==========================================================
# 8. COMPARACIÓN DE OUTLIERS
# ==========================================================

df_outliers_visual = (
    df_outliers_eda.copy()
    .sort_values("Outliers", ascending=True)
)

figuras_fase1["outliers"] = px.bar(
    df_outliers_visual,
    x="Outliers",
    y="Variable",
    orientation="h",
    text="Outliers",
    hover_data=["Porcentaje"],
    color_discrete_sequence=[COLORES["acento"]],
    title="Valores atípicos detectados mediante IQR"
)

# ==========================================================
# 9. FACTORES ASOCIADOS A LA DEMANDA
# ==========================================================

df_correlacion_visual = (
    correlacion_demanda
    .reset_index()
    .melt(
        id_vars="Variable",
        var_name="Metodo",
        value_name="Correlacion"
    )
)

figuras_fase1["factores_demanda"] = px.bar(
    df_correlacion_visual,
    x="Variable",
    y="Correlacion",
    color="Metodo",
    barmode="group",
    text_auto=".3f",
    title="Correlación de factores meteorológicos"
)

figuras_fase1["factores_demanda"].add_hline(
    y=0,
    line_color="#64748B"
)

# ==========================================================
# 10. PRUEBAS DE INDEPENDENCIA CHI-CUADRADO
# ==========================================================

df_chi2_visual = df_chi2.copy()

df_chi2_visual["Relacion"] = (
    df_chi2_visual["Variable_1"]
    + " vs. "
    + df_chi2_visual["Variable_2"]
)

figuras_fase1["chi_cuadrado"] = px.bar(
    df_chi2_visual,
    x="Relacion",
    y="P_ajustado",
    color="Conclusion",
    text_auto=".3f",
    hover_data=[
        "P_valor",
        "Chi2",
        "V_Cramer",
        "Frecuencias_esperadas_validas"
    ],
    title="Pruebas Chi-cuadrado: p-valores ajustados"
)

figuras_fase1["chi_cuadrado"].add_hline(
    y=0.05,
    line_dash="dash",
    line_color=COLORES["negativo"],
    annotation_text="Significancia: 0.05"
)

# ==========================================================
# 11. CALIDAD Y COMPLETITUD DE DATOS
# ==========================================================

df_calidad_visual = df_calidad_eda.copy()

df_calidad_visual["Completitud"] = (
    100 - df_calidad_visual["Porcentaje_faltantes"]
)

figuras_fase1["calidad_datos"] = px.bar(
    df_calidad_visual,
    x="Completitud",
    y="Variable",
    orientation="h",
    text_auto=".0f",
    color_discrete_sequence=[COLORES["secundario"]],
    title="Porcentaje de completitud por variable"
)

figuras_fase1["calidad_datos"].update_xaxes(
    range=[0, 110],
    ticksuffix="%"
)

# ==========================================================
# 12. APLICAR ESTILO VISUAL UNIFICADO
# ==========================================================

for nombre, figura in figuras_fase1.items():

    figura.update_layout(
        template="plotly_white",
        font=dict(
            family="Arial",
            size=12,
            color=COLORES["texto"]
        ),
        title_font_size=17,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(
            l=45,
            r=35,
            t=70,
            b=65
        ),
        height=450,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        )
    )

# ==========================================================
# 13. GUARDAR FIGURAS INTERACTIVAS
# ==========================================================

CARPETA_GRAFICAS_F1 = FASE1 / "graficas"

CARPETA_GRAFICAS_F1.mkdir(
    parents=True,
    exist_ok=True
)

for nombre, figura in figuras_fase1.items():

    figura.write_html(
        str(CARPETA_GRAFICAS_F1 / f"{nombre}.html"),
        include_plotlyjs=True
    )

    figura.write_json(
        str(CARPETA_GRAFICAS_F1 / f"{nombre}.json")
    )

# ==========================================================
# 14. VALIDACIONES
# ==========================================================

assert len(figuras_fase1) == 11

assert all(
    len(figura.data) > 0
    for figura in figuras_fase1.values()
)

assert len(
    list(CARPETA_GRAFICAS_F1.glob("*.html"))
) == 11

assert len(
    list(CARPETA_GRAFICAS_F1.glob("*.json"))
) == 11

# ==========================================================
# 15. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 1 - VISUALIZACIONES INTERACTIVAS")
print("=" * 60)

print("\nGráficas generadas:", len(figuras_fase1))

for numero, nombre in enumerate(figuras_fase1, 1):

    print(f"{numero:02d}. {nombre}: OK")

print("\nArchivos HTML:", len(
    list(CARPETA_GRAFICAS_F1.glob("*.html"))
))

print("Archivos JSON:", len(
    list(CARPETA_GRAFICAS_F1.glob("*.json"))
))

print("\n=== DEMANDA PROMEDIO SEGÚN EL CLIMA ===")

display(demanda_clima.round(2))

print("\n=== VISTA PREVIA DE GRÁFICAS ===")

# Mostrar tres figuras para verificar su funcionamiento.

figuras_fase1["histograma_demanda"].show()

figuras_fase1["correlacion_pearson"].show()

figuras_fase1["dispersion_temperatura"].show()

print("\nFase 1 - Visualizaciones generadas correctamente.")
