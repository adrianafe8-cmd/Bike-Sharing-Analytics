# ==========================================================
# DASHBOARD GLOBAL - CELDA 9
# FASE 2: Consolidación y visualizaciones
# ==========================================================

import base64
import re

# ==========================================================
# 1. EXTRAER MÉTRICAS DESDE LAS SALIDAS ORIGINALES
# ==========================================================

def recuperar_texto_f2(numero_celda):

    return "\n".join(
        df_salidas_f2.loc[
            df_salidas_f2["Celda"] == numero_celda,
            "Resultado"
        ].tolist()
    )

texto_validacion_f2 = recuperar_texto_f2(19)
texto_prueba_f2 = recuperar_texto_f2(21)
texto_r_f2 = recuperar_texto_f2(30)

# Extraer resultados de regresión mediante expresiones
# regulares, evitando introducir métricas manualmente.

numero = r"(-?\d+(?:\.\d+)?)"

patron_modelos = (
    r"(Regresión lineal (?:simple|múltiple))"
    + r"\s+" + numero
    + r"\s+" + numero
    + r"\s+" + numero
)

coincidencias_modelos = re.findall(
    patron_modelos,
    texto_validacion_f2
)

assert len(coincidencias_modelos) == 2, (
    "No se recuperaron los dos modelos de validación."
)

df_validacion_f2 = pd.DataFrame(
    coincidencias_modelos,
    columns=["Modelo", "MAE", "RMSE", "R2"]
)

for columna in ["MAE", "RMSE", "R2"]:

    df_validacion_f2[columna] = (
        df_validacion_f2[columna].astype(float)
    )

# Recuperar evaluación final del modelo seleccionado.

patron_evaluacion = (
    r"(Validación|Prueba)"
    + r"\s+" + numero
    + r"\s+" + numero
    + r"\s+" + numero
)

coincidencias_evaluacion = re.findall(
    patron_evaluacion,
    texto_prueba_f2
)

assert len(coincidencias_evaluacion) == 2

df_evaluacion_f2 = pd.DataFrame(
    coincidencias_evaluacion,
    columns=["Conjunto", "MAE", "RMSE", "R2"]
)

for columna in ["MAE", "RMSE", "R2"]:

    df_evaluacion_f2[columna] = (
        df_evaluacion_f2[columna].astype(float)
    )

# ==========================================================
# 2. IDENTIFICAR EL MODELO SELECCIONADO
# ==========================================================

modelo_seleccionado_f2 = (
    df_validacion_f2.loc[
        df_validacion_f2["MAE"].idxmin(),
        "Modelo"
    ]
)

mae_simple_f2 = df_validacion_f2.loc[
    df_validacion_f2["Modelo"] ==
    "Regresión lineal simple",
    "MAE"
].iloc[0]

mae_multiple_f2 = df_validacion_f2.loc[
    df_validacion_f2["Modelo"] ==
    "Regresión lineal múltiple",
    "MAE"
].iloc[0]

mejora_mae_f2 = (
    1 - mae_multiple_f2 / mae_simple_f2
) * 100

metricas_test_f2 = (
    df_evaluacion_f2
    .set_index("Conjunto")
    .loc["Prueba"]
)

# ==========================================================
# 3. RECUPERAR RESULTADOS COMPLEMENTARIOS DE R
# ==========================================================

r2_r = re.search(
    r"Multiple R-squared:\s*([\d.]+)",
    texto_r_f2
)

r2_ajustado_r = re.search(
    r"Adjusted R-squared:\s*([\d.]+)",
    texto_r_f2
)

diferencia_r_python = re.search(
    r"Diferencia máxima R vs Python:\s*"
    r"([\d.eE+-]+)",
    texto_r_f2
)

singularidades_r = re.search(
    r"(\d+) not defined because of singularities",
    texto_r_f2
)

assert all([
    r2_r,
    r2_ajustado_r,
    diferencia_r_python,
    singularidades_r
]), "No se recuperaron todos los resultados de R."

df_resultados_r_f2 = pd.DataFrame({
    "Indicador": [
        "R2 entrenamiento R",
        "R2 ajustado entrenamiento R",
        "Diferencia máxima R vs Python",
        "Coeficientes no estimables"
    ],
    "Valor": [
        float(r2_r.group(1)),
        float(r2_ajustado_r.group(1)),
        float(diferencia_r_python.group(1)),
        int(singularidades_r.group(1))
    ]
})

# ==========================================================
# 4. PARTICIÓN CRONOLÓGICA
# ==========================================================

