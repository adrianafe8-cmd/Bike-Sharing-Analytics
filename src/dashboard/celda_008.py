# ==========================================================
# DASHBOARD GLOBAL - CELDA 8
# FASE 2: Recuperación de resultados originales
# ==========================================================

import json
import re
from pathlib import Path

BASE_DASHBOARD = Path("/content/Dashboard_Global_Bicicletas")

# 1. Localizar el notebook original de la Fase 2

nombre_notebook_f2 = "Proyecto_Integrador_Bicicletas_Final.ipynb"

archivos_f2 = list(
    BASE_DASHBOARD.rglob(nombre_notebook_f2)
)

assert len(archivos_f2) == 1, (
    f"Se esperaba un notebook de Fase 2. "
    f"Encontrados: {len(archivos_f2)}"
)

ruta_notebook_f2 = archivos_f2[0]

# 2. Crear directorio para resultados de la Fase 2

FASE2 = BASE_DASHBOARD / "resultados" / "Fase_2"

FASE2.mkdir(parents=True, exist_ok=True)

# 3. Leer el notebook sin ejecutar su código

with open(ruta_notebook_f2, "r", encoding="utf-8") as archivo:
    notebook_f2 = json.load(archivo)

celdas_f2 = notebook_f2.get("cells", [])

# 4. Identificar las celdas y sus salidas

inventario_f2 = []
salidas_f2 = []

for numero, celda in enumerate(celdas_f2, start=1):

    tipo = celda.get("cell_type", "")

    fuente = celda.get("source", "")

    if isinstance(fuente, list):
        fuente = "".join(fuente)

    outputs = celda.get("outputs", [])

    inventario_f2.append({
        "Celda": numero,
        "Tipo": tipo,
        "Ejecucion": celda.get("execution_count"),
        "Cantidad_salidas": len(outputs),
        "Contenido": fuente[:180].replace("\n", " ")
    })

    # Recuperar resultados textuales almacenados

    for salida in outputs:

        texto = salida.get("text", "")

        if not texto:
            texto = salida.get("data", {}).get(
                "text/plain", ""
            )

        if isinstance(texto, list):
            texto = "".join(texto)

        if texto:
            salidas_f2.append({
                "Celda": numero,
                "Tipo_salida": salida.get("output_type"),
                "Resultado": texto
            })

# 5. Consolidar los resultados

df_inventario_f2 = pd.DataFrame(inventario_f2)

df_salidas_f2 = pd.DataFrame(
    salidas_f2,
    columns=["Celda", "Tipo_salida", "Resultado"]
)

# 6. Identificar resultados relevantes para regresión

patron_metricas = (
    r"\b(?:MAE|MSE|RMSE|R2|R²|R\^2|MAPE|"
    r"coeficiente|regresión|regresion|regression|"
    r"residuos|residuals|intercepto|accuracy)\b"
)

df_metricas_detectadas_f2 = df_salidas_f2[
    df_salidas_f2["Resultado"].str.contains(
        patron_metricas,
        case=False,
        regex=True,
        na=False
    )
].copy()

# 7. Guardar evidencias recuperadas

df_inventario_f2.to_csv(
    FASE2 / "inventario_notebook_fase2.csv",
    index=False,
    encoding="utf-8-sig"
)

df_salidas_f2.to_csv(
    FASE2 / "salidas_originales_fase2.csv",
    index=False,
    encoding="utf-8-sig"
)

df_metricas_detectadas_f2.to_csv(
    FASE2 / "metricas_detectadas_fase2.csv",
    index=False,
    encoding="utf-8-sig"
)

# 8. Presentar resultados

print("=" * 60)
print("FASE 2 - RECUPERACIÓN DE RESULTADOS ORIGINALES")
print("=" * 60)

print("\nNotebook:", ruta_notebook_f2.name)

print("Total de celdas:", len(celdas_f2))

print("Celdas de código:", sum(
    c.get("cell_type") == "code"
    for c in celdas_f2
))

print("Celdas Markdown:", sum(
    c.get("cell_type") == "markdown"
    for c in celdas_f2
))

print("Salidas textuales recuperadas:", len(df_salidas_f2))

print("Salidas con posibles métricas:",
      len(df_metricas_detectadas_f2))

print("\n=== INVENTARIO DE CELDAS ===")

display(df_inventario_f2)

print("\n=== RESULTADOS DE REGRESIÓN DETECTADOS ===")

for _, fila in df_metricas_detectadas_f2.iterrows():

    print("\n" + "-" * 60)
    print("Celda:", fila["Celda"])
    print("-" * 60)
    print(fila["Resultado"][:6000])

# 9. Validaciones

assert len(celdas_f2) > 0

assert len(df_salidas_f2) > 0, (
    "El notebook no contiene resultados textuales guardados."
)

print("\n=== VALIDACIONES ===")
print("Lectura del notebook: OK")
print("Recuperación de salidas: OK")
print("Archivos CSV generados: 3")
print("Modelos reentrenados: 0")

print("\nFase 2 - Recuperación de evidencias finalizada.")