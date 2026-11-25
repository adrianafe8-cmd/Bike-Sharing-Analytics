# ==========================================================
# DASHBOARD GLOBAL - CELDA 12
# FASE 4: Recuperación y consolidación de evidencias
# ==========================================================

import json
import shutil
from pathlib import Path

# ==========================================================
# 1. CONFIGURAR DIRECTORIOS
# ==========================================================

ORIGEN_FASE4 = EVIDENCIAS / "Fase_4"

FASE4 = BASE_DASHBOARD / "resultados" / "Fase_4"

FASE4.mkdir(parents=True, exist_ok=True)

CARPETA_IMAGENES_F4 = FASE4 / "imagenes_originales"

CARPETA_IMAGENES_F4.mkdir(
    parents=True,
    exist_ok=True
)

assert ORIGEN_FASE4.exists(), (
    "No se encontró el directorio de evidencias de Fase 4."
)

# ==========================================================
# 2. RECUPERAR ARCHIVOS CSV ORIGINALES
# ==========================================================

# Se cargan directamente los resultados generados durante
# la ejecución original de la Fase 4.

tablas_fase4 = {}

inventario_csv_f4 = []

for ruta in sorted(ORIGEN_FASE4.rglob("*.csv")):

    nombre = ruta.stem

    assert nombre not in tablas_fase4, (
        f"Nombre de archivo duplicado: {nombre}"
    )

    tabla = pd.read_csv(
        ruta,
        encoding="utf-8-sig"
    )

    tablas_fase4[nombre] = tabla

    inventario_csv_f4.append({
        "Archivo": ruta.name,
        "Filas": tabla.shape[0],
        "Columnas": tabla.shape[1],
        "Variables": ", ".join(
            tabla.columns.astype(str)
        ),
        "Ruta_original": str(ruta)
    })

    # Conservar una copia exacta del archivo original.

    shutil.copy2(
        ruta,
        FASE4 / ruta.name
    )

df_inventario_csv_f4 = pd.DataFrame(
    inventario_csv_f4
)

assert len(tablas_fase4) > 0, (
    "No se recuperaron archivos CSV."
)

# ==========================================================
# 3. VALIDAR TABLAS PRINCIPALES
# ==========================================================

tablas_requeridas_f4 = [

    "metricas_baseline_regresion",
    "metricas_baseline_clasificacion",
    "resumen_final_regresion",
    "resumen_final_clasificacion",
    "resumen_mejoras",
    "resumen_preparacion",
    "cumplimiento_requerimientos",
    "detalle_outliers",
    "limites_winsorization",
    "resultados_winsorization",
    "resultados_codificacion",
    "verificacion_estandarizacion",
    "estrategia_balanceo",
    "matrices_finales"
]

tablas_faltantes_f4 = [

    nombre
    for nombre in tablas_requeridas_f4
    if nombre not in tablas_fase4
]

assert not tablas_faltantes_f4, (
    f"Tablas faltantes: {tablas_faltantes_f4}"
)

# ==========================================================
# 4. ASIGNAR TABLAS PRINCIPALES
# ==========================================================

df_regresion_f4 = tablas_fase4[
    "metricas_baseline_regresion"
].copy()

df_clasificacion_f4 = tablas_fase4[
    "metricas_baseline_clasificacion"
].copy()

df_resumen_regresion_f4 = tablas_fase4[
    "resumen_final_regresion"
].copy()

df_resumen_clasificacion_f4 = tablas_fase4[
    "resumen_final_clasificacion"
].copy()

df_mejoras_f4 = tablas_fase4[
    "resumen_mejoras"
].copy()

df_preparacion_f4 = tablas_fase4[
    "resumen_preparacion"
].copy()

df_cumplimiento_f4 = tablas_fase4[
    "cumplimiento_requerimientos"
].copy()

df_outliers_f4 = tablas_fase4[
    "detalle_outliers"
].copy()

df_limites_f4 = tablas_fase4[
    "limites_winsorization"
].copy()

df_winsorization_f4 = tablas_fase4[
    "resultados_winsorization"
].copy()

df_codificacion_f4 = tablas_fase4[
    "resultados_codificacion"
].copy()

df_estandarizacion_f4 = tablas_fase4[
    "verificacion_estandarizacion"
].copy()

df_balanceo_f4 = tablas_fase4[
    "estrategia_balanceo"
].copy()

df_matrices_f4 = tablas_fase4[
    "matrices_finales"
].copy()

# ==========================================================
# 5. RECUPERAR IMÁGENES ORIGINALES
# ==========================================================

imagenes_originales_f4 = []

for ruta in sorted(ORIGEN_FASE4.rglob("*")):

    if not ruta.is_file():
        continue

    if ruta.suffix.lower() not in [
        ".png", ".jpg", ".jpeg"
    ]:
        continue

    destino = CARPETA_IMAGENES_F4 / ruta.name

    shutil.copy2(
        ruta,
        destino
    )

    imagenes_originales_f4.append({
        "Archivo": ruta.name,
        "Formato": ruta.suffix.lower(),
        "Tamaño_KB": round(
            destino.stat().st_size / 1024,
            2
        ),
        "Ruta": str(destino)
    })