# Recuperar tamaños desde el resumen reproducible.

texto_resumen_f2 = recuperar_texto_f2(32)

particion_f2 = re.search(
    r"Partición:\s*(\d+)\s+entrenamiento,\s*"
    r"(\d+)\s+validación,\s*(\d+)\s+prueba",
    texto_resumen_f2
)

assert particion_f2 is not None

df_particion_f2 = pd.DataFrame({
    "Conjunto": [
        "Entrenamiento",
        "Validación",
        "Prueba"
    ],
    "Registros": [
        int(particion_f2.group(1)),
        int(particion_f2.group(2)),
        int(particion_f2.group(3))
    ]
})

df_particion_f2["Porcentaje"] = (
    df_particion_f2["Registros"]
    / df_particion_f2["Registros"].sum()
    * 100
)

# ==========================================================
# 5. VISUALIZACIONES INTERACTIVAS
# ==========================================================

figuras_fase2 = {}

# 5.1 Comparación de errores en validación

df_errores_f2 = df_validacion_f2.melt(
    id_vars="Modelo",
    value_vars=["MAE", "RMSE"],
    var_name="Metrica",
    value_name="Valor"
)

figuras_fase2["comparacion_modelos"] = px.bar(
    df_errores_f2,
    x="Modelo",
    y="Valor",
    color="Metrica",
    barmode="group",
    text_auto=".2f",
    title="Comparación de modelos en validación",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# 5.2 Comparación del coeficiente R2

figuras_fase2["comparacion_r2"] = px.bar(
    df_validacion_f2,
    x="Modelo",
    y="R2",
    color="Modelo",
    text_auto=".4f",
    title="Coeficiente R² en validación"
)

figuras_fase2["comparacion_r2"].add_hline(
    y=0,
    line_dash="dash",
    line_color=COLORES["negativo"]
)

figuras_fase2["comparacion_r2"].update_layout(
    showlegend=False
)

# 5.3 Desempeño del modelo seleccionado

df_evaluacion_largo_f2 = df_evaluacion_f2.melt(
    id_vars="Conjunto",
    value_vars=["MAE", "RMSE"],
    var_name="Metrica",
    value_name="Valor"
)

figuras_fase2["evaluacion_final"] = px.bar(
    df_evaluacion_largo_f2,
    x="Conjunto",
    y="Valor",
    color="Metrica",
    barmode="group",
    text_auto=".2f",
    title="Regresión múltiple: validación y prueba",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"]
    ]
)

# 5.4 R2 del modelo seleccionado

figuras_fase2["r2_evaluacion"] = px.bar(
    df_evaluacion_f2,
    x="Conjunto",
    y="R2",
    color="Conjunto",
    text_auto=".4f",
    title="Regresión múltiple: evolución del R²"
)

figuras_fase2["r2_evaluacion"].add_hline(
    y=0,
    line_dash="dash",
    line_color=COLORES["negativo"]
)

figuras_fase2["r2_evaluacion"].update_layout(
    showlegend=False
)

# 5.5 Distribución de los conjuntos

figuras_fase2["particion_datos"] = px.pie(
    df_particion_f2,
    names="Conjunto",
    values="Registros",
    hole=0.55,
    title="Partición cronológica del dataset",
    color_discrete_sequence=[
        COLORES["principal"],
        COLORES["secundario"],
        COLORES["acento"]
    ]
)

figuras_fase2["particion_datos"].update_traces(
    textinfo="label+percent"
)

# 5.6 Mejora relativa del MAE

figuras_fase2["mejora_mae"] = go.Figure(
    go.Indicator(
        mode="number",
        value=mejora_mae_f2,
        number={
            "suffix": "%",
            "valueformat": ".2f",
            "font": {
                "size": 65,
                "color": COLORES["secundario"]
            }
        },
        title={
            "text": "Reducción del MAE en validación"
        }
    )
)

# ==========================================================
# 6. APLICAR ESTILO VISUAL
# ==========================================================

for nombre, figura in figuras_fase2.items():

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
        margin=dict(l=45, r=35, t=70, b=65),
        height=420
    )

# ==========================================================
# 7. RECUPERAR IMÁGENES ORIGINALES DEL NOTEBOOK
# ==========================================================

CARPETA_IMAGENES_F2 = FASE2 / "imagenes_originales"

CARPETA_IMAGENES_F2.mkdir(
    parents=True,
    exist_ok=True
)

imagenes_originales_f2 = []

