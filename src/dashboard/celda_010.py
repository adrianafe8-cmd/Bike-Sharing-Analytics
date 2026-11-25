# ==========================================================
# DASHBOARD GLOBAL - CELDA 10
# FASE 3: Recuperación de resultados originales
# ==========================================================

import json
import re
import base64
from pathlib import Path

# ==========================================================
# 1. LOCALIZAR EL NOTEBOOK ORIGINAL
# ==========================================================

nombre_notebook_f3 = (
    "Fase_3_Modelado_Avanzado_Bicicletas.ipynb"
)

archivos_f3 = list(
    BASE_DASHBOARD.rglob(nombre_notebook_f3)
)

assert len(archivos_f3) == 1, (
    f"Se esperaba un notebook de Fase 3. "
    f"Encontrados: {len(archivos_f3)}"
)

ruta_notebook_f3 = archivos_f3[0]

# Crear directorios para almacenar las evidencias.

FASE3 = BASE_DASHBOARD / "resultados" / "Fase_3"

FASE3.mkdir(parents=True, exist_ok=True)

CARPETA_IMAGENES_F3 = FASE3 / "imagenes_originales"

CARPETA_IMAGENES_F3.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# 2. LEER EL NOTEBOOK SIN EJECUTAR SU CÓDIGO
# ==========================================================

with open(
    ruta_notebook_f3,
    "r",
    encoding="utf-8"
) as archivo:

    notebook_f3 = json.load(archivo)

celdas_f3 = notebook_f3.get("cells", [])

assert len(celdas_f3) > 0, (
    "El notebook no contiene celdas."
)

# ==========================================================
# 3. RECUPERAR INVENTARIO, SALIDAS E IMÁGENES
# ==========================================================

inventario_f3 = []
salidas_f3 = []
imagenes_originales_f3 = []
errores_f3 = []

for numero_celda, celda in enumerate(
    celdas_f3,
    start=1
):

    tipo = celda.get("cell_type", "")

    fuente = celda.get("source", "")

    if isinstance(fuente, list):
        fuente = "".join(fuente)

    outputs = celda.get("outputs", [])

    inventario_f3.append({
        "Celda": numero_celda,
        "Tipo": tipo,
        "Ejecucion": celda.get("execution_count"),
        "Cantidad_salidas": len(outputs),
        "Contenido": fuente[:200].replace("\n", " ")
    })

    for numero_salida, salida in enumerate(
        outputs,
        start=1
    ):

        datos_salida = salida.get("data", {})

        # Recuperar resultados textuales originales.

        texto = salida.get("text", "")

        if not texto:
            texto = datos_salida.get("text/plain", "")

        if isinstance(texto, list):
            texto = "".join(texto)

        if texto:

            salidas_f3.append({
                "Celda": numero_celda,
                "Salida": numero_salida,
                "Tipo_salida": salida.get("output_type"),
                "Resultado": texto
            })

        # Identificar posibles errores históricos.

        if salida.get("output_type") == "error":

            errores_f3.append({
                "Celda": numero_celda,
                "Error": salida.get("ename"),
                "Descripcion": salida.get("evalue")
            })

        # Recuperar imágenes originales.

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
                CARPETA_IMAGENES_F3 / nombre
            )

            ruta_imagen.write_bytes(
                base64.b64decode(contenido)
            )

            imagenes_originales_f3.append({
                "Celda": numero_celda,
                "Archivo": nombre,
                "Ruta": str(ruta_imagen),
                "Tamaño_KB": round(
                    ruta_imagen.stat().st_size / 1024,
                    2
                )
            })

# ==========================================================
# 4. CONSOLIDAR LAS EVIDENCIAS
# ==========================================================

df_inventario_f3 = pd.DataFrame(inventario_f3)

df_salidas_f3 = pd.DataFrame(
    salidas_f3,
    columns=[
        "Celda",
        "Salida",
        "Tipo_salida",
        "Resultado"
    ]
)

df_imagenes_f3 = pd.DataFrame(
    imagenes_originales_f3,
    columns=[
        "Celda",
        "Archivo",
        "Ruta",
        "Tamaño_KB"
    ]
)

df_errores_f3 = pd.DataFrame(
    errores_f3,
    columns=[
        "Celda",
        "Error",
        "Descripcion"
    ]
)

assert not df_salidas_f3.empty, (
    "No se encontraron resultados textuales guardados."
)

# ==========================================================
# 5. IDENTIFICAR MÉTRICAS Y RESULTADOS RELEVANTES
# ==========================================================

patrones_f3 = {

    "Regresion": (
        r"\b(?:MAE|RMSE|MSE|R2|R²|Ridge|"
        r"Regressor|regresión|regresion)\b"
    ),

    "Clasificacion": (
        r"\b(?:Accuracy|Precision|Recall|"
        r"F1|F1_score|F1_macro|AUC|AUC_ROC|"
        r"ROC|KNN|Classifier|clasificación|"
        r"clasificacion|umbral)\b"
    ),

    "Clustering": (
        r"\b(?:Silhouette|KMeans|K-Means|"
        r"Agglomerative|clustering|"
        r"ARI|inercia|Davies|Calinski)\b"
    ),

    "Validacion": (
        r"\b(?:validación|validacion|"
        r"TimeSeriesSplit|fold|folds|"
        r"hiperparámetros|hiperparametros|"
        r"seleccionado|partición|particion)\b"
    )
}