df_imagenes_f4 = pd.DataFrame(
    imagenes_originales_f4,
    columns=[
        "Archivo",
        "Formato",
        "Tamaño_KB",
        "Ruta"
    ]
)

# ==========================================================
# 6. RECUPERAR METADATOS DE REPRODUCIBILIDAD
# ==========================================================

metadatos_f4 = {}

for ruta in sorted(ORIGEN_FASE4.rglob("*.json")):

    with open(
        ruta,
        "r",
        encoding="utf-8-sig"
    ) as archivo:

        metadatos_f4[ruta.stem] = json.load(
            archivo
        )

    shutil.copy2(
        ruta,
        FASE4 / ruta.name
    )

# ==========================================================
# 7. GUARDAR INVENTARIOS
# ==========================================================

df_inventario_csv_f4.to_csv(
    FASE4 / "inventario_csv_fase4.csv",
    index=False,
    encoding="utf-8-sig"
)

df_imagenes_f4.to_csv(
    FASE4 / "inventario_imagenes_fase4.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 8. PRESENTAR RESULTADOS RECUPERADOS
# ==========================================================

print("=" * 60)
print("FASE 4 - RECUPERACIÓN Y CONSOLIDACIÓN")
print("=" * 60)

print("\nArchivos CSV recuperados:", len(tablas_fase4))

print("Imágenes originales:", len(df_imagenes_f4))

print("Archivos JSON:", len(metadatos_f4))

print("\n=== INVENTARIO DE TABLAS ===")

print(
    df_inventario_csv_f4[
        ["Archivo", "Filas", "Columnas"]
    ].to_string(index=False)
)

# Mostrar las tablas principales sin generar
# código HTML adicional en la salida de Colab.

tablas_revision_f4 = {

    "MÉTRICAS BASELINE DE REGRESIÓN":
        df_regresion_f4,

    "MÉTRICAS BASELINE DE CLASIFICACIÓN":
        df_clasificacion_f4,

    "RESUMEN FINAL DE REGRESIÓN":
        df_resumen_regresion_f4,

    "RESUMEN FINAL DE CLASIFICACIÓN":
        df_resumen_clasificacion_f4,

    "MEJORAS DE LOS MODELOS":
        df_mejoras_f4,

    "RESUMEN DE PREPARACIÓN":
        df_preparacion_f4,

    "CUMPLIMIENTO DE REQUERIMIENTOS":
        df_cumplimiento_f4,

    "DETECCIÓN DE OUTLIERS":
        df_outliers_f4,

    "LÍMITES DE WINSORIZATION":
        df_limites_f4,

    "RESULTADOS DE WINSORIZATION":
        df_winsorization_f4,

    "CODIFICACIÓN DE VARIABLES":
        df_codificacion_f4,

    "ESTANDARIZACIÓN":
        df_estandarizacion_f4,

    "ESTRATEGIA DE BALANCEO":
        df_balanceo_f4,

    "MATRICES DE CONFUSIÓN":
        df_matrices_f4
}

for titulo, tabla in tablas_revision_f4.items():

    print(f"\n=== {titulo} ===")

    print(tabla.to_string(index=False))

print("\n=== IMÁGENES ORIGINALES ===")

print(
    df_imagenes_f4[
        ["Archivo", "Tamaño_KB"]
    ].to_string(index=False)
)

print("\n=== METADATOS DE REPRODUCIBILIDAD ===")

for nombre, contenido in metadatos_f4.items():

    print(f"\nArchivo: {nombre}.json")

    print(
        json.dumps(
            contenido,
            indent=2,
            ensure_ascii=False
        )
    )

# ==========================================================
# 9. VALIDACIONES FINALES
# ==========================================================

assert len(tablas_fase4) == 19, (
    "La cantidad de CSV no coincide con el inventario."
)

assert len(df_imagenes_f4) == 12, (
    "La cantidad de imágenes no coincide con el inventario."
)

assert len(metadatos_f4) == 2

assert (
    len(tablas_fase4)
    + len(df_imagenes_f4)
    + len(metadatos_f4)
) == 33

assert all(
    not tabla.empty
    for tabla in tablas_fase4.values()
)

assert all(
    Path(ruta).exists()
    for ruta in df_imagenes_f4["Ruta"]
)

assert all(
    (FASE4 / f"{nombre}.csv").exists()
    for nombre in tablas_fase4
)

print("\n=== VALIDACIONES ===")

print("Recuperación de archivos CSV: OK")
print("Recuperación de imágenes: OK")
print("Recuperación de metadatos: OK")
print("Tablas principales disponibles: OK")
print("Integridad del inventario: OK")
print("Total de evidencias originales: 33")
print("Modelos reentrenados: 0")

print(
    "\nFase 4 - Recuperación de evidencias finalizada."
)