for numero_celda, celda in enumerate(
    celdas_f2, start=1
):

    for numero_salida, salida in enumerate(
        celda.get("outputs", []), start=1
    ):

        datos_salida = salida.get("data", {})

        for mime, extension in [
            ("image/png", ".png"),
            ("image/jpeg", ".jpg")
        ]:

            if mime not in datos_salida:
                continue

            contenido = datos_salida[mime]

            if isinstance(contenido, list):
                contenido = "".join(contenido)

            nombre = (
                f"celda_{numero_celda:02d}"
                f"_salida_{numero_salida:02d}"
                f"{extension}"
            )

            ruta_imagen = (
                CARPETA_IMAGENES_F2 / nombre
            )

            ruta_imagen.write_bytes(
                base64.b64decode(contenido)
            )

            imagenes_originales_f2.append({
                "Celda": numero_celda,
                "Archivo": nombre,
                "Ruta": str(ruta_imagen),
                "Tamaño_KB": round(
                    ruta_imagen.stat().st_size / 1024,
                    2
                )
            })

df_imagenes_f2 = pd.DataFrame(
    imagenes_originales_f2,
    columns=[
        "Celda",
        "Archivo",
        "Ruta",
        "Tamaño_KB"
    ]
)

# ==========================================================
# 8. GUARDAR TABLAS Y FIGURAS
# ==========================================================

tablas_fase2 = {
    "comparacion_modelos": df_validacion_f2,
    "evaluacion_final": df_evaluacion_f2,
    "resultados_r": df_resultados_r_f2,
    "particion_datos": df_particion_f2,
    "inventario_imagenes": df_imagenes_f2
}

for nombre, tabla in tablas_fase2.items():

    tabla.to_csv(
        FASE2 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

CARPETA_GRAFICAS_F2 = FASE2 / "graficas"

CARPETA_GRAFICAS_F2.mkdir(
    parents=True,
    exist_ok=True
)

for nombre, figura in figuras_fase2.items():

    figura.write_html(
        str(CARPETA_GRAFICAS_F2 / f"{nombre}.html"),
        include_plotlyjs=True
    )

    figura.write_json(
        str(CARPETA_GRAFICAS_F2 / f"{nombre}.json")
    )

# ==========================================================
# 9. VALIDACIONES
# ==========================================================

assert df_particion_f2["Registros"].sum() == len(df)

assert modelo_seleccionado_f2 == (
    "Regresión lineal múltiple"
)

assert np.isclose(
    metricas_test_f2["MAE"],
    937.7764,
    atol=0.0001
)

assert np.isclose(
    metricas_test_f2["RMSE"],
    1231.9848,
    atol=0.0001
)

assert np.isclose(
    metricas_test_f2["R2"],
    0.6218,
    atol=0.0001
)

assert float(
    diferencia_r_python.group(1)
) < 1e-8

assert len(figuras_fase2) == 6

assert len(list(
    CARPETA_GRAFICAS_F2.glob("*.html")
)) == 6

assert len(list(
    CARPETA_GRAFICAS_F2.glob("*.json")
)) == 6

# ==========================================================
# 10. PRESENTACIÓN DE RESULTADOS
# ==========================================================

print("=" * 60)
print("FASE 2 - CONSOLIDACIÓN Y VISUALIZACIONES")
print("=" * 60)

print("\n=== COMPARACIÓN DE MODELOS ===")
display(df_validacion_f2)

print("\nModelo seleccionado:", modelo_seleccionado_f2)

print(f"Reducción del MAE: {mejora_mae_f2:.2f}%")

print("\n=== EVALUACIÓN FINAL ===")
display(df_evaluacion_f2)

print("\n=== RESULTADOS COMPLEMENTARIOS EN R ===")
display(df_resultados_r_f2)

print("\n=== PARTICIÓN CRONOLÓGICA ===")
display(df_particion_f2.round(2))

print("\n=== IMÁGENES ORIGINALES RECUPERADAS ===")
display(df_imagenes_f2)

print("\n=== GRÁFICAS INTERACTIVAS ===")

for nombre in figuras_fase2:
    print(f"{nombre}: OK")

print("\n=== VALIDACIONES ===")
print("Integridad de métricas originales: OK")
print("Partición del dataset: OK")
print("Equivalencia R y Python: OK")
print("Modelos reentrenados: 0")
print("Gráficas interactivas:", len(figuras_fase2))
print("Imágenes originales:", len(df_imagenes_f2))

print("\n=== VISTA PREVIA ===")

figuras_fase2["comparacion_modelos"].show()

figuras_fase2["r2_evaluacion"].show()

print("\nFase 2 - Consolidación finalizada correctamente.")