resultados_detectados_f3 = {}

for categoria, patron in patrones_f3.items():

    resultados_detectados_f3[categoria] = (
        df_salidas_f3.loc[
            df_salidas_f3["Resultado"].str.contains(
                patron,
                case=False,
                regex=True,
                na=False
            )
        ].copy()
    )

# Consolidar sin duplicar salidas que pertenecen
# a más de una categoría.

df_metricas_detectadas_f3 = (
    pd.concat(
        resultados_detectados_f3.values(),
        ignore_index=True
    )
    .drop_duplicates(
        subset=["Celda", "Salida"]
    )
    .sort_values(["Celda", "Salida"])
    .reset_index(drop=True)
)

# ==========================================================
# 6. GUARDAR EVIDENCIAS RECUPERADAS
# ==========================================================

tablas_recuperadas_f3 = {

    "inventario_notebook_fase3":
        df_inventario_f3,

    "salidas_originales_fase3":
        df_salidas_f3,

    "metricas_detectadas_fase3":
        df_metricas_detectadas_f3,

    "inventario_imagenes_fase3":
        df_imagenes_f3,

    "errores_historicos_fase3":
        df_errores_f3
}

for nombre, tabla in tablas_recuperadas_f3.items():

    tabla.to_csv(
        FASE3 / f"{nombre}.csv",
        index=False,
        encoding="utf-8-sig"
    )

# Guardar resultados por categoría.

for categoria, tabla in resultados_detectados_f3.items():

    tabla.to_csv(
        FASE3 / f"resultados_{categoria.lower()}.csv",
        index=False,
        encoding="utf-8-sig"
    )

# ==========================================================
# 7. PRESENTAR RESUMEN DE RECUPERACIÓN
# ==========================================================

print("=" * 60)
print("FASE 3 - RECUPERACIÓN DE RESULTADOS ORIGINALES")
print("=" * 60)

print("\nNotebook:", ruta_notebook_f3.name)

print("Total de celdas:", len(celdas_f3))

print(
    "Celdas de código:",
    sum(
        c.get("cell_type") == "code"
        for c in celdas_f3
    )
)

print(
    "Celdas Markdown:",
    sum(
        c.get("cell_type") == "markdown"
        for c in celdas_f3
    )
)

print(
    "Salidas textuales recuperadas:",
    len(df_salidas_f3)
)

print(
    "Imágenes originales recuperadas:",
    len(df_imagenes_f3)
)

print(
    "Errores históricos detectados:",
    len(df_errores_f3)
)

print("\n=== RESULTADOS POR CATEGORÍA ===")

for categoria, tabla in resultados_detectados_f3.items():

    print(f"{categoria}: {len(tabla)} salidas")

# ==========================================================
# 8. MOSTRAR INVENTARIO DE CELDAS
# ==========================================================

print("\n=== INVENTARIO DE CELDAS ===")

print(
    df_inventario_f3[
        [
            "Celda",
            "Tipo",
            "Ejecucion",
            "Cantidad_salidas",
            "Contenido"
        ]
    ].to_string(index=False)
)

# ==========================================================
# 9. MOSTRAR RESULTADOS ORIGINALES
# ==========================================================

print("\n=== MÉTRICAS Y RESULTADOS DETECTADOS ===")

for _, fila in df_metricas_detectadas_f3.iterrows():

    print("\n" + "-" * 60)

    print(
        f"Celda: {fila['Celda']} | "
        f"Salida: {fila['Salida']}"
    )

    print("-" * 60)

    print(fila["Resultado"][:8000])

# ==========================================================
# 10. MOSTRAR IMÁGENES Y ERRORES HISTÓRICOS
# ==========================================================

print("\n=== IMÁGENES ORIGINALES RECUPERADAS ===")

print(
    df_imagenes_f3[
        ["Celda", "Archivo", "Tamaño_KB"]
    ].to_string(index=False)
)

if not df_errores_f3.empty:

    print("\n=== ERRORES HISTÓRICOS ===")

    print(
        df_errores_f3.to_string(index=False)
    )

# ==========================================================
# 11. VALIDACIONES FINALES
# ==========================================================

assert len(df_inventario_f3) == len(celdas_f3)

assert len(df_metricas_detectadas_f3) > 0, (
    "No se detectaron métricas relevantes."
)

assert all(
    Path(ruta).exists()
    for ruta in df_imagenes_f3["Ruta"]
)

assert all(
    (FASE3 / f"{nombre}.csv").exists()
    for nombre in tablas_recuperadas_f3
)

print("\n=== VALIDACIONES ===")

print("Lectura del notebook: OK")
print("Recuperación de salidas: OK")
print("Recuperación de imágenes: OK")
print("Archivos CSV generados: 9")
print("Modelos reentrenados: 0")

print(
    "\nFase 3 - Recuperación de evidencias finalizada."